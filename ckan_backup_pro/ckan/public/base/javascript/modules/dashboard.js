this.ckan.module("dashboard",function(b,a){return{button:null,popover:null,searchTimeout:null,initialize:function(){b.proxyAll(this,/_on/);this.button=b("#followee-filter .btn").on("click",this._onShowFolloweeDropdown);var c=this.button.prop("title");this.button.popover({placement:"bottom",title:"Filter",html:true,content:b("#followee-popover").html()});this.button.prop("title",c);this.popover=this.button.data("popover").tip().addClass("popover-followee")},_onShowFolloweeDropdown:function(){this.button.toggleClass("active");if(this.button.hasClass("active")){setTimeout(this._onInitSearch,100)}return false},_onInitSearch:function(){var c=b("input",this.popover);if(!c.hasClass("inited")){c.on("keyup",this._onSearchKeyUp).addClass("inited")}c.focus()},_onSearchKeyUp:function(){clearTimeout(this.searchTimeout);this.searchTimeout=setTimeout(this._onSearchKeyUpTimeout,300)},_onSearchKeyUpTimeout:function(){var c=b("input",this.popover);var d=c.val().toLowerCase();if(d){b("li",this.popover).hide();b('li.everything, [data-search^="'+d+'"]',this.popover).show()}else{b("li",this.popover).show()}}}});