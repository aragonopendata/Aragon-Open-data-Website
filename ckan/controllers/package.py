# -*- coding: utf-8 -*-
import logging
from urllib import urlencode
import datetime

from pylons import config
from genshi.template import MarkupTemplate
from genshi.template.text import NewTextTemplate
from paste.deploy.converters import asbool

import ckan.logic as logic
import ckan.lib.base as base
import ckan.lib.maintain as maintain
import ckan.lib.package_saver as package_saver
import ckan.lib.i18n as i18n
import ckan.lib.navl.dictization_functions as dict_fns
import ckan.lib.accept as accept
import ckan.lib.helpers as h
import ckan.model as model
import ckan.lib.datapreview as datapreview
import ckan.lib.plugins
import ckan.plugins as p

from ckan.common import OrderedDict, _, json, request, c, g, response
from home import CACHE_PARAMETERS

import cx_Oracle
import psycopg2

import MySQLdb

from ckan.ckanclient import config as configuracion

from ckan.ckanclient import sustCaracter as sustCaracter


import re
from time import time
from urllib import urlretrieve
from os import remove
import xlrd
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
from json import JSONEncoder
import csv
import urllib
import htmllib
from StringIO import StringIO


BLACKLIST = ("id", "package_id", "vocabulary_id", "revision_id",
             "resource_group_id", "relationships_as_object",
             "revision_timestamp", "author_email", "version", "type",
             "cache_last_updated", "webstore_last_updated", "hash",
             "tracking_summary", "total", "recent", "mimetype_inner",
             "cache_url", "webstore_url", "position", "capacity", "image_url",
             "approval_status", "isopen", "relationships_as_subject")


log = logging.getLogger(__name__)

render = base.render
abort = base.abort
redirect = base.redirect

NotFound = logic.NotFound
NotAuthorized = logic.NotAuthorized
ValidationError = logic.ValidationError
check_access = logic.check_access
get_action = logic.get_action
tuplize_dict = logic.tuplize_dict
clean_dict = logic.clean_dict
parse_params = logic.parse_params
flatten_to_string_key = logic.flatten_to_string_key

lookup_package_plugin = ckan.lib.plugins.lookup_package_plugin

asciify = h.asciify

#Esta función recibe un str y si tiene url (http://) lo metemos como si fuese enlaces en html. Con href
def url2HREF(str):
    dev=""
    if str.find('http://') != -1:
        iniURL = 0
        longURL = 0
        iniURL = str.find("http://");
        while (iniURL!= -1):
            longURL=str[iniURL:].find(" ");
            if (longURL==-1):
                longURL =len(str[iniURL:])
            if (iniURL==0):
                dev = dev + "<a href=\""+str[iniURL:iniURL+longURL]+ "\">"+str[iniURL:iniURL+longURL]+"</a>"
            else:
                dev = dev + str[:iniURL-1]+ " <a href=\""+str[iniURL:iniURL+longURL]+ "\">"+str[iniURL:iniURL+longURL]+"</a>"
            if iniURL+longURL <= len(str):
                str = str[iniURL+longURL:]
                iniURL = str.find("http://");
                if (iniURL==-1):
                    dev = dev +str
            else:
                str=""
        return dev
    return str

def _encode_params(params):
    return [(k, v.encode('utf-8') if isinstance(v, basestring) else str(v))
            for k, v in params]


def url_with_params(url, params):
    params = _encode_params(params)
    return url + u'?' + urlencode(params)


def search_url(params, package_type=None):
    if not package_type or package_type == 'catalogo':
        url = h.url_for(controller='package', action='search')
    elif package_type == 'catalogoAOD':
        url = request.path
    elif package_type == 'recomendPackage':
        url = request.path
    else:
        url = h.url_for('{0}_search'.format(package_type))
    return url_with_params(url, params)


class PackageController(base.BaseController):

    def _package_form(self, package_type=None):
        return lookup_package_plugin(package_type).package_form()

    def _setup_template_variables(self, context, data_dict, package_type=None):
        return lookup_package_plugin(package_type).\
            setup_template_variables(context, data_dict)

    def _new_template(self, package_type):
        return lookup_package_plugin(package_type).new_template()

    def _edit_template(self, package_type):
        return lookup_package_plugin(package_type).edit_template()

    def _search_template(self, package_type):
        return lookup_package_plugin(package_type).search_template()

    def _read_template(self, package_type):
        return lookup_package_plugin(package_type).read_template()

    def _history_template(self, package_type):
        return lookup_package_plugin(package_type).history_template()

    def _guess_package_type(self, expecting_name=False):
        """
            Guess the type of package from the URL handling the case
            where there is a prefix on the URL (such as /data/package)
        """

        # Special case: if the rot URL '/' has been redirected to the package
        # controller (e.g. by an IRoutes extension) then there's nothing to do
        # here.
        if request.path == '/':
            return 'catalogo'

        parts = [x for x in request.path.split('/') if x]

        idx = -1
        if expecting_name:
            idx = -2

        pt = parts[idx]
        if pt == 'package':
            pt = 'catalogo'

        if pt == 'catalogo.html':
            pt = 'catalogo'

        if pt == 'catalogo':
            pt = 'catalogo'

        return pt

    def search(self):
        from ckan.lib.search import SearchError

        package_type = self._guess_package_type()

        try:
            context = {'model': model, 'user': c.user or c.author}
            check_access('site_read', context)
        except NotAuthorized:
            abort(401, _('Not authorized to see this page'))

        # unicode format (decoded from utf8)
        #[M] no asciify in param q
        q = c.q = request.params.get('q', u'')
        #q = c.q = asciify(request.params.get('q', u''))
        #log.error('######La consulta en SolR al principio: %s', q)
        c.query_error = False
        try:
            page = int(request.params.get('page', 1))
        except ValueError, e:
            abort(400, ('"page" parameter must be an integer'))
        limit = g.datasets_per_page

        # most search operations should reset the page counter:
        params_nopage = [(k, v) for k, v in request.params.items()
                         if k != 'page']

        def drill_down_url(alternative_url=None, **by):
            return h.add_url_param(alternative_url=alternative_url,
                                   controller='package', action='search',
                                   new_params=by)

        c.drill_down_url = drill_down_url

        def remove_field(key, value=None, replace=None):
            return h.remove_url_param(key, value=value, replace=replace,
                                  controller='package', action='search')

        c.remove_field = remove_field

        sort_by = request.params.get('sort', None)
        params_nosort = [(k, v) for k, v in params_nopage if k != 'sort']

        def _sort_by(fields):
            """
            Sort by the given list of fields.

            Each entry in the list is a 2-tuple: (fieldname, sort_order)

            eg - [('metadata_modified', 'desc'), ('name', 'asc')]

            If fields is empty, then the default ordering is used.
            """
            params = params_nosort[:]

            if fields:
                sort_string = ', '.join('%s %s' % f for f in fields)
                params.append(('sort', sort_string))
            return search_url(params, package_type)

        c.sort_by = _sort_by
        if sort_by is None:
            c.sort_by_fields = []
        else:
            c.sort_by_fields = [field.split()[0]
                                for field in sort_by.split(',')]

        def pager_url(q=None, page=None):
            params = list(params_nopage)
            params.append(('page', page))
            return search_url(params, package_type)

        c.search_url_params = urlencode(_encode_params(params_nopage))

        try:
            c.fields = []
            # c.fields_grouped will contain a dict of params containing
            # a list of values eg {'tags':['tag1', 'tag2']}
            c.fields_grouped = {}
            search_extras = {}
            fq = ''
            formats = ''
            for (param, value) in request.params.items():
                if param not in ['q', 'page', 'sort'] \
                        and len(value) and not param.startswith('_'):

                    if param.startswith('res_format') and value in ('XML', 'JSON', 'CSV'):
                        if len(q):
                            q += ' AND (res_format:"%s" OR res_format:"%s")' % (value, 'XLS')
                        else:
                            q = 'res_format:"%s" OR res_format:"%s"' % (value, 'XLS')
                        c.fields.append((param, value))

                        #TODO: no estaba antes
                        if param not in c.fields_grouped:
                            c.fields_grouped[param] = [value]
                        else:
                            c.fields_grouped[param].append(value)

                    elif not param.startswith('ext_'):
                        c.fields.append((param, value))
                        fq += ' %s:"%s"' % (param, value)
                        if param not in c.fields_grouped:
                            c.fields_grouped[param] = [value]
                        else:
                            c.fields_grouped[param].append(value)
                    else:
                        search_extras[param] = value

            context = {'model': model, 'session': model.Session,
                       'user': c.user or c.author, 'for_view': True}

            if package_type and package_type != 'catalogo':
                # Only show datasets of this particular type
                fq += ' +dataset_type:{type}'.format(type=package_type)
            else:
                # Unless changed via config options, don't show non standard
                # dataset types on the default search page
                if not asbool(config.get('ckan.search.show_all_types', 'False')):
                    fq += ' +dataset_type:dataset'

            facets = OrderedDict()

            default_facet_titles = {
                    'organization': _('Organizations'),
                    'groups': _('Groups'),
                    'tags': _('Tags'),
                    'res_format': _('Formats'),
                    'license_id': _('License'),
                    }

            for facet in g.facets:
                if facet in default_facet_titles:
                    facets[facet] = default_facet_titles[facet]
                else:
                    facets[facet] = facet

            # Facet titles
            for plugin in p.PluginImplementations(p.IFacets):
                facets = plugin.dataset_facets(facets, package_type)

            c.facet_titles = facets

            data_dict = {
                'q': q,
                'fq': fq.strip(),
                'facet.field': facets.keys(),
                'rows': limit,
                'start': (page - 1) * limit,
                'sort': sort_by,
                'extras': search_extras
            }

            query = get_action('package_search')(context, data_dict)
            c.sort_by_selected = query['sort']

            c.page = h.Page(
                collection=query['results'],
                page=page,
                url=pager_url,
                item_count=query['count'],
                items_per_page=limit
            )
            c.facets = query['facets']
            c.search_facets = query['search_facets']
            c.page.items = query['results']
        except SearchError, se:
            log.error('Dataset search error: %r', se.args)
            c.query_error = True
            c.facets = {}
            c.search_facets = {}
            c.page = h.Page(collection=[])
        c.search_facets_limits = {}
        for facet in c.search_facets.keys():
            limit = int(request.params.get('_%s_limit' % facet,
                                           g.facets_default_number))
            c.search_facets_limits[facet] = limit

        maintain.deprecate_context_item(
          'facets',
          'Use `c.search_facets` instead.')

        self._setup_template_variables(context, {},
                                       package_type=package_type)

        return render(self._search_template(package_type))

    def _content_type_from_extension(self, ext):
        ct, mu, ext = accept.parse_extension(ext)
        if not ct:
            return None, None, None,
        return ct, ext, (NewTextTemplate, MarkupTemplate)[mu]

    def _content_type_from_accept(self):
        """
        Given a requested format this method determines the content-type
        to set and the genshi template loader to use in order to render
        it accurately.  TextTemplate must be used for non-xml templates
        whilst all that are some sort of XML should use MarkupTemplate.
        """
        ct, mu, ext = accept.parse_header(request.headers.get('Accept', ''))
        return ct, ext, (NewTextTemplate, MarkupTemplate)[mu]

    def read(self, id, format='html'):
        if (format == 'homer'):
            ctype, format, loader = "application/xml; charset=utf-8", "homer", \
                    MarkupTemplate
        elif not format == 'html':
            ctype, extension, loader = \
                self._content_type_from_extension(format)
            if not ctype:
                # An unknown format, we'll carry on in case it is a
                # revision specifier and re-constitute the original id
                id = "%s.%s" % (id, format)
                ctype, format, loader = "text/html; charset=utf-8", "html", \
                    MarkupTemplate
        else:
            ctype, format, loader = self._content_type_from_accept()

        response.headers['Content-Type'] = ctype

        package_type = self._get_package_type(id.split('@')[0])
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True}
        data_dict = {'id': id}

        # interpret @<revision_id> or @<date> suffix
        split = id.split('@')
        if len(split) == 2:
            data_dict['id'], revision_ref = split
            if model.is_id(revision_ref):
                context['revision_id'] = revision_ref
            else:
                try:
                    date = h.date_str_to_datetime(revision_ref)
                    context['revision_date'] = date
                except TypeError, e:
                    abort(400, _('Invalid revision format: %r') % e.args)
                except ValueError, e:
                    abort(400, _('Invalid revision format: %r') % e.args)
        elif len(split) > 2:
            abort(400, _('Invalid revision format: %r') %
                  'Too many "@" symbols')

        # check if package exists
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            #Ejemplo de como cambiar la licencia
            #c.pkg_dict['license_title']='perico'
            
            #Recorremos todos los extras para que modifique los value que tiene una uri dentro de ella  para que les añada el href
