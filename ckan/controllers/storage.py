import os
import re
import urllib
import uuid
from datetime import datetime
from cgi import FieldStorage

from ofs import get_impl
from pylons import request, response
from pylons.controllers.util import abort, redirect_to
from pylons import config
from paste.fileapp import FileApp
from paste.deploy.converters import asbool

from ckan.lib.base import BaseController, c, request, render, config, h, abort
from ckan.lib.jsonp import jsonpify
import ckan.model as model
import ckan.new_authz as new_authz
import cx_Oracle

from ckan.ckanclient import config as configuracion

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
try:
    import json
except:
    import simplejson as json

from logging import getLogger
log = getLogger(__name__)


BUCKET = config.get('ckan.storage.bucket', 'default')
key_prefix = config.get('ckan.storage.key_prefix', 'file/')

_eq_re = re.compile(r"^(.*)(=[0-9]*)$")


def fix_stupid_pylons_encoding(data):
    """
    Fix an apparent encoding problem when calling request.body
    TODO: Investigate whether this is fixed in later versions?
    """
    if data.startswith("%") or data.startswith("+"):
        data = urllib.unquote_plus(data)
    m = _eq_re.match(data)
    if m:
        data = m.groups()[0]
    return data


def create_pairtree_marker(folder):
    """ Creates the pairtree marker for tests if it doesn't exist """
    if not folder[:-1] == '/':
        folder = folder + '/'

    directory = os.path.dirname(folder)
    if not os.path.exists(directory):
        os.makedirs(directory)

    target = os.path.join(directory, 'pairtree_version0_1')
    if os.path.exists(target):
        return

    open(target, 'wb').close()


def get_ofs():
    """Return a configured instance of the appropriate OFS driver.
    """
    storage_backend = config['ofs.impl']
    kw = {}
    for k, v in config.items():
        if not k.startswith('ofs.') or k == 'ofs.impl':
            continue
        kw[k[4:]] = v

    # Make sure we have created the marker file to avoid pairtree issues
    if storage_backend == 'pairtree' and 'storage_dir' in kw:
        create_pairtree_marker(kw['storage_dir'])

    ofs = get_impl(storage_backend)(**kw)
    return ofs


def authorize(method, bucket, key, user, ofs):
    """
    Check authz for the user with a given bucket/key combo within a
    particular ofs implementation.
    """
    if not method in ['POST', 'GET', 'PUT', 'DELETE']:
        abort(400)
    if method != 'GET':
        # do not allow overwriting
        if ofs.exists(bucket, key):
            abort(409)
        # now check user stuff
        context = {'user': c.user,
                   'model': model}
        is_authorized = new_authz.is_authorized_boolean(
            'file_upload', context, {})
        if not is_authorized:
            h.flash_error('Not authorized to upload files.')
            abort(401)


class StorageController(BaseController):
    '''Upload to storage backend.
    '''
    _ofs_impl = None

    @property
    def ofs(self):
        if not StorageController._ofs_impl:
            StorageController._ofs_impl = get_ofs()
        return StorageController._ofs_impl

    def upload(self):
        label = key_prefix + request.params.get('filepath', str(uuid.uuid4()))
        c.data = {
            'action': h.url_for('storage_upload_handle', qualified=False),
            'fields': [
                {
                    'name': 'key',
                    'value': label
                }
            ]
        }
        return render('storage/index.html')

    def upload_handle(self):
        bucket_id = BUCKET
        params = dict(request.params.items())
        stream = params.get('file')
        label = params.get('key')
        authorize('POST', BUCKET, label, c.userobj, self.ofs)
        if not label:
            abort(400, "No label")
        if not isinstance(stream, FieldStorage):
            abort(400, "No file stream.")
        del params['file']
        params['filename-original'] = stream.filename
        #params['_owner'] = c.userobj.name if c.userobj else ""
        params['uploaded-by'] = c.userobj.name if c.userobj else ""

        self.ofs.put_stream(bucket_id, label, stream.file, params)
        success_action_redirect = h.url_for(
            'storage_upload_success', qualified=True,
            bucket=BUCKET, label=label)
        # Do not redirect here as it breaks js file uploads (get infinite loop
        # in FF and crash in Chrome)
        return self.success(label)

    def subir_archivos(self):

        params = dict(request.params.items())
        if params:
           stream = params.get('file')
           label = params.get('key')

           fn = os.path.basename(label.replace(' ','-'))

           folder = label.split('/')[0]
           nombre = label.split('/')[1]

           fn = nombre
           directory= configuracion.UPLOAD_DOCUMENTS + folder
           if not os.path.exists(directory):
            os.makedirs(directory)
           open(directory + "/" + fn, 'wb').write(stream.file.read())
           print('The file "' + fn + '" was uploaded successfully')
           message = 'The file "' + fn + '" was uploaded successfully'

        else:
           message = 'No file was uploaded'

    def success(self, label=None):
        label = request.params.get('label', label)
        h.flash_success('Upload successful')
        c.file_url = h.url_for('storage_file',
                               label=label,
                               qualified=True)
        c.upload_url = h.url_for('storage_upload')
        return render('storage/success.html')

    def success_empty(self, label=None):
        # very simple method that just returns 200 OK
        return ''

    def file(self, label):
        exists = self.ofs.exists(BUCKET, label)
        if not exists:
            # handle erroneous trailing slash by redirecting to url w/o slash
            if label.endswith('/'):
                label = label[:-1]
                # This may be best being cached_url until we have moved it into
                # permanent storage
                file_url = h.url_for('storage_file', label=label)
                h.redirect_to(file_url)
            else:
                abort(404)

        file_url = self.ofs.get_url(BUCKET, label)
        if file_url.startswith("file://"):
            metadata = self.ofs.get_metadata(BUCKET, label)
            filepath = file_url[len("file://"):]
            headers = {
                # 'Content-Disposition':'attachment; filename="%s"' % label,
                'Content-Type': metadata.get('_format', 'text/plain')}
            fapp = FileApp(filepath, headers=None, **headers)
            return fapp(request.environ, self.start_response)
        else:
            h.redirect_to(file_url.encode('ascii', 'ignore'))


