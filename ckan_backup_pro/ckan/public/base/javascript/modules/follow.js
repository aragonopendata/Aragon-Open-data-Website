this.ckan.module("follow",function(b,a){return{options:{action:null,type:null,id:null,loading:false,i18n:{follow:a("Follow"),unfollow:a("Unfollow")}},initialize:function(){b.proxyAll(this,/_on/);this.el.on("click",this._onClick)},_onClick:function(e){var d=this.options;if(d.action&&d.type&&d.id&&!d.loading){e.preventDefault();var c=this.sandbox.client;var f=d.action+"_"+d.type;d.loading=true;this.el.addClass("disabled");c.call("POST",f,{id:d.id},this._onClickLoaded)}},_onClickLoaded:function(e){var d=this.options;var c=this.sandbox;d.loading=false;this.el.removeClass("disabled");if(d.action=="follow"){d.action="unfollow";this.el.html('<i class="icon-remove-sign"></i> '+this.i18n("unfollow")).removeClass("btn-success").addClass("btn-danger")}else{d.action="follow";this.el.html('<i class="icon-plus-sign"></i> '+this.i18n("follow")).removeClass("btn-danger").addClass("btn-success")}c.publish("follow-"+d.action+"-"+d.id)}}});