#            for extra in c.pkg_dict['extras']:
#                extra['value']=url2HREF(extra['value'])

            c.pkg = context['package']
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        # used by disqus plugin
        c.current_package_id = c.pkg.id
        c.related_count = c.pkg.related_count

        # can the resources be previewed?
        for resource in c.pkg_dict['resources']:
            resource['can_be_previewed'] = self._resource_preview(
                {'resource': resource, 'package': c.pkg_dict})

        self._setup_template_variables(context, {'id': id},
                                       package_type=package_type)

        package_saver.PackageSaver().render_package(c.pkg_dict, context)

        template = self._read_template(package_type)
        template = template[:template.index('.') + 1] + format
        log.error('Entro en el read y el package es '+ str(c.pkg_dict['name']))
        
        
        self.getRecomendedPackages(c.pkg_dict['name'])
        

        return render(template, loader_class=loader)

    def history(self, id):
        package_type = self._get_package_type(id.split('@')[0])

        if 'diff' in request.params or 'selected1' in request.params:
            try:
                params = {'id': request.params.getone('pkg_name'),
                          'diff': request.params.getone('selected1'),
                          'oldid': request.params.getone('selected2'),
                          }
            except KeyError, e:
                if 'pkg_name' in dict(request.params):
                    id = request.params.getone('pkg_name')
                c.error = \
                    _('Select two revisions before doing the comparison.')
            else:
                params['diff_entity'] = 'package'
                h.redirect_to(controller='revision', action='diff', **params)

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author}
        data_dict = {'id': id}
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg_revisions = get_action('package_revision_list')(context,
                                                                  data_dict)
            # TODO: remove
            # Still necessary for the authz check in group/layout.html
            c.pkg = context['package']

        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % '')
        except NotFound:
            abort(404, _('Dataset not found'))

        format = request.params.get('format', '')
        if format == 'atom':
            # Generate and return Atom 1.0 document.
            from webhelpers.feedgenerator import Atom1Feed
            feed = Atom1Feed(
                title=_(u'CKAN Dataset Revision History'),
                link=h.url_for(controller='revision', action='read',
                               id=c.pkg_dict['name']),
                description=_(u'Recent changes to CKAN Dataset: ') +
                (c.pkg_dict['title'] or ''),
                language=unicode(i18n.get_lang()),
            )
            for revision_dict in c.pkg_revisions:
                revision_date = h.date_str_to_datetime(
                    revision_dict['timestamp'])
                try:
                    dayHorizon = int(request.params.get('days'))
                except:
                    dayHorizon = 30
                dayAge = (datetime.datetime.now() - revision_date).days
                if dayAge >= dayHorizon:
                    break
                if revision_dict['message']:
                    item_title = u'%s' % revision_dict['message'].\
                        split('\n')[0]
                else:
                    item_title = u'%s' % revision_dict['id']
                item_link = h.url_for(controller='revision', action='read',
                                      id=revision_dict['id'])
                item_description = _('Log message: ')
                item_description += '%s' % (revision_dict['message'] or '')
                item_author_name = revision_dict['author']
                item_pubdate = revision_date
                feed.add_item(
                    title=item_title,
                    link=item_link,
                    description=item_description,
                    author_name=item_author_name,
                    pubdate=item_pubdate,
                )
            feed.content_type = 'application/atom+xml'
            return feed.writeString('utf-8')

        c.related_count = c.pkg.related_count
        return render(self._history_template(c.pkg_dict.get('type',
                                                            package_type)))

    def new(self, data=None, errors=None, error_summary=None):
        package_type = self._guess_package_type(True)
        #HIBERUS: FUERZO EL TIPO DEL PACKAGE PARA QUE APAREZCA EN EL LISTADO
        package_type = 'dataset'

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author,
                   'save': 'save' in request.params}

        # Package needs to have a organization group in the call to
        # check_access and also to save it
        try:
            check_access('package_create', context)
        except NotAuthorized:
            abort(401, _('Unauthorized to create a package'))

        if context['save'] and not data:
            return self._save_new(context, package_type=package_type)

        data = data or clean_dict(dict_fns.unflatten(tuplize_dict(parse_params(
            request.params, ignore_keys=CACHE_PARAMETERS))))
        c.resources_json = h.json.dumps(data.get('resources', []))
        # convert tags if not supplied in data
        if data and not data.get('tag_string'):
            data['tag_string'] = ', '.join(
                h.dict_list_reduce(data.get('tags', {}), 'name'))

        errors = errors or {}
        error_summary = error_summary or {}
        # in the phased add dataset we need to know that
        # we have already completed stage 1
        stage = ['active']
        if data.get('state') == 'draft':
            stage = ['active', 'complete']
        elif data.get('state') == 'draft-complete':
            stage = ['active', 'complete', 'complete']

        # if we are creating from a group then this allows the group to be
        # set automatically
        data['group_id'] = request.params.get('group') or \
            request.params.get('groups__0__id')

        vars = {'data': data, 'errors': errors,
                'error_summary': error_summary,
                'action': 'new', 'stage': stage}
        c.errors_json = h.json.dumps(errors)

        self._setup_template_variables(context, {},
                                       package_type=package_type)

        # TODO: This check is to maintain backwards compatibility with the
        # old way of creating custom forms. This behaviour is now deprecated.
        if hasattr(self, 'package_form'):
            c.form = render(self.package_form, extra_vars=vars)
        else:
            c.form = render(self._package_form(package_type=package_type),
                            extra_vars=vars)
        return render(self._new_template(package_type),
                      extra_vars={'stage': stage})

    def resource_edit(self, id, resource_id, data=None, errors=None,
                      error_summary=None):
        if request.method == 'POST' and not data:
            data = data or clean_dict(dict_fns.unflatten(tuplize_dict(parse_params(
                request.POST))))
            # we don't want to include save as it is part of the form
            #del data['save']

            if hasattr(data, 'resource_type'):
              if (data['resource_type'] == 'vista'):
                try:
                    data['url'] = self._save_vista(data['vistas_value'], data['filtro'])
                    #data['name'] = "Vista"
                except:
                    msg = _('Debe seleccionar una vista de las disponibles u otro tipo de recurso')
                    errors = {}
                    error_summary = {_('Error'): msg}
                    abort( 500, msg)
                    #return self.new_resource(id, data, errors, error_summary)

            context = {'model': model, 'session': model.Session,
                       'api_version': 3,
                       'user': c.user or c.author}

            data['package_id'] = id
            try:
                if resource_id:
                    data['id'] = resource_id
                    get_action('resource_update')(context, data)
                else:
                    get_action('resource_create')(context, data)
            except ValidationError, e:
                errors = e.error_dict
                error_summary = e.error_summary
                return self.resource_edit(id, resource_id, data,
                                          errors, error_summary)
            except NotAuthorized:
                abort(401, _('Unauthorized to edit this resource'))
            #redirect(h.url_for(controller='package', action='resource_read',
            #                   id=id, resource_id=resource_id))

            return 'OK'

        context = {'model': model, 'session': model.Session,
                   'api_version': 3,
                   'user': c.user or c.author,}
        pkg_dict = get_action('package_show')(context, {'id': id})
        if pkg_dict['state'].startswith('draft'):
            # dataset has not yet been fully created
            resource_dict = get_action('resource_show')(context, {'id': resource_id})
            fields = ['url', 'resource_type', 'format', 'name', 'description', 'id']
            data = {}
            for field in fields:
                data[field] = resource_dict[field]
            return self.new_resource(id, data=data)
        # resource is fully created
        try:
            resource_dict = get_action('resource_show')(context, {'id': resource_id})
        except NotFound:
            abort(404, _('Resource not found'))
        c.pkg_dict = pkg_dict
        c.resource = resource_dict
        # set the form action
        c.form_action = h.url_for(controller='package',
                                  action='resource_edit',
                                  resource_id=resource_id,
                                  id=id)
        if not data:
            data = resource_dict

        errors = errors or {}
        error_summary = error_summary or {}
        vars = {'data': data, 'errors': errors,
                'error_summary': error_summary, 'action': 'new'}
        return render('package/resource_edit.html', extra_vars=vars)

    def new_resource(self, id, data=None, errors=None, error_summary=None):
        ''' FIXME: This is a temporary action to allow styling of the
        forms. '''
        if request.method == 'POST' and not data:
            save_action = request.params.get('save')
            data = data or clean_dict(dict_fns.unflatten(tuplize_dict(parse_params(
                request.POST))))
            # we don't want to include save as it is part of the form

            if (data['resource_type'] == 'vista'):
                try:
                    data['url'] = self._save_vista(data['vistas_value'], data['filtro'])
                    #data['name'] = "Vista"
                except:
                    msg = _('Debe seleccionar una vista de las disponibles u otro tipo de recurso')
                    errors = {}
                    error_summary = {_('Error'): msg}
                    abort( 500, msg)
                    #return self.new_resource(id, data, errors, error_summary)

            # CHECK IF IT WORKS!!!
            if (data['mimetype_inner'] == ''):
              data['mimetype_inner'] = h.getMimetypeFromFormat(data['format'])
            if (data['mimetype'] == ''):
              data['mimetype'] = h.getMimetypeDistributionFromFormat(data['format'])
            
            #del data['save']
            resource_id = data['id']
            del data['id']

            context = {'model': model, 'session': model.Session,
                       'user': c.user or c.author}

            # see if we have any data that we are trying to save
            data_provided = False
            for key, value in data.iteritems():
                if value and key != 'resource_type':
                    data_provided = True
                    break

            if not data_provided and save_action != "go-dataset-complete":
                if save_action == 'go-dataset':
                    # go to final stage of adddataset
                    redirect(h.url_for(controller='package',
                                       action='edit', id=id))
                # see if we have added any resources
                try:
                    data_dict = get_action('package_show')(context, {'id': id})
                except NotAuthorized:
                    abort(401, _('Unauthorized to update dataset'))
                except NotFound:
                    abort(404,
                      _('The dataset {id} could not be found.').format(id=id))
                if not len(data_dict['resources']):
                    # no data so keep on page
                    msg = _('You must add at least one data resource')
                    # On new templates do not use flash message
                    if g.legacy_templates:
                        h.flash_error(msg)
                        redirect(h.url_for(controller='package',
                                           action='new_resource', id=id))
                    else:
                        errors = {}
                        error_summary = {_('Error'): msg}
                        return self.new_resource(id, data, errors, error_summary)

                return msg
                # we have a resource so let them add metadata
                redirect(h.url_for(controller='package',
                                   action='new_metadata', id=id))

            data['package_id'] = id
            try:
                if resource_id:
                    data['id'] = resource_id
                    get_action('resource_update')(context, data)
                else:
                    response_res_create = get_action('resource_create')(context, data)
                    if (response_res_create['id']):
                      return response_res_create['id'] 
            except ValidationError, e:
                errors = e.error_dict
                error_summary = e.error_summary
                return self.new_resource(id, data, errors, error_summary)
            except NotAuthorized:
                abort(401, _('Unauthorized to create a resource'))
            except NotFound:
                abort(404,
                    _('The dataset {id} could not be found.').format(id=resource_id))

            #ignore rest of code and end now
            #it should be never reach this point
            return 'OK'

            if save_action == 'go-metadata':
                # go to final stage of add dataset
                redirect(h.url_for(controller='package',
                                   action='new_metadata', id=id))
            elif save_action == 'go-dataset':
                # go to first stage of add dataset
                redirect(h.url_for(controller='package',
                                   action='edit', id=id))
            elif save_action == 'go-dataset-complete':
                # go to first stage of add dataset
                redirect(h.url_for(controller='package',
                                   action='read', id=id))
            else:
                # add more resources
                redirect(h.url_for(controller='package',
                                   action='new_resource', id=id))
        errors = errors or {}
        error_summary = error_summary or {}
        vars = {'data': data, 'errors': errors,
                'error_summary': error_summary, 'action': 'new'}
        vars['pkg_name'] = id
        # get resources for sidebar
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author}
        try:
            pkg_dict = get_action('package_show')(context, {'id': id})
        except NotFound:
            abort(404, _('The dataset {id} could not be found.').format(id=id))
        # required for nav menu
        vars['pkg_dict'] = pkg_dict
        if pkg_dict['state'] == 'draft':
            vars['stage'] = ['complete', 'active']
        elif pkg_dict['state'] == 'draft-complete':
            vars['stage'] = ['complete', 'active', 'complete']
        return render('package/new_resource.html', extra_vars=vars)

    def new_metadata(self, id, data=None, errors=None, error_summary=None):
        ''' FIXME: This is a temporary action to allow styling of the
        forms. '''
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author}

        if request.method == 'POST' and not data:
            save_action = request.params.get('save')
            data = data or clean_dict(dict_fns.unflatten(tuplize_dict(parse_params(
                request.POST))))
            # we don't want to include save as it is part of the form
            del data['save']

            data_dict = get_action('package_show')(context, {'id': id})

            data_dict['id'] = id
            # update the state
            if save_action == 'finish':
                # we want this to go live when saved
                data_dict['state'] = 'active'
            elif save_action in ['go-resources', 'go-dataset']:
                data_dict['state'] = 'draft-complete'
            # allow the state to be changed
            context['allow_state_change'] = True
            data_dict.update(data)
            try:
                get_action('package_update')(context, data_dict)
            except ValidationError, e:
                errors = e.error_dict
                error_summary = e.error_summary
                return self.new_metadata(id, data, errors, error_summary)
            except NotAuthorized:
                abort(401, _('Unauthorized to update dataset'))
            if save_action == 'go-resources':
                # we want to go back to the add resources form stage
                redirect(h.url_for(controller='package',
                                   action='new_resource', id=id))
            elif save_action == 'go-dataset':
                # we want to go back to the add dataset stage
                redirect(h.url_for(controller='package',
                                   action='edit', id=id))

            redirect(h.url_for(controller='package', action='read', id=id))

        if not data:
            data = get_action('package_show')(context, {'id': id})
        errors = errors or {}
        error_summary = error_summary or {}
        vars = {'data': data, 'errors': errors, 'error_summary': error_summary}
        vars['pkg_name'] = id

        package_type = self._get_package_type(id)
        self._setup_template_variables(context, {},
                                       package_type=package_type)

        return render('package/new_package_metadata.html', extra_vars=vars)

    def edit(self, id, data=None, errors=None, error_summary=None):
        package_type = self._get_package_type(id)
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author,
                   'save': 'save' in request.params,
                   'moderated': config.get('moderated'),
                   'pending': True}

        if context['save'] and not data:
            return self._save_edit(id, context, package_type=package_type)
        try:
            c.pkg_dict = get_action('package_show')(context, {'id': id})
            context['for_edit'] = True
            old_data = get_action('package_show')(context, {'id': id})
            # old data is from the database and data is passed from the
            # user if there is a validation error. Use users data if there.
            if data:
                old_data.update(data)
            data = old_data
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % '')
        except NotFound:
            abort(404, _('Dataset not found'))
        # are we doing a multiphase add?
        if data.get('state', '').startswith('draft'):
            c.form_action = h.url_for(controller='package', action='new')
            c.form_style = 'new'
            return self.new(data=data, errors=errors,
                            error_summary=error_summary)

        c.pkg = context.get("package")
        c.resources_json = h.json.dumps(data.get('resources', []))

        try:
            check_access('package_update', context)
        except NotAuthorized, e:
            abort(401, _('User %r not authorized to edit %s') % (c.user, id))
        # convert tags if not supplied in data
        if data and not data.get('tag_string'):
            data['tag_string'] = ', '.join(h.dict_list_reduce(
                c.pkg_dict.get('tags', {}), 'name'))
        errors = errors or {}
        vars = {'data': data, 'errors': errors,
                'error_summary': error_summary, 'action': 'edit'}
        c.errors_json = h.json.dumps(errors)

        self._setup_template_variables(context, {'id': id},
                                       package_type=package_type)
        c.related_count = c.pkg.related_count

        # we have already completed stage 1
        vars['stage'] = ['active']
        if data.get('state') == 'draft':
            vars['stage'] = ['active', 'complete']
        elif data.get('state') == 'draft-complete':
            vars['stage'] = ['active', 'complete', 'complete']

        # TODO: This check is to maintain backwards compatibility with the
        # old way of creating custom forms. This behaviour is now deprecated.
        if hasattr(self, 'package_form'):
            c.form = render(self.package_form, extra_vars=vars)
        else:
            c.form = render(self._package_form(package_type=package_type),
                            extra_vars=vars)

        return render(self._edit_template(package_type),
                      extra_vars={'stage': vars['stage']})

    def read_ajax(self, id, revision=None):
        package_type = self._get_package_type(id)
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author,
                   'revision_id': revision}
        try:
            data = get_action('package_show')(context, {'id': id})
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % '')
        except NotFound:
            abort(404, _('Dataset not found'))

        data.pop('tags')
        data = flatten_to_string_key(data)
        response.headers['Content-Type'] = 'application/json;charset=utf-8'
        return h.json.dumps(data)

    def history_ajax(self, id):

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author}
        data_dict = {'id': id}
        try:
            pkg_revisions = get_action('package_revision_list')(
                context, data_dict)
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % '')
        except NotFound:
            abort(404, _('Dataset not found'))

        data = []
        approved = False
        for num, revision in enumerate(pkg_revisions):
            if not approved and revision['approved_timestamp']:
                current_approved, approved = True, True
            else:
                current_approved = False

            data.append({'revision_id': revision['id'],
                         'message': revision['message'],
                         'timestamp': revision['timestamp'],
                         'author': revision['author'],
                         'approved': bool(revision['approved_timestamp']),
                         'current_approved': current_approved})

        response.headers['Content-Type'] = 'application/json;charset=utf-8'
        return h.json.dumps(data)

    def _get_package_type(self, id):
        """
        Given the id of a package it determines the plugin to load
        based on the package's type name (type). The plugin found
        will be returned, or None if there is no plugin associated with
        the type.
        """
        pkg = model.Package.get(id)
        if pkg:
            return pkg.type or 'dataset'
        return None

    def _tag_string_to_list(self, tag_string):
        ''' This is used to change tags from a sting to a list of dicts '''
        out = []
        for tag in tag_string.split(','):
            tag = tag.strip()
            if tag:
                out.append({'name': tag,
                            'state': 'active'})
        return out

    def _save_new(self, context, package_type=None):
        # The staged add dataset used the new functionality when the dataset is
        # partially created so we need to know if we actually are updating or
        # this is a real new.
        is_an_update = False
        ckan_phase = request.params.get('_ckan_phase')
        from ckan.lib.search import SearchIndexError
        try:
            data_dict = clean_dict(dict_fns.unflatten(
                tuplize_dict(parse_params(request.POST))))
            if ckan_phase:
                # prevent clearing of groups etc
                context['allow_partial_update'] = True
                # sort the tags
                data_dict['tags'] = self._tag_string_to_list(
                    data_dict['tag_string'])
                if data_dict.get('pkg_name'):
                    is_an_update = True
                    # This is actually an update not a save
                    data_dict['id'] = data_dict['pkg_name']
                    del data_dict['pkg_name']
                    # this is actually an edit not a save
                    pkg_dict = get_action('package_update')(context, data_dict)

                    if request.params['save'] == 'go-metadata':
                        # redirect to add metadata
                        url = h.url_for(controller='package',
                                        action='new_metadata',
                                        id=pkg_dict['name'])
                    else:
                        # redirect to add dataset resources
                        url = h.url_for(controller='package',
                                        action='new_resource',
                                        id=pkg_dict['name'])
                    redirect(url)
                # Make sure we don't index this dataset
                if request.params['save'] not in ['go-resource', 'go-metadata']:
                    data_dict['state'] = 'draft'
                # allow the state to be changed
                context['allow_state_change'] = True

            data_dict['type'] = package_type
            context['message'] = data_dict.get('log_message', '')
            pkg_dict = get_action('package_create')(context, data_dict)

            if ckan_phase:
                # redirect to add dataset resources
                url = h.url_for(controller='package',
                                action='new_resource',
                                id=pkg_dict['name'])
                redirect(url)

            self._form_save_redirect(pkg_dict['name'], 'new', package_type=package_type)
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % '')
        except NotFound, e:
            abort(404, _('Dataset not found'))
        except dict_fns.DataError:
            abort(400, _(u'Integrity Error'))
        except SearchIndexError, e:
            try:
                exc_str = unicode(repr(e.args))
            except Exception:  # We don't like bare excepts
                exc_str = unicode(str(e))
            abort(500, _(u'Unable to add package to search index.') + exc_str)
        except ValidationError, e:
            errors = e.error_dict
            error_summary = e.error_summary
            if is_an_update:
                # we need to get the state of the dataset to show the stage we
                # are on.
                pkg_dict = get_action('package_show')(context, data_dict)
                data_dict['state'] = pkg_dict['state']
                return self.edit(data_dict['id'], data_dict,
                                 errors, error_summary)
            data_dict['state'] = 'none'
            return self.new(data_dict, errors, error_summary)

    def _save_edit(self, name_or_id, context, package_type=None):
        from ckan.lib.search import SearchIndexError
        log.debug('Package save request name: %s POST: %r',
                  name_or_id, request.POST)
        try:
            data_dict = clean_dict(dict_fns.unflatten(
                tuplize_dict(parse_params(request.POST))))
            #if '_ckan_phase' in data_dict:
                # we allow partial updates to not destroy existing resources
                #context['allow_partial_update'] = True
                #data_dict['tags'] = self._tag_string_to_list(
                    #data_dict['tag_string'])
                #del data_dict['_ckan_phase']
                #del data_dict['save']
                
            context['allow_partial_update'] = True
            data_dict['tags'] = self._tag_string_to_list(
                    data_dict['tag_string'])
            context['message'] = data_dict.get('log_message', '')
            if not context['moderated']:
                context['pending'] = False
            data_dict['id'] = name_or_id
            pkg = get_action('package_update')(context, data_dict)
            if request.params.get('save', '') == 'Approve':
                get_action('make_latest_pending_package_active')(
                    context, data_dict)
            c.pkg = context['package']
            c.pkg_dict = pkg

            if 'customEditor' in request.params:
              # we don't need all this stuff
              return 'OK'

            self._form_save_redirect(pkg['name'], 'edit', package_type=package_type)
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)
        except NotFound, e:
            abort(404, _('Dataset not found'))
        except dict_fns.DataError:
            abort(400, _(u'Integrity Error'))
        except SearchIndexError, e:
            try:
                exc_str = unicode(repr(e.args))
            except Exception:  # We don't like bare excepts
                exc_str = unicode(str(e))
            abort(500, _(u'Unable to update search index.') + exc_str)
        except ValidationError, e:
            errors = e.error_dict
            error_summary = e.error_summary
            return self.edit(name_or_id, data_dict, errors, error_summary)

    def _form_save_redirect(self, pkgname, action, package_type=None):
        '''This redirects the user to the CKAN package/read page,
        unless there is request parameter giving an alternate location,
        perhaps an external website.
        @param pkgname - Name of the package just edited
        @param action - What the action of the edit was
        '''
        assert action in ('new', 'edit')
        url = request.params.get('return_to') or \
            config.get('package_%s_return_url' % action)
        if url:
            url = url.replace('<NAME>', pkgname)
        else:
            if package_type is None or package_type == 'catalogo':
                url = h.url_for(controller='package', action='read', id=pkgname)
            else:
                url = h.url_for('{0}_read'.format(package_type), id=pkgname)
        redirect(url)

    def _adjust_license_id_options(self, pkg, fs):
        options = fs.license_id.render_opts['options']
        is_included = False
        for option in options:
            license_id = option[1]
            if license_id == pkg.license_id:
                is_included = True
        if not is_included:
            options.insert(1, (pkg.license_id, pkg.license_id))

    def delete(self, id):

        if 'cancel' in request.params:
            h.redirect_to(controller='package', action='edit', id=id)

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author}

        try:
            check_access('package_delete', context, {'id': id})
        except NotAuthorized:
            abort(401, _('Unauthorized to delete package %s') % '')

        try:
            if request.method == 'POST':
                get_action('package_delete')(context, {'id': id})
                h.flash_notice(_('Dataset has been deleted.'))
                h.redirect_to(controller='package', action='search')
            c.pkg_dict = get_action('package_show')(context, {'id': id})
        except NotAuthorized:
            abort(401, _('Unauthorized to delete package %s') % '')
        except NotFound:
            abort(404, _('Dataset not found'))
        return render('package/confirm_delete.html')

    def resource_delete(self, id, resource_id):

        if 'cancel' in request.params:
            h.redirect_to(controller='package', action='resource_edit', resource_id=resource_id, id=id)

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author}

        try:
            check_access('package_delete', context, {'id': id})
        except NotAuthorized:
            abort(401, _('Unauthorized to delete package %s') % '')

        try:
            if request.method == 'POST':
                get_action('resource_delete')(context, {'id': resource_id})
                #h.flash_notice(_('Resource has been deleted.'))
                #h.redirect_to(controller='package', action='read', id=id)
                return 'Resource has been deleted.'
            c.resource_dict = get_action('resource_show')(context, {'id': resource_id})
            c.pkg_id = id
        except NotAuthorized:
            abort(401, _('Unauthorized to delete resource %s') % '')
        except NotFound:
            abort(404, _('Resource not found'))
        #return render('package/confirm_delete_resource.html')

    def autocomplete(self):
        # DEPRECATED in favour of /api/2/util/dataset/autocomplete
        q = unicode(request.params.get('q', ''))
        if not len(q):
            return ''

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author}

        data_dict = {'q': q}
        packages = get_action('package_autocomplete')(context, data_dict)

        pkg_list = []
        for pkg in packages:
            pkg_list.append('%s|%s' % (pkg['match_displayed'].
                                       replace('|', ' '), pkg['name']))
        return '\n'.join(pkg_list)

    def _render_edit_form(self, fs, params={}, clear_session=False):
        # errors arrive in c.error and fs.errors
        c.log_message = params.get('log_message', '')
        # rgrp: expunge everything from session before dealing with
        # validation errors) so we don't have any problematic saves
        # when the fs.render causes a flush.
        # seb: If the session is *expunged*, then the form can't be
        # rendered; I've settled with a rollback for now, which isn't
        # necessarily what's wanted here.
        # dread: I think this only happened with tags because until
        # this changeset, Tag objects were created in the Renderer
        # every time you hit preview. So I don't believe we need to
        # clear the session any more. Just in case I'm leaving it in
        # with the log comments to find out.
        if clear_session:
            # log to see if clearing the session is ever required
            if model.Session.new or model.Session.dirty or \
                    model.Session.deleted:
                log.warn('Expunging session changes which were not expected: '
                         '%r %r %r', (model.Session.new, model.Session.dirty,
                                      model.Session.deleted))
            try:
                model.Session.rollback()
            except AttributeError:
                # older SQLAlchemy versions
                model.Session.clear()
        edit_form_html = fs.render()
        c.form = h.literal(edit_form_html)
        return h.literal(render('package/edit_form.html'))

    def _update_authz(self, fs):
        validation = fs.validate()
        if not validation:
            c.form = self._render_edit_form(fs, request.params)
            raise package_saver.ValidationException(fs)
        try:
            fs.sync()
        except Exception, inst:
            model.Session.rollback()
            raise
        else:
            model.Session.commit()

    def resource_read(self, id, resource_id):
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author}

        try:
            c.resource = get_action('resource_show')(context,
                                                     {'id': resource_id})
            c.package = get_action('package_show')(context, {'id': id})
            # required for nav menu
            c.pkg = context['package']
            c.pkg_dict = c.package
        except NotFound:
            abort(404, _('Resource not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read resource %s') % id)
        # get package license info
        license_id = c.package.get('license_id')
        try:
            c.package['isopen'] = model.Package.\
                get_license_register()[license_id].isopen()
        except KeyError:
            c.package['isopen'] = False

        # TODO: find a nicer way of doing this
        c.datastore_api = '%s/api/action' % config.get('ckan.site_url', '').rstrip('/')

        c.related_count = c.pkg.related_count

        c.resource['can_be_previewed'] = self._resource_preview(
            {'resource': c.resource, 'package': c.package})
        return render('package/resource_read.html')

    def _resource_preview(self, data_dict):
        return bool(datapreview.res_format(data_dict['resource'])
                    in datapreview.direct() + datapreview.loadable()
                    or datapreview.get_preview_plugin(
                        data_dict, return_first=True))

    def resource_download(self, id, resource_id):
        """
        Provides a direct download by redirecting the user to the url stored
        against this resource.
        """
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author}

        try:
            rsc = get_action('resource_show')(context, {'id': resource_id})
            pkg = get_action('package_show')(context, {'id': id})
        except NotFound:
            abort(404, _('Resource not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read resource %s') % id)

        if not 'url' in rsc:
            abort(404, _('No download is available'))
        redirect(rsc['url'])

    def follow(self, id):
        '''Start following this dataset.'''
        context = {'model': model,
                   'session': model.Session,
                   'user': c.user or c.author}
        data_dict = {'id': id}
        try:
            get_action('follow_dataset')(context, data_dict)
            package_dict = get_action('package_show')(context, data_dict)
            h.flash_success(_("You are now following {0}").format(
                package_dict['title']))
        except ValidationError as e:
            error_message = (e.extra_msg or e.message or e.error_summary
                    or e.error_dict)
            h.flash_error(error_message)
        except NotAuthorized as e:
            h.flash_error(e.extra_msg)
        h.redirect_to(controller='package', action='read', id=id)

    def unfollow(self, id):
        '''Stop following this dataset.'''
        context = {'model': model,
                   'session': model.Session,
                   'user': c.user or c.author}
        data_dict = {'id': id}
        try:
            get_action('unfollow_dataset')(context, data_dict)
            package_dict = get_action('package_show')(context, data_dict)
            h.flash_success(_("You are no longer following {0}").format(
                package_dict['title']))
        except ValidationError as e:
            error_message = (e.extra_msg or e.message or e.error_summary
                    or e.error_dict)
            h.flash_error(error_message)
        except (NotFound, NotAuthorized) as e:
            error_message = e.extra_msg or e.message
            h.flash_error(error_message)
        h.redirect_to(controller='package', action='read', id=id)

    def followers(self, id=None):
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True}
        data_dict = {'id': id}
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
            c.followers = get_action('dataset_follower_list')(context,
                    {'id': c.pkg_dict['id']})

            c.related_count = c.pkg.related_count
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read package %s') % id)

        return render('package/followers.html')

    def activity(self, id):
        '''Render this package's public activity stream page.'''

        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True}
        data_dict = {'id': id}
        try:
            c.pkg_dict = get_action('package_show')(context, data_dict)
            c.pkg = context['package']
            c.package_activity_stream = get_action(
                    'package_activity_list_html')(context,
                            {'id': c.pkg_dict['id']})
            c.related_count = c.pkg.related_count
        except NotFound:
            abort(404, _('Dataset not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read dataset %s') % id)

        return render('package/activity.html')

    def resource_embedded_dataviewer(self, id, resource_id,
                                     width=500, height=500):
        """
        Embeded page for a read-only resource dataview. Allows
        for width and height to be specified as part of the
        querystring (as well as accepting them via routes).
        """
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author}

        try:
            c.resource = get_action('resource_show')(context,
                                                     {'id': resource_id})
            c.package = get_action('package_show')(context, {'id': id})
            c.resource_json = h.json.dumps(c.resource)

            # double check that the resource belongs to the specified package
            if not c.resource['id'] in [r['id']
                                        for r in c.package['resources']]:
                raise NotFound

        except NotFound:
            abort(404, _('Resource not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read resource %s') % id)

        # Construct the recline state
        state_version = int(request.params.get('state_version', '1'))
        recline_state = self._parse_recline_state(request.params)
        if recline_state is None:
            abort(400, ('"state" parameter must be a valid recline '
                        'state (version %d)' % state_version))

        c.recline_state = h.json.dumps(recline_state)

        c.width = max(int(request.params.get('width', width)), 100)
        c.height = max(int(request.params.get('height', height)), 100)
        c.embedded = True

        return render('package/resource_embedded_dataviewer.html')

    def _parse_recline_state(self, params):
        state_version = int(request.params.get('state_version', '1'))
        if state_version != 1:
            return None

        recline_state = {}
        for k, v in request.params.items():
            try:
                v = h.json.loads(v)
            except ValueError:
                pass
            recline_state[k] = v

        recline_state.pop('width', None)
        recline_state.pop('height', None)
        recline_state['readOnly'] = True

        # previous versions of recline setup used elasticsearch_url attribute
        # for data api url - see http://trac.ckan.org/ticket/2639
        # fix by relocating this to url attribute which is the default location
        if 'dataset' in recline_state and 'elasticsearch_url' in recline_state['dataset']:
            recline_state['dataset']['url'] = recline_state['dataset']['elasticsearch_url']

        # Ensure only the currentView is available
        # default to grid view if none specified
        if not recline_state.get('currentView', None):
            recline_state['currentView'] = 'grid'
        for k in recline_state.keys():
            if k.startswith('view-') and \
                    not k.endswith(recline_state['currentView']):
                recline_state.pop(k)
        return recline_state

    def resource_datapreview(self, id, resource_id):
        '''
        Embeded page for a resource data-preview.

        Depending on the type, different previews are loaded.  This could be an
        img tag where the image is loaded directly or an iframe that embeds a
        webpage, recline or a pdf preview.
        '''
        context = {
            'model': model,
            'session': model.Session,
            'user': c.user or c.author
        }

        try:
            c.resource = get_action('resource_show')(context,
                                                     {'id': resource_id})
            c.package = get_action('package_show')(context, {'id': id})

            data_dict = {'resource': c.resource, 'package': c.package}

            preview_plugin = datapreview.get_preview_plugin(data_dict)

            if preview_plugin is None:
                abort(409, _('No preview has been defined.'))

            preview_plugin.setup_template_variables(context, data_dict)
            c.resource_json = json.dumps(c.resource)
        except NotFound:
            abort(404, _('Resource not found'))
        except NotAuthorized:
            abort(401, _('Unauthorized to read resource %s') % id)
        else:
            return render(preview_plugin.preview_template(context, data_dict))

    def metadata_catalog(self):
        ctype, extension, loader = self._content_type_from_extension('rdf')
        response.headers['Content-Type'] = ctype

        fq = ' +dataset_type:dataset'

        try:
            context = {'model': model, 'user': c.user or c.author}
            check_access('site_read', context)
        except NotAuthorized:
            abort(401, _('Not authorized to see this page'))

        q = c.q = request.params.get('q', u'')