class StorageAPIController(BaseController):
    _ofs_impl = None

    @property
    def ofs(self):
        if not StorageAPIController._ofs_impl:
            StorageAPIController._ofs_impl = get_ofs()
        return StorageAPIController._ofs_impl

    @jsonpify
    def index(self):
        info = {
            'metadata/{label}': {
                'description': 'Get or set metadata for this '
                               'item in storage', },
            'auth/request/{label}': {
                'description': self.auth_request.__doc__, },
            'auth/form/{label}': {
                'description': self.auth_form.__doc__, }}
        return info

    def set_metadata(self, label):
        bucket = BUCKET
        if not label.startswith("/"):
            label = "/" + label

        try:
            data = fix_stupid_pylons_encoding(request.body)
            if data:
                metadata = json.loads(data)
            else:
                metadata = {}
        except:
            abort(400)

        try:
            b = self.ofs._require_bucket(bucket)

        except:
            abort(409)

        k = self.ofs._get_key(b, label)
        if k is None:
            k = b.new_key(label)
            metadata = metadata.copy()
            metadata["_creation_time"] = str(datetime.utcnow())
            self.ofs._update_key_metadata(k, metadata)
            k.set_contents_from_file(StringIO(''))
        elif request.method == "PUT":
            old = self.ofs.get_metadata(bucket, label)
            to_delete = []
            for ok in old.keys():
                if ok not in metadata:
                    to_delete.append(ok)
            if to_delete:
                self.ofs.del_metadata_keys(bucket, label, to_delete)
            self.ofs.update_metadata(bucket, label, metadata)
        else:
            self.ofs.update_metadata(bucket, label, metadata)

        k.make_public()
        k.close()

        return self.get_metadata(bucket, label)

    @jsonpify
    def get_metadata(self, label):
        bucket = BUCKET
        storage_backend = config['ofs.impl']
        if storage_backend in ['google', 's3']:
            if not label.startswith("/"):
                label = "/" + label
            url = "https://%s%s" % (
                self.ofs.conn.calling_format.build_host(
                    self.ofs.conn.server_name(), bucket), label)
        else:
            #url = h.url_for('storage_file',label=label,qualified=False)
            #if url.startswith('/'):
            #url = config.get('ckan.site_url','').rstrip('/') + url

            url = configuracion.URL_DOCUMENTS + label

        #if not self.ofs.exists(bucket, label):
            #abort(404)        #metadata = self.ofs.get_metadata(bucket, label)
        now = datetime.now()

        metadata = {}
        metadata["_location"] = url
        metadata["filename-original"] = label.split("/")[1]
        metadata["_last_modified"] = now.strftime("%Y-%m-%d %H:%M")
        metadata["_label"] = label

        try:
            format = label.split('.')[1]
        except:
            format = "";

        metadata["_format"] = format

        try:
            tamanio = os.stat(configuracion.UPLOAD_DOCUMENTS + label).st_size
        except:
            tamanio = "";

        metadata["_content_length"] = tamanio;
        return metadata

    @jsonpify
    def auth_request(self, label):
        '''Provide authentication information for a request so a client can
        interact with backend storage directly.

        :param label: label.
        :param kwargs: sent either via query string for GET or json-encoded
            dict for POST). Interpreted as http headers for request plus an
            (optional) method parameter (being the HTTP method).

            Examples of headers are:

                Content-Type
                Content-Encoding (optional)
                Content-Length
                Content-MD5
                Expect (should be '100-Continue')

        :return: is a json hash containing various attributes including a
        headers dictionary containing an Authorization field which is good for
        15m.

        '''
        bucket = BUCKET
        if request.POST:
            try:
                data = fix_stupid_pylons_encoding(request.body)
                headers = json.loads(data)
            except Exception:
                from traceback import print_exc
                msg = StringIO()
                print_exc(msg)
                log.error(msg.seek(0).read())
                abort(400)
        else:
            headers = dict(request.params)
        if 'method' in headers:
            method = headers['method']
            del headers['method']
        else:
            method = 'POST'

        authorize(method, bucket, label, c.userobj, self.ofs)

        http_request = self.ofs.authenticate_request(method, bucket, label,
                                                     headers)
        return {
            'host': http_request.host,
            'method': http_request.method,
            'path': http_request.path,
            'headers': http_request.headers}

    def _get_remote_form_data(self, label):
        method = 'POST'
        content_length_range = \
            int(config.get('ckan.storage.max_content_length', 50000000))
        acl = 'public-read'
        fields = [{
            'name': self.ofs.conn.provider.metadata_prefix + 'uploaded-by',
            'value': c.userobj.id}]
        conditions = ['{"%s": "%s"}' % (x['name'], x['value']) for x in
                      fields]
        # In FF redirect to this breaks js upload as FF attempts to open file
        # (presumably because mimetype = javascript) and this stops js
        # success_action_redirect = h.url_for('storage_api_get_metadata',
        # qualified=True, label=label)
        success_action_redirect = h.url_for('storage_upload_success_empty',
                                            qualified=True,
                                            label=label)
        data = self.ofs.conn.build_post_form_args(
            BUCKET,
            label,
            expires_in=72000,
            max_content_length=content_length_range,
            success_action_redirect=success_action_redirect,
            acl=acl,
            fields=fields,
            conditions=conditions
        )
        # HACK: fix up some broken stuff from boto
        # e.g. should not have content-length-range in list of fields!
        storage_backend = config['ofs.impl']
        for idx, field in enumerate(data['fields']):
            if storage_backend == 'google':
                if field['name'] == 'AWSAccessKeyId':
                    field['name'] = 'GoogleAccessId'
            if field['name'] == 'content-length-range':
                del data['fields'][idx]
        return data

    def _get_form_data(self, label):
        storage_backend = config['ofs.impl']
        if storage_backend in ['google', 's3']:
            return self._get_remote_form_data(label)
        else:
            data = {
                'action': h.url_for('storage_upload_handle', qualified=False),
                'fields': [
                    {
                        'name': 'key',
                        'value': label
                    }
                ]
            }
            return data

    @jsonpify
    def auth_form(self, label):
        '''Provide fields for a form upload to storage including
        authentication.

        :param label: label.
        :return: json-encoded dictionary with action parameter and fields list.
        '''
        bucket = BUCKET
        if request.POST:
            try:
                data = fix_stupid_pylons_encoding(request.body)
                headers = json.loads(data)
            except Exception:
                from traceback import print_exc
                msg = StringIO()
                print_exc(msg)
                log.error(msg.seek(0).read())
                abort(400)
        else:
            headers = dict(request.params)

        method = 'POST'
        authorize(method, bucket, label, c.userobj, self.ofs)
        data = self._get_form_data(label)
        return data

    #Cargar la lista de vistas disponibles para ese usuario
    def load_user_vistas(self, label):

        params = dict(request.params.items())
        if params:
            user = params.get('user')

        connection = cx_Oracle.connect( configuracion.OPENDATA_USR + "/" + configuracion.OPENDATA_PASS + "@" + configuracion.OPENDATA_CONEXION_BD)
        cursor = connection.cursor()

        if user == configuracion.USR_ADMIN:
            sentencia = "SELECT id_vista, nombre FROM opendata.opendata_v_vistas"
        else:
            sentencia = "SELECT * FROM opendata.opendata_v_listadoVistas where usuario='" + user + "'"
        registros = cursor.execute(sentencia)

        lista = []
        for r in registros:
            lista.append(r)

        cursor.close()
        connection.close()

        return json.dumps(lista)

    # Cargar vista del desplegable en el formulario
    def show_vista(self, label):
        params = dict(request.params.items())
        if params:
            filtro = params.get('filtro')
            completa = params.get('completa')

        connection = cx_Oracle.connect(configuracion.OPENDATA_USR + "/" + configuracion.OPENDATA_PASS + "@" + configuracion.OPENDATA_CONEXION_BD)
        cursor = connection.cursor()
        registros = cursor.execute("SELECT NOMBREREAL,BASEDATOS FROM opendata.opendata_v_vistas where id_vista=" + label)

        datosVista = []
        for r in registros:
            datosVista.append(r)

        cursor.close()
        connection.close()

        # Comprobamos si se reciben los datos de la conexion (solo 1)
        if (len(datosVista) != 1):
            datosVista = "Ha ocurrido un error"
        else:
            print(datosVista[0][0])
            print(datosVista[0][1])

	    if (datosVista[0][1] =='APP1'):
		#connection2 = cx_Oracle.connect(configuracion.AST_USR + "/" + configuracion.AST_PASS + "@" + configuracion.AST1_CONEXION_BD)
		connection2 = cx_Oracle.connect(configuracion.OPENDATA_USR + "/" + configuracion.OPENDATA_PASS + "@" + configuracion.AST1_CONEXION_BD)
	    else:
		#connection2 = cx_Oracle.connect(configuracion.AST2_USR + "/" + configuracion.AST2_PASS + "@" + configuracion.AST2_CONEXION_BD)
                connection2 = cx_Oracle.connect(configuracion.AST1_USR + "/" + configuracion.AST1_PASS + "@" + configuracion.AST2_CONEXION_BD)

            cursor2 = connection2.cursor()

            sentencia = 'SELECT * FROM ' + datosVista[0][0];

            if (filtro == ''):
                if (completa == 'false'):
                    sentencia = sentencia + " WHERE ROWNUM <= 10";

            else:
                if (completa == 'true'):
                    sentencia = sentencia + " WHERE " + filtro;
                else:
                    sentencia = sentencia + " WHERE " + filtro + " AND ROWNUM <= 10";

            registros = cursor2.execute(sentencia)
            nombres = ()
            resultados = []

            # Obtener los nombres de las columnas
            descripcion = cursor2.description
            for col in descripcion:
                nombres = nombres + tuple([col[0]])
            resultados.append(nombres)

            hayElementos = False
            # Adjuntar los resultados
            for r in registros:
                hayElementos = True
                resultados.append(r)

            cursor2.close()
            connection2.close()

        if (hayElementos):
            data = resultados
        else:
            data = []

        def date_handler(obj):
            return obj.isoformat() if hasattr(obj, 'isoformat') else obj

        return json.dumps(data, default=date_handler)






