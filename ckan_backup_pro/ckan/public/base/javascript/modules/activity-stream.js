this.ckan.module("activity-stream",function(b,a){return{options:{more:null,id:null,context:null,offset:null,loading:false,i18n:{loading:a("Loading...")}},initialize:function(){b.proxyAll(this,/_on/);var c=this.options;c.more=(c.more=="True");this._onBuildLoadMore();b(window).on("scroll",this._onScrollIntoView);this._onScrollIntoView()},elementInViewport:function(e){var g=e.offsetTop;var f=e.offsetLeft;var d=e.offsetWidth;var c=e.offsetHeight;while(e.offsetParent){e=e.offsetParent;g+=e.offsetTop;f+=e.offsetLeft}return(g<(window.pageYOffset+window.innerHeight)&&f<(window.pageXOffset+window.innerWidth)&&(g+c)>window.pageYOffset&&(f+d)>window.pageXOffset)},_onScrollIntoView:function(){var d=b(".load-more a",this.el);if(d.length==1){var c=this.elementInViewport(d[0]);if(c&&!this.options.loading){d.trigger("click")}}},_onBuildLoadMore:function(){var c=this.options;if(c.more){b(".load-more",this.el).on("click","a",this._onLoadMoreClick);c.offset=b(".item",this.el).length}},_onLoadMoreClick:function(d){d.preventDefault();var c=this.options;if(!c.loading){c.loading=true;b(".load-more a",this.el).html(this.i18n("loading")).addClass("disabled");this.sandbox.client.call("GET",c.context+"_activity_list_html","?id="+c.id+"&offset="+c.offset,this._onActivitiesLoaded)}},_onActivitiesLoaded:function(e){var d=this.options;var c=b(e.result);d.more=(c.data("module-more")=="True");d.offset+=30;b(".load-less",c).remove();b(".load-more",this.el).remove();b("li",c).appendTo(this.el);this._onBuildLoadMore();d.loading=false}}});