#		c.fecha = datetime.datetime.now().isoformat()
        c.fecha = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        data_dict = {
                'q': q,
                'fq': fq.strip(),
                'rows': 999999,
                'sort': 'metadata_modified desc',
                'start': 0
        }

        query = get_action('package_search')(context, data_dict)
        c.pkg = query['results']

        return render('package/catalogo.rdf', loader_class=loader)

    def federador_catalog(self):
        ctype, extension, loader = self._content_type_from_extension('rdf')
        response.headers['Content-Type'] = ctype

        fq = ' +dataset_type:dataset'

        try:
            context = {'model': model, 'user': c.user or c.author}
            check_access('site_read', context)
        except NotAuthorized:
            abort(401, _('Not authorized to see this page'))

        q = c.q = request.params.get('q', u'')

#		c.fecha = datetime.datetime.now().isoformat()
        c.fecha = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        c.urlenco = urllib.quote

        data_dict = {
                'q': q,
                'fq': fq.strip(),
                'rows': 999999,
                'sort': 'metadata_modified desc',
                'start': 0
        }

        query = get_action('package_search')(context, data_dict)
        c.pkg = query['results']

        return render('package/federador.rdf', loader_class=loader)


    def homer_catalog(self):
        ctype, extension, loader = self._content_type_from_extension('rdf')
        response.headers['Content-Type'] = ctype

        context = {'model': model, 'user': c.user or c.author}
        check_access('site_read', context)

        q = c.q = request.params.get('q', u'')

        data_dict = {
               'q': q,
                'rows': 999999,  #no importa, siempre da un maximo
                'start': 0
        }

        query = get_action('package_search')(context, data_dict)
        c.pkg = query['results']
        return render('package/catalogoHOMER.xml', loader_class=loader)

   
    #Esta función se le mete un tipo y devuelve la consulta referente a ese tipo
    def _consultaSOLR(self, tipo):
        consulta =''
        if tipo == 'calendario':
             consulta = "(res_format:ICS || res_format:ics) && dataset_type:dataset && entity_type:package && state:active && capacity:public"
        elif tipo == 'fotos':
             consulta = "(res_format:jpeg || res_format:JPEG || res_format:jpg || res_format:JPG || res_format:png || res_format:PNG || res_format:gif || res_format:GIF ) && dataset_type:dataset && entity_type:package && state:active && capacity:public" 
        elif tipo == 'hojas-de-calculo':
             consulta = "(res_format:XLS || res_format:xls || res_format:ods || res_format:ODS || res_format:xlsx || res_format:XLSX) && dataset_type:dataset && entity_type:package && state:active && capacity:public"
        elif tipo == 'mapas':
             consulta = "(res_format:dxf || res_format:DXF || res_format:gml || res_format:GML || res_format:geojson || res_format:GEOJSON || res_format:kmz || res_format:KMZ || res_format:shp || res_format:SHP || res_format:dgn || res_format:DGN || res_format:dwg || res_format:DWG ) && dataset_type:dataset && entity_type:package && state:active && capacity:public"
        elif tipo == 'recursos-educativos':
             consulta ="(name:recurso-educativo*) && dataset_type:dataset && entity_type:package && state:active && capacity:public"
        elif tipo == 'recursos-web':
             consulta ="(res_format:html || res_format:HTML || res_format:url || res_format:URL) && dataset_type:dataset && entity_type:package && state:active && capacity:public"
        elif tipo == 'rss':
             consulta = "(res_format:rss || res_format:RSS) && dataset_type:dataset && entity_type:package && state:active && capacity:public"
        elif tipo == 'texto-plano':
             consulta = "(((res_format:XLS || res_format:xls ) && (res_url:http*.xls )) || res_format:json || res_format:JSON || res_format:xml || res_format:XML || res_format:csv || res_format:CSV || res_format:px || res_format:PX || res_format:url || res_format:URL) && dataset_type:dataset && entity_type:package && state:active && capacity:public"
        return consulta
    
    
    
    def searchAOD(self, tema=None, tipo=None, subtipo=None, temaEstadistico=None, temaBBDD=None, queryLibre=None, organizacion=None, tipoDataset=None):
        from ckan.lib.search import SearchError

        #package_type = self._guess_package_type()
        package_type = 'catalogo'
        

        try:
            context = {'model': model, 'user': c.user or c.author}
            check_access('site_read', context)
        except NotAuthorized:
            abort(401, _('Not authorized to see this page'))

        # unicode format (decoded from utf8)
        #q = c.q = request.params.get('q', u'')

        auxq = None
        if tema is not None:
                 auxq = "groups:%s " % tema

        if temaEstadistico is not None:
             if auxq  is not None:
                 auxq += " && 01_IAEST_Temaestadstico:%s*" % temaEstadistico
             else:
                 auxq = "01_IAEST_Temaestadstico:%s* " % temaEstadistico

