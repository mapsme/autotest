import {JetView} from "webix-jet";
import MenuView from "views/top";
import {beta_url} from "models/beta"

export default class UniqueCrashListView extends JetView{
	config(){

	    document.title = "Crash list"

        var grid = {
          view:"datatable",
          select:"row",
          id: "crashes_table",
          pager: "crash_pager",
          columns:[
              {id:"id", template: function(obj) {
                    return '<a href="#!/top/unique.crash?id='+ obj.id + '">' + obj.id + '</a>'}, header:"Number",width:100, sort:"int"},
              {id:"release", header:"Release", fillspace:true, sort:"string"},
              {id:"device_name", header:"Device",fillspace:true, sort:"string"},
              {id:"date", header:"Date",fillspace:true, sort:"string"},
              {id:"count", header:"Count",fillspace:true, sort:"int"}
              ]
            }

       var search_layout = {view:"search", id: "search", placeholder:"Search..",  hotkey: "enter", inputAlign: "left", width: 300, click: doOnClick}

       function doOnClick(){
           if ($$("search").getValue() != ""){
                console.log($$("search").getValue())
                 webix.ajax().get(beta_url + "/crashes/search", {"text": $$("search").getValue()}, function(text, data){
                    var info = data.json()
                    console.log(info)
                    $$("search").setValue("")
                    $$("crash_pager").disable()
                    $$("crashes_table").clearAll()
                    $$("crashes_table").parse(info)


                    if ($$("clear_filter") == undefined){
                    $$("header_layout").addView({view:"button", type:"icon", id: "clear_filter",
                                                icon: "mdi mdi-close", width: 40, tooltip: "Clear search results",
                                                css: "webix_transparent.webix_button"})
                    $$("clear_filter").attachEvent("onItemClick", function(){
                        $$("crashes_table").setPage(0)
                        $$("crashes_table").clearAll()
                        $$("crashes_table").loadNext(50, 0, function(){}, beta_url + "/crashes/unique")
                        $$("clear_filter").hide()
                        $$("crash_pager").enable()
                    })
                } else {
                    $$("clear_filter").show()
                    $$("crash_pager").disable()
                }
                 })
             }

       }
       // todo поиск по тексту


       var pager = {
          view:"pager", id:"crash_pager",
          size:50,
          template: "{common.prev()}{common.page()}{common.next()}",
          maxWidth: 100
        }

       return {type: "layout",
               rows: [
               {id: "header_layout", cols: [pager, search_layout]},
               grid
              ]};
	}

	init(){
	    $$("crashes_table").loadNext(50, 0, function(){}, beta_url + "/crashes/unique").then(function(){
	        $$("crash_pager").attachEvent("onItemClick", function(id, ev){
	        var page = this.config.page
	        if (id=="next"){
                $$("crashes_table").loadNext(50, this.config.page+1, null, beta_url + "/crashes/unique").then(function(data){
                       var json = data.json();
                       $$("crashes_table").parse(json)
                       $$("crashes_table").setPage(page+1)
                });
            } else {
                $$("crashes_table").setPage(page)
            }

	        })

	    })

	    $$("crashes_table").attachEvent("onAfterSelect", function(selection, preserve){
                this.$scope.show("/top/unique.crash?id=" + selection.id)
        })

	}

	ready(view){
	    //webix.ui(view)
	}
};