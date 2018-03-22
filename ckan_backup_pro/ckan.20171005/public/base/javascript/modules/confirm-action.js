this.ckan.module("confirm-action",function(b,a){return{options:{i18n:{heading:a("Please Confirm Action"),content:a("Are you sure you want to perform this action?"),confirm:a("Confirm"),cancel:a("Cancel")},template:['<div class="modal">','<div class="modal-header">','<button type="button" class="close" data-dismiss="modal">×</button>',"<h3></h3>","</div>",'<div class="modal-body"></div>','<div class="modal-footer">','<button class="btn btn-cancel"></button>','<button class="btn btn-primary"></button>',"</div>","</div>"].join("\n")},initialize:function(){b.proxyAll(this,/_on/);this.el.on("click",this._onClick)},confirm:function(){this.sandbox.body.append(this.createModal());this.modal.modal("show");this.modal.css({"margin-top":this.modal.height()*-0.5,top:"50%"})},performAction:function(){var c=b("<form/>",{action:this.el.attr("href"),method:"POST"});c.appendTo("body").submit()},createModal:function(){if(!this.modal){var c=this.modal=b(this.options.template);c.on("click",".btn-primary",this._onConfirmSuccess);c.on("click",".btn-cancel",this._onConfirmCancel);c.modal({show:false});c.find("h3").text(this.i18n("heading"));c.find(".modal-body").text(this.i18n("content"));c.find(".btn-primary").text(this.i18n("confirm"));c.find(".btn-cancel").text(this.i18n("cancel"))}return this.modal},_onClick:function(c){c.preventDefault();this.confirm()},_onConfirmSuccess:function(c){this.performAction()},_onConfirmCancel:function(c){this.modal.modal("hide")}}});