#		if author is not None:
#			 if auxq  is not None:
#				 auxq += " && author:%s" % author
#			 else:
#				 auxq = "author:%s " % author

        # tabla si tiene CSV y XLS
        # arboles de datos: JSON y XLS
        # Mapa: formato GIS
        # Fotos: jpg
        # RSS: RSS
        # Info estadistica: publicador IAEst
        qTipo = None
        if tipo is not None:
             if (tipo == 'calendario') | (tipo == 'fotos') | (tipo == 'hojas-de-calculo') | (tipo == 'mapas') | (tipo == 'recursos-educativos') | (tipo == 'recursos-web') | (tipo == 'rss') | (tipo == 'texto-plano'):
                 qTipo = self._consultaSOLR(tipo)
             elif tipo == 'informacion-estadistica':
                 qTipo = "organization:instituto-aragones-estadistica"
             elif tipo == 'base-datos':
                 qTipo = "extras_Frequency:Instantanea"
             elif tipo == 'busqueda-libre':
                 if queryLibre is None:
                     qtipo = "*:*"
                 else:
                     qTipo = "%s" % queryLibre
             elif tipo == 'busqueda-organizacion':
                 if organizacion is None:
                     qTipo = "*:*"
                 else:
                     #print "La organizacion es ", organizacion
                     qTipo = "organization:%s" % organizacion
                     if tipoDataset is not None:
                         #print "el tipoDataset es ", tipoDataset
                         qTipo+=" && ("+self._consultaSOLR(tipoDataset)+")"

        if auxq is not None:
             if qTipo is not None:
                 auxq += " && (" + qTipo + ") "
        else:
             auxq = qTipo

        if temaBBDD is not None:
             auxq += " && groups:%s" % temaBBDD
            
        if subtipo is not None:
             if auxq  is not None:
                 auxq += " && author:%s" % subtipo
             else:
                 auxq = "author:%s" % subtipo

        q = c.q = auxq
        log.error('La consulta en SolRal final: %s', q)
        #print 'La consulta de solr final es ', auxq

        c.query_error = False
        try:
            page = int(request.params.get('page', 1))
        except ValueError, e:
            abort(400, ('"page" parameter must be an integer'))
        limit = g.datasets_per_page

        # most search operations should reset the page counter:
        params_nopage = [(k, v) for k, v in request.params.items()
                         if k != 'page']

        def drill_down_url(alternative_url=None, **by):
            return h.add_url_param(alternative_url=alternative_url,
                                   controller='package', action='search',
                                   new_params=by)

        c.drill_down_url = drill_down_url

        def remove_field(key, value=None, replace=None):
            return h.remove_url_param(key, value=value, replace=replace,
                                  controller='package', action='search')

        c.remove_field = remove_field

        sort_by = request.params.get('sort', None)
        params_nosort = [(k, v) for k, v in params_nopage if k != 'sort']

        def _sort_by(fields):
            """
            Sort by the given list of fields.

            Each entry in the list is a 2-tuple: (fieldname, sort_order)

            eg - [('metadata_modified', 'desc'), ('name', 'asc')]

            If fields is empty, then the default ordering is used.
            """
            params = params_nosort[:]

            if fields:
                sort_string = ', '.join('%s %s' % f for f in fields)
                params.append(('sort', sort_string))
            #return search_url(params, package_type)
            return search_url(params, 'catalogoAOD')

        c.sort_by = _sort_by
        if sort_by is None:
            c.sort_by_fields = []
        else:
            c.sort_by_fields = [field.split()[0]
                                for field in sort_by.split(',')]

        def pager_url(q=None, page=None):
            params = list(params_nopage)
            params.append(('page', page))
            #return search_url(params, package_type)
            return search_url(params, 'catalogoAOD')

        c.search_url_params = urlencode(_encode_params(params_nopage))

        try:
            c.fields = []
            # c.fields_grouped will contain a dict of params containing
            # a list of values eg {'tags':['tag1', 'tag2']}
            c.fields_grouped = {}
            search_extras = {}
            fq = ''
            for (param, value) in request.params.items():
                if param not in ['q', 'page', 'sort'] \
                        and len(value) and not param.startswith('_'):
                    if not param.startswith('ext_'):
                        c.fields.append((param, value))
                        fq += ' %s:"%s"' % (param, value)
                        if param not in c.fields_grouped:
                            c.fields_grouped[param] = [value]
                        else:
                            c.fields_grouped[param].append(value)
                    else:
                        search_extras[param] = value

            context = {'model': model, 'session': model.Session,
                       'user': c.user or c.author, 'for_view': True}

