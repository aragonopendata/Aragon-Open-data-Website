!function(e){function t(t){var n=this.value,s=e.url.slugify(n,!0);n!==s&&(this.value=s,e(this).trigger("slugify",[this.value,n]))}function n(t){if(t.charCode){t.preventDefault();var n,s,i=this.value,u=this.selectionStart,l=this.selectionEnd,r=String.fromCharCode(t.charCode);this.setSelectionRange?(n=i.substring(0,u)+r+i.substring(l,i.length),this.value=e.url.slugify(n,!1),this.setSelectionRange(u+1,u+1)):document.selection&&document.selection.createRange&&(s=document.selection.createRange(),s.text=r+s.text),e(this).trigger("slugify",[this.value,i])}}e.fn.slug=function(){return this.each(function(){e(this).on({"blur.slug":t,"change.slug":t,"keypress.slug":n})})},e.extend(e.fn.slug,{onChange:t,onKeypress:n})}(this.jQuery);