(function(d,c){var b=d.url.escape;function a(f){f=d.extend(true,a.defaults,f||{});var e=this.map(function(){var g=d(this);var j=g.find("input");var i=d(f.template);var h=i.find(".slug-preview-value");function k(){var l=b(j.val())||f.placeholder;h.text(l)}i.find("label").text(f.i18n.URL);i.find(".slug-preview-prefix").text(f.prefix);i.find("button").text(f.i18n.Edit).click(function(l){l.preventDefault();g.show();i.hide()});k();j.on("change",k);g.after(i).hide();return i[0]});return this.pushStack(e)}a.defaults={prefix:"",placeholder:"",i18n:{URL:"URL",Edit:"Edit"},template:['<div class="slug-preview">','  <div style="height:22px"></div>','<label class="control-label fieldName" for="field-title"></label><div style="height:44px"></div>','<span class="slug-preview-prefix"></span><span class="slug-preview-value"></span>','<button class="recuadroRedondeado"></button>',"</div>"].join("\n")};d.fn.slugPreview=a})(this.jQuery,this);