#			if package_type and package_type != 'catalogo':
#				# Only show datasets of this particular type
#				fq += ' +dataset_type:{type}'.format(type=package_type)
#			else:
#				# Unless changed via config options, don't show non standard
#				# dataset types on the default search page
#				if not asbool(config.get('ckan.search.show_all_types', 'False')):
#					fq += ' +dataset_type:dataset'

            facets = OrderedDict()

            default_facet_titles = {
                    'organization': _('Organizations'),
                    'groups': _('Groups'),
                    'tags': _('Tags'),
                    'res_format': _('Formats'),
                    'license_id': _('License'),
                    }

            for facet in g.facets:
                if facet in default_facet_titles:
                    facets[facet] = default_facet_titles[facet]
                else:
                    facets[facet] = facet

            # Facet titles
            for plugin in p.PluginImplementations(p.IFacets):
                facets = plugin.dataset_facets(facets, package_type)

            c.facet_titles = facets

            fq = ' +dataset_type:dataset'

            data_dict = {
                'q': q,
                'fq': fq.strip(),
                'facet.field': facets.keys(),
                'rows': limit,
                'start': (page - 1) * limit,
                'sort': sort_by,
                'extras': search_extras
            }

            query = get_action('package_search')(context, data_dict)
            c.sort_by_selected = query['sort']

            c.page = h.Page(
                collection=query['results'],
                page=page,
                url=pager_url,
                item_count=query['count'],
                items_per_page=limit
            )
            
#            print 'El c.page es '+str(c.page)
#            print 'La url es '+str(pager_url)
            c.facets = query['facets']
            c.search_facets = query['search_facets']
            c.page.items = query['results']
        except SearchError, se:
            log.error('Dataset search error: %r', se.args)
            c.query_error = True
            c.facets = {}
            c.search_facets = {}
            c.page = h.Page(collection=[])
        c.search_facets_limits = {}
        for facet in c.search_facets.keys():
            limit = int(request.params.get('_%s_limit' % facet,
                                           g.facets_default_number))
            c.search_facets_limits[facet] = limit

        maintain.deprecate_context_item(
          'facets',
          'Use `c.search_facets` instead.')

        self._setup_template_variables(context, {},
                                       package_type=package_type)

        return render(self._search_template(package_type))

    def searchHOMER(self):
        return render('package/search_homer.html')

    def detallesHOMER(self, id):
        return render('package/detalles_homer.html')

    def show_index(self, format):
        """ Create a {format} file with all datasets info """
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author, 'for_view': True}
        data_dict = {
            'rows': 1000
        }
        data = get_action('package_search')(context, data_dict)
#        print len(data['results'])
        if format == 'json':
            c.content_to_render = self._create_json_index(data)
        elif format == 'xml':
            c.content_to_render = self._create_xml_index(data)
        elif format == 'csv':
            c.content_to_render = self._create_csv_index(data)

        return render('package/resource_render.html', loader_class=NewTextTemplate)

    #Función en la que teniendo el name da las recomendaciones ha ese titulo
    def getRecomendedPackages(self, packge_name):
        from ckan.lib.search import SearchError
        solr_query=packge_name.replace('-', ' ')
#        log.error('Se va a buscar '+packge_name)

        try:
            c.fields = []
            # c.fields_grouped will contain a dict of params containing
            # a list of values eg {'tags':['tag1', 'tag2']}
            c.fields_grouped = {}
            search_extras = {}
            fq = ''
            context = {    'model': model, 'session': model.Session,
                                    'user': c.user or c.author, 'for_view': True}
        
            facets = OrderedDict()

            default_facet_titles = {
                'organization': _('Organizations'),
                'groups': _('Groups'),
                'tags': _('Tags'),
                'res_format': _('Formats'),
                'license_id': _('License'),
            }
    
    
            sort_by = request.params.get('sort', None)
            
            
            
            
            q = c.q = solr_query
#            log.error('######La consulta en SolR al principio: %s', q)
            data_dict = {
                'q': q,
                'fq': fq.strip(),
                'rows': 4,
                'sort': sort_by,
                'start': 0 #Ya que 0 es el propio
            }
            
#            print 'La consulta es '+str(q)
            query = get_action('package_search')(context, data_dict)
            
#            print 'query ees '+str(len(query['results']))
#            print 'la query es '+str(query)
            
            i=0
	    ubicacion=0
            for asd in query['results']:
                 if asd['name'] == packge_name:
                     ubicacion = i
                 i=i+1
            
            package_a_sacar = query['results'].pop(ubicacion)
            
#            print 'El package a sacar es '+package_a_sacar['name']
            query['count'] = query['count'] -1
#            print 'la consulta es '+str(query);
#            c.sort_by_selected = query['sort']
    
            
            
            
            
            try:
                page = int(request.params.get('page', 1))
            except ValueError, e:
                abort(400, ('"page" parameter must be an integer'))
            
            params_nopage = [(k, v) for k, v in request.params.items()
                         if k != 'page']
            
            def pager_url(q=None, page=None):
                params = list(params_nopage)
                params.append(('page', page))
                return search_url(params, 'recomendPackage')
            
            limit = g.datasets_per_page
            print 'El limite es '+str(limit)
            print ' la url del pager'+str(pager_url)
            
            
            
            
            c.page = h.Page(
                collection=query['results'],
                page=page,
                url=pager_url,
                item_count=query['count'],
                items_per_page=limit
            )
            c.facets = query['facets']
            c.search_facets = query['search_facets']
#            c.page.items = query['results']
            
            
            
            print 'Se encuentran '+str(len(c.page.items))
            print 'Las recoemndadiones son:'
            for item in c.page.items:
                print 'EL dataset es '+str(item['name'])
        except SearchError, se:
#            log.error('Error a la hora de obtener los dataset recomendados: %r', se.args)
            c.query_error = True
            c.facets = {}
            c.search_facets = {}
            c.page = h.Page(collection=[])
        
        c.search_facets_limits = {}
        for facet in c.search_facets.keys():
            limit = int(request.params.get('_%s_limit' % facet, g.facets_default_number))
            c.search_facets_limits[facet] = limit

        maintain.deprecate_context_item(
            'facets',
            'Use `c.search_facets` instead.')
        
        package_type='recomendPackage'
        
        self._setup_template_variables(context, {}, package_type=package_type)
    
        return render(self._search_template(package_type))


    def data_resource(self, dataset, formato, version=None):
        """ Filter to resource rendering or download
                If resource doesn't exist, but a file with same name
                in XLS format does, it should be transformed to
                the required format (XML, JSON or CSV).
                Idem for Aragopedia resources
            """
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author}

        fq = ' +dataset_type:dataset'
        q = 'name:' + dataset

        data_dict = {
                'q': q,
                'fq': fq.strip()
        }

        try:
            dataset_rsc = get_action('package_search')(context, data_dict)
            xlsAuto = {'csv', 'xml', 'json'}
            urlAuto = {'csv', 'xml', 'json', 'ttl'}
            for res in dataset_rsc['results']:
              for resource in res['resources']:
                if resource.get('format').lower() == formato.lower():
                  if version is None:
                    return redirect(resource.get('url'))
                  else:
                    if resource.get(formato.upper() + '_position') ==  version:
                      return redirect(resource.get('url'))

                if resource.get('format').lower() == 'xls' and formato.lower() in xlsAuto:
                  if version is None:
#                    return redirect(c.urlenco(unicode('http://opendata.aragon.es/catalogo/render/resource/' + resource.get('name') + '.' + formato).encode('utf8'), ':?=/&amp;%'))
                    return redirect(unicode('http://opendata.aragon.es/catalogo/render/resource/' + resource.get('name') + '.' + formato).encode('utf8'))
                  else:
                    if resource.get(formato.upper() + '_position') ==  version:
#                      return redirect(c.urlenco(unicode('http://opendata.aragon.es/catalogo/render/resource/' + resource.get('name') + '.' + formato).encode('utf8'), ':?=/&amp;%'))
                      return redirect(unicode('http://opendata.aragon.es/catalogo/render/resource/' + resource.get('name') + '.' + formato).encode('utf8'))

                if resource.get('format').lower() == 'url' and formato.lower() in urlAuto:
                  if version is None:
#                    return redirect(c.urlenco(unicode((rsc_dict['url'].split("?"))[0]+  '.ttl?api_key=e103dc13eb276ad734e680f5855f20c6&amp;_view=completa').encode('utf8'), ':?=/&amp;%'))
                    return redirect(unicode((resource['url'].split("?"))[0]+  '.ttl?api_key=e103dc13eb276ad734e680f5855f20c6&_view=completa').encode('utf8'))
                  else:
                    if resource.get(formato.upper() + '_position') ==  version:
#                     return redirect(c.urlenco(unicode((rsc_dict['url'].split("?"))[0]+  '.ttl?api_key=e103dc13eb276ad734e680f5855f20c6&amp;_view=completa').encode('utf8'), ':?=/&amp;%'))
                      return redirect(unicode((resource['url'].split("?"))[0]+  '.ttl?api_key=e103dc13eb276ad734e680f5855f20c6&_view=completa').encode('utf8'))

        except NotFound:
            abort(404, _('Resource not found'))


    def render_resource(self, resource_id):
        """ Filter to resource rendering or download
                If resource doesn't exist, but a file with same name
                in XLS format does, it should be transformed to
                the required format (XML, JSON or CSV)
            """
        context = {'model': model, 'session': model.Session,
                   'user': c.user or c.author}
        try:
            # Resource exists, redirect to the download URL
            rsc = get_action('resource_show')(context, {'id': resource_id})
            return redirect(rsc['url'])
        except NotFound:
            # Resource doesn't exist, we search for a XLS file with same name
            xls_resource_id = re.sub("\.\w{3,4}$", ".xls", resource_id)
            try:
                rsc = get_action('resource_show')(context,
                                                  {'id': xls_resource_id})
            except NotFound:
                # Some resources has no extension...
                try:
                    xls_resource_id = re.sub("\.\w{3,4}$", "", resource_id)
                    rsc = get_action('resource_show')(context,
                                                      {'id': xls_resource_id})
                except:
                    print xls_resource_id + " not_found"
                    abort(404, _('Resource not found'))
        if rsc['url'] is None:
            abort(404, _('Resource not found'))

        xls_file = self._download_xls_file(rsc['url'])
        format = re.search("\.(\w{3,4})$", resource_id).group(1).lower()
        if format == 'xml':
            c.content_to_render = self._xls_to_xml(xls_file)
        elif format == 'json':
            c.content_to_render = self._xls_to_json(xls_file)
        elif format == 'csv':
            c.content_to_render = self._xls_to_csv(xls_file)
        else:
            remove(xls_file)
            abort(404, _('Resource not found'))

        remove(xls_file)
        return render('package/resource_render.html', loader_class=NewTextTemplate)

    def _create_json_index(self, data):
        data_wo_ids = self._remove_fields(data['results'])
        return JSONEncoder(ensure_ascii=False, indent=4).encode(data_wo_ids)

    def _create_xml_index(self, data):
        xml = self._serialize_xml(data['results'], 'datasets')
        return self._indent_xml(xml)


    def _serialize_xml(self, root, name):
        xml = ET.Element(name)
        if isinstance(root, dict):
            for key in root.keys():
                if key not in BLACKLIST:
                    xml.append(self._serialize_xml(root[key], key))
        elif isinstance(root, list):
            for item in root:
                xml.append(self._serialize_xml(item, 'item'))
        elif isinstance(root, bool) or isinstance(root, int):
            xml.text = str(root)
        else:
            xml.text = root
        return xml

    def _remove_fields(self, root):
        data = root
        if isinstance(data, dict):
            for key in data.keys():
                if key not in BLACKLIST:
                    data[key] = self._remove_fields(data[key])
                else:
                    del data[key]
        elif isinstance(data, list):
            for item in data:
                item = self._remove_fields(item)
        return data



    def _download_xls_file(self, url):
        """ Download a xls with random name to hard disk"""
        dest = configuracion.DOWNLOAD_TEMPORAL + "/" + str(int(time()*100)) + ".xls"
        urlretrieve(url, dest)
        return dest

    def _indent_xml(self, xml):
        raw_xml = ET.tostring(xml, 'utf-8')
        reparsed = minidom.parseString(raw_xml)
        return reparsed.toprettyxml()


    def _xls_to_xml(self, xls_file):
        """ Prepare a xml string based on a xls file """
        xml_filename = re.sub("\.xls", ".xml", xls_file)
        root = ET.Element("root")
        xls = xlrd.open_workbook(xls_file)
        for sheet_xls in xls.sheets():
            sheet_xml = ET.Element("sheet")
            sheet_xml.attrib["name"] = sheet_xls.name
            for row in range(sheet_xls.nrows):
                row_xml = ET.Element("row")
                row_xml.attrib["name"] = str(row)
                for value in sheet_xls.row_values(row):
                    value_xml = ET.Element("value")
                    if isinstance(value, unicode):
                        value_xml.text = value
                    else:
                        value_xml.text = str(value)
                    row_xml.append(value_xml)
                sheet_xml.append(row_xml)
            root.append(sheet_xml)
        return self._indent_xml(root)

    def _xls_to_json(self, xls_file):
        """ Prepare a json string based on a xls file """
        xls = xlrd.open_workbook(xls_file)
        sheets = []
        for sheet_xls in xls.sheets():
            sheet_json = {'name': sheet_xls.name}
            rows = []
            for row in range(sheet_xls.nrows):
                row_json = {'name': str(row)}
                values = []
                for value in sheet_xls.row_values(row):
                    if isinstance(value, unicode):
                        values.append(value)
                    else:
                        values.append(value)
                row_json['values'] = values
                rows.append(row_json)
            sheet_json['rows'] = rows
            sheets.append(sheet_json)
        text = JSONEncoder(ensure_ascii=False, indent=4).encode(sheets)
        return text

    def _xls_to_csv(self, xls_file):
        xls = xlrd.open_workbook(xls_file)
        sheet = xls.sheet_by_index(0)
        csv_rows = []
        for sheet in xls.sheets():
            for row in range(sheet.nrows):
                csv_row = []
                for value in sheet.row_values(row):
                    if isinstance(value, float):
                        value_to_print = str(value)
                    else:
                        value_to_print = value
                    csv_row.append(value_to_print)
                csv_rows.append(', '.join(csv_row))
        text = '\n'.join(csv_rows)
        return text

    def downloadIaest (self):
        from ckan.ckanclient.datosIaest import descargar
        descargar()

    # GUardar la vista generada
    def _save_vista(self, vista, filtro):

	#PRO
        connection = cx_Oracle.connect(configuracion.OPENDATA_USR + "/" + configuracion.OPENDATA_PASS  + "@" + configuracion.OPENDATA_CONEXION_BD)
        #PRE
	#connection = cx_Oracle.connect(configuracion.OPENDATA_USR + "/" + configuracion.OPENDATA_PASS  + "@" + configuracion.OPENDATA_CONEXION_BD_PRE)
	
	cursor = connection.cursor()
        resultado = cursor.var(cx_Oracle.NUMBER)
        registros = cursor.callproc('OPENDATA_PCK_ACCIONES.OPENDATA_PR_RESOURCEVISTA', [vista, filtro, "NADA", resultado])

        connection.commit()
        resultado = resultado.getvalue()

        cursor.close()
        connection.close()

        return configuracion.URL_VISTAS + str(resultado).split('.')[0]






    #Mostrar una vista guardada
    def showVista(self):
        import os
        import sys
        sys.path.insert(0, '/var/www/wolfcms/GA_OD_Core')
        import ga_od_core 
        params = dict(request.params.items())
        if params:
            vistaResourceId = params.get('id')
            vistaNombre = params.get('name').encode('utf8')
            vistaFormato = params.get('formato')
        
        vista_id = ga_od_core.get_view_id(vistaResourceId)
               
        data = ga_od_core.download(vista_id,None,None,vistaFormato,None,None)

        #import urllib2
        #data = urllib2.urlopen("http://preopendata.aragon.es/GA_OD_Core/download?view_id="+str(vista_id)+"&select_sql=*&filter_sql=&formato="+str(vistaFormato)).read()

        if (vistaFormato == 'JSON'):
            #response.headers['Content-Type'] = 'application/json;charset=utf-8'
            response.headers = [('Content-Disposition', 'attachment; filename=\"' + str(vistaNombre) +"__ad" +  ".json" + '\"'),('Content-Type', 'application/json;charset=utf-8')]
        if (vistaFormato == 'CSV'):
            #response.headers['Content-Type'] = 'text/csv;charset=utf-8'

            response.headers = [('Content-Disposition', 'attachment; filename=\"' + str(vistaNombre)+ "__ad"+ ".csv" + '\"'),('Content-Type', 'text/csv;charset=utf-8')]
        if (vistaFormato == 'XML'):
            response.headers['Content-Type'] = 'application/xml;charset=utf-8';
            response.headers['Content-Disposition'] = 'attachment; filename=' + str(vistaNombre) + '.xml';     
        return data
