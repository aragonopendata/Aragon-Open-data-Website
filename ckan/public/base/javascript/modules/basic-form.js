this.ckan.module("basic-form",function(b,a){return{initialize:function(){var c=a("There are unsaved modifications to this form").fetch();this.el.incompleteFormWarning(c);if($("html").hasClass("ie7")){this.el.on("submit",function(){var d=$(this);$("button",d).each(function(){var e=$(this);$('<input type="hidden">').prop("name",e.prop("name")).prop("value",e.val()).appendTo(d)})})}}}});