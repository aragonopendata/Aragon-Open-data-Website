(function(d,c){var i={};function f(o){var m=[].slice.call(arguments,0),n=0,p=m.length;for(;n<p;n+=1){o[m[n]]=d.proxy(o[m[n]],o)}return o}function g(n){if(typeof n!=="object"){return{}}else{if(Object.create){return Object.create(n)}}function m(){}m.prototype=n;return new m()}function e(p,m,n){m=m||{};var o=m.hasOwnProperty("constructor")?m.constructor:e.constructor(p);o.prototype=g(p.prototype);o.prototype.constructor=o;delete m.constructor;d.extend(o.prototype,m,{__super__:p.prototype});return d.extend(o,p,n)}i.View=e({},{constructor:function a(m){this.el=m instanceof d?m:d(m);this.events=d({})},$:function(m){return this.el.find(m)},bind:function(m,o){if(arguments.length===1){for(var n in m){if(m.hasOwnProperty(n)){this.bind(n,m[n])}}return this}function p(){return o.apply(this,Array.prototype.slice.call(arguments,1))}p.guid=o.guid=o.guid||(d.guid?d.guid++:d.event.guid++);this.events.bind(m,p);return this},unbind:function(){this.events.unbind.apply(this.events,arguments);return this},trigger:function(){this.events.triggerHandler.apply(this.events,arguments);return this},show:function(){this.el.show();return this.trigger("show")},hide:function(){this.el.hide();return this.trigger("hide")}});i.MainView=e(i.View,{constructor:function h(o,n,q,p){this.__super__.constructor.apply(this,arguments);f(this,"redraw","onNavChange","onNavToggleEditor","onEditorSubmit");var m=this;this.nav=new i.NavigationView(this.$(".dataexplorer-tableview-nav"));this.grid=new i.GridView(this.$(".dataexplorer-tableview-grid"),n,q);this.chart=new i.ChartView(this.$(".dataexplorer-tableview-graph"),n,q);this.editor=new i.EditorView(this.$(".dataexplorer-tableview-editor"),n,p);this.nav.bind({change:this.onNavChange,"toggle-editor":this.onNavToggleEditor});this.editor.bind({"show hide":this.redraw,submit:this.onEditorSubmit});this.$(".dataexplorer-tableview-editor-info h1").click(function(){d(this).parent().toggleClass("dataexplorer-tableview-editor-hide-info")});this.chart.hide()},redraw:function(){this.chart.redraw();this.grid.redraw();return this},onNavChange:function(n){var m=n==="grid";this.grid[m?"show":"hide"]();this.chart[m?"hide":"show"]()},onNavToggleEditor:function(m){this.el.toggleClass("dataexplorer-tableview-hide-editor",!m);this.redraw()},onEditorSubmit:function(m){this.nav.toggle("chart");this.chart.update(m)}});i.NavigationView=e(i.View,{constructor:function b(m){this.__super__.constructor.apply(this,arguments);f(this,"onEditorToggleChange","onPanelToggleChange");this.panelButtons=this.$(".dataexplorer-tableview-nav-toggle").buttonset();this.panelButtons.change(this.onPanelToggleChange);this.editorButton=this.$("#dataexplorer-tableview-nav-editor").button();this.editorButton.change(this.onEditorToggleChange)},toggle:function(m){this.$('input[value="'+m+'"]').click().change().next().click();return this},onPanelToggleChange:function(m){this.trigger("change",[m.target.value])},onEditorToggleChange:function(m){this.trigger("toggle-editor",[m.target.checked])}});i.GridView=e(i.View,{constructor:function j(o,n,p,m){this.__super__.constructor.apply(this,arguments);f(this,"_onSort","redraw");this.dirty=false;this.columns=n;this.data=p;this.grid=new Slick.Grid(o,p,n,d.extend({enableColumnReorder:false,forceFitColumns:true,syncColumnCellResize:true,enableCellRangeSelection:false},m));this.grid.onSort=this._onSort;this.$(".slick-header-column").wrapInner('<div class="slick-header-wrapper" />').css("overflow","visible").css("z-index",function(q){return n.length-q});new Slick.Controls.ColumnPicker(this.columns,this.grid)},show:function(){this.__super__.show.apply(this,arguments);if(this.dirty){this.redraw();this.dirty=false}return this},redraw:function(){if(this.el.is(":visible")){this.grid.resizeCanvas();this.grid.autosizeColumns()}else{this.dirty=true}},_onSort:function(n,m){this.data.sort(function(q,p){var o=q[n.field],r=p[n.field];if(o==r){return 0}return(o>r?1:-1)*(m?1:-1)});this.grid.invalidate()}});i.ChartView=e(i.View,{constructor:function k(n,m,p,o){this.__super__.constructor.apply(this,arguments);this.data=p;this.columns=m;this.chart=o;this.createPlot((o&&o.type)||"line");this.draw()},createPlot:function(o){var n=i.ChartView.findTypeById(o),m=n&&n.getOptions?n.getOptions(this):{};this.plot=d.plot(this.el,this.createSeries(),m);return this},createSeries:function(){var n=[],m=this;if(this.chart){d.each(this.chart.series,function(o,q){var p=[];d.each(m.data,function(s){var r=this[m.chart.groups],t=this[q];if(typeof r==="string"){r=s}p.push([r,t])});n.push({data:p,label:m._getColumnName(q)})})}return n},draw:function(){this.plot.setData(this.createSeries());return this.redraw()},update:function(m){if(!this.chart||m.type!==this.chart.type){this.createPlot(m.type)}this.chart=m;this.draw();return this},redraw:function(){this.plot.resize();this.plot.setupGrid();this.plot.draw();return this},_getColumnName:function(o){for(var m=0,n=this.columns.length;m<n;m+=1){if(this.columns[m].field===o){return this.columns[m].name}}return name}},{TYPES:[{id:"line",name:"Line Chart"},{id:"bar",name:"Bar Chart (draft)",getOptions:function(m){return{series:{lines:{show:false},bars:{show:true,barWidth:1,align:"left",fill:true}},xaxis:{tickSize:1,tickLength:1,tickFormatter:function(n){if(m.data[n]){return m.data[n][m.chart.groups]}return""}}}}}],findTypeById:function(n){var m=d.grep(this.TYPES,function(o){return o.id===n});return m.length?m[0]:null}});i.EditorView=e(i.View,{constructor:function l(n,m,o){this.__super__.constructor.apply(this,arguments);f(this,"onAdd","onRemove","onSubmit","onSave");this.columns=m;this.type=this.$(".dataexplorer-tableview-editor-type select");this.groups=this.$(".dataexplorer-tableview-editor-group select");this.series=this.$(".dataexplorer-tableview-editor-series select");this.id=this.$(".dataexplorer-tableview-editor-id");this.$("button").button();this.save=this.$(".dataexplorer-tableview-editor-save").click(this.onSave);this.el.bind("submit",this.onSubmit);this.el.delegate('a[href="#remove"]',"click",this.onRemove);this.el.delegate("select","change",this.onSubmit);this.$(".dataexplorer-tableview-editor-add").click(this.onAdd);this.setupTypeOptions().setupColumnOptions();this.seriesClone=this.series.parent().clone();if(o){this.load(o)}},setupTypeOptions:function(){var m={};d.each(i.ChartView.TYPES,function(){m[this.id]=this.name});this.type.html(this._createOptions(m));return this},setupColumnOptions:function(){var m={},n="";d.each(this.columns,function(o,p){m[p.field]=p.name});n=this._createOptions(m);this.groups.html(n);this.series.html(n);return this},addSeries:function(){var o=this.seriesClone.clone(),n=o.find("label"),m=this.series.length;this.$("ul").append(o);this.updateSeries();n.append('<a href="#remove">Remove</a>');n.find("span").text(String.fromCharCode(this.series.length+64));return this},removeSeries:function(m){m.remove();this.updateSeries();this.series.each(function(o){if(o>0){var n=d(this).prev().find("span");n.text(String.fromCharCode(o+65))}});return this.submit()},updateSeries:function(){this.series=this.$(".dataexplorer-tableview-editor-series select");return this},load:function(n){var m=this;this._selectOption(this.type,n.type);this._selectOption(this.groups,n.groups);this.id.val(n.id);this.type.val(n.type);d.each(n.series,function o(p,r){var q=m.series.eq(p);if(!q.length){m.addSeries();return o(p,r)}m._selectOption(q,r)});return this},submit:function(){return this._triggerChartData("submit")},loading:function(m){var n=m===false?"enable":"disable";this.$("select").attr("disabled",m!==false);this.save.button(n);this._updateSaveText(m===false?null:"Loading...");return this},saving:function(m){this.disableSave(m);this._updateSaveText(m===false?null:"Saving...");return this},disableSave:function(m){this.save.button(m===false?"enable":"disable");return this},onAdd:function(m){m.preventDefault();this.addSeries()},onRemove:function(n){n.preventDefault();var m=d(n.target).parents(".dataexplorer-tableview-editor-series");this.removeSeries(m)},onSave:function(m){m.preventDefault();this._triggerChartData("save")},onSubmit:function(m){m&&m.preventDefault();this.submit()},_updateSaveText:function(o){var n=this.save.find("span"),m=n.data("default");if(!m){n.data("default",n.text())}n.text(o||m)},_triggerChartData:function(m){var n=this.series.map(function(){return d(this).val()});return this.trigger(m,[{id:this.id.val(),type:this.type.val(),groups:this.groups.val(),series:d.makeArray(n)}])},_selectOption:function(m,n){m.find('[value="'+n+'"]').attr("selected","selected")},_createOptions:function(m){var n=[];d.each(m,function(o,p){n.push('<option value="'+o+'">'+p+"</option>")});return n.join("")}});d.extend(true,this,{DATAEXPLORER:{TABLEVIEW:{UI:i,createTableView:function(n,m,p,o){return new i.MainView(n,m,p,o)}}}})})(jQuery);