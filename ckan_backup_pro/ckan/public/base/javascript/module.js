this.ckan=this.ckan||{};(function(f,g,d){var b="data-module";var e="data-module-";function a(j,i,h){this.el=j instanceof g?j:g(j);this.options=g.extend(true,{},this.options,i);this.sandbox=h}g.extend(a.prototype,{el:null,options:null,$:function(h){return this.el.find(h)},i18n:function(j){var h=[].slice.call(arguments,1);var k=this.options.i18n;var i=(k&&k[j])||j;if(typeof i==="function"){i=i.apply(null,h)}return typeof i.fetch==="function"?i.fetch.apply(i,h):i},initialize:function(){},teardown:function(){},remove:function(){this.teardown();this.el.remove()}});function c(i,j){if(c.registry[i]){throw new Error('There is already a module registered as "'+i+'"')}if(typeof j==="function"){j=j(g,f.i18n.translate,f.i18n)}j=g.extend({constructor:function h(){a.apply(this,arguments)}},j);c.registry[i]=g.inherit(a,j,{namespace:i});return f}c.registry={};c.instances={};c.initialize=function(){f.pubsub.enqueue();g("[data-module]",document.body).each(function(h,i){c.initializeElement(this)});f.pubsub.dequeue();return c};c.initializeElement=function(i){var h=c.registry;var j=g.trim(i.getAttribute(b)).split(" ");g.each(j,function(m,l){var k=h[l];if(k&&typeof k==="function"){c.createInstance(k,i)}})};c.createInstance=function(k,l){var j=c.extractOptions(l);var i=f.sandbox(l,j);var h=new k(l,j,i);if(typeof h.initialize==="function"){h.initialize()}var m=c.instances[k.namespace]||[];m.push(h);c.instances[k.namespace]=m};c.extractOptions=function(j){var o=j.attributes;var k=0;var i=o.length;var p={};var h;var l;var n;for(;k<i;k+=1){l=o[k];if(l.name.indexOf(e)===0){h=l.name.slice(e.length);try{n=l.value===""?true:g.parseJSON(l.value)}catch(m){n=l.value}p[g.camelCase(h)]=n}}return p};f.module=c;f.module.BaseModule=a})(this.ckan,this.jQuery,this);