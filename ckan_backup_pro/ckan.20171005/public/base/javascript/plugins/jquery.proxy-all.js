(function(a){a.proxyAll=function(f){var b=[].slice.call(arguments,1);var c=0;var d=b.length;var e;var g;for(;c<d;c+=1){g=b[c];for(e in f){if(typeof f[e]==="function"){if((g instanceof RegExp&&g.test(e))||e===g){if(f[e].proxied!==true){f[e]=a.proxy(f[e],f);f[e].proxied=true}}}}}return f}})(this.jQuery);