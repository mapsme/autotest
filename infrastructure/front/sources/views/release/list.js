import {JetView} from "webix-jet";
import MenuView from "views/top";
import {beta_url} from "models/beta"
import {release_statuses} from "models/release_statuses"

export default class ReleasesListView extends JetView{
	config(){
	    document.title = "Release list"

        var addButton = {
            view:"button",
            type:"icon",
            icon:"mdi mdi-plus-box",
            label:"Add new release",
            autowidth: true,
            align: "left",
            click: () => {
                var window = {
                      view:"window",
                      id: "add_window",
                      height:350,
                      width:500,
                      modal: true,
                      head:"Add new release",
                      position:"center",
                      body:{
                        view:"form",
                        id: "add_release_form",
                        elements: [
                            { rows:[

                                { view:"text",  name: "name", required: true, labelWidth: 150, width: 400, inputAlign: "right", labelAlign:"right", label:"Release name", value:"" },
                                { view:"combo", name: "status", required: true, labelWidth: 150, width: 400, inputAlign: "right", labelAlign:"right", label:"Release status", value:"New",
                                    options:release_statuses
                                },
                                { view: "datepicker", value: "", format: "%Y-%m-%d", label: "Start date", name: "time_start", labelWidth: 150, width: 400, labelAlign:"right"},
                                { view: "datepicker", value: "", format: "%Y-%m-%d", label: "End date", name: "time_end", labelWidth: 150, width: 400, labelAlign:"right"}
                            ]},


                            { cols: [
                                {view: "button", align: "center", type: "submit", label: "Add", autowidth: true, click: () => {
                                    var valid = $$('add_release_form').validate();
                                        if (valid) {
                                            webix.ajax().sync().post(beta_url + "/release", $$('add_release_form').getValues());
                                            $$('add_window').close();
                                            $$("mytable").load(beta_url + "/release?is_archive=false");
                                        }

                                    }},
                                {view: "button", align: "center", label: "Cancel", autowidth: true, click:("$$('add_window').close();")}
                                ]
                            }
                        ]
                      }
                    }

                    webix.ui(window).show();
            }
        }

        var grid = {
          view:"datatable",
          url: beta_url + "/release?is_archive=false",
          id: "mytable",
          select:"row",
          multiselect: false,
          columns:[
              {id:"name", header:"Release name",width:500, sort:"string", dataIndex: "name"},
              {id:"status", header:"Release status", sort:"string",fillspace:true, dataIndex: "status"},
              {id: "actions", header: "Actions", fillspace:true, template:"<span class='webix_icon mdi mdi-pencil'></span> <span class='webix_icon mdi mdi-archive'></span>" }],
            onClick:{
                "mdi-pencil":function(ev, id){
                    var window = {
                      view:"window",
                      id: "edit_window",
                      height:350,
                      width:500,
                      modal: true,
                      head:"Edit release",
                      position:"center",
                      body:{
                        view:"form",
                        id: "edit_release_form",
                        elements: [
                            { rows:[

                                { view:"text",  name: "name", required: true, labelWidth: 150, width: 400, inputAlign: "right", labelAlign:"right", label:"Release name", value:"" },
                                { view:"combo", name: "status", required: true, labelWidth: 150, width: 400, inputAlign: "right", labelAlign:"right", label:"Release status", value:"New",
                                    options:release_statuses
                                },
                                { view: "datepicker", value: "", format: "%Y-%m-%d", label: "Start date", name: "time_start", labelWidth: 150, width: 400, labelAlign:"right"},
                                { view: "datepicker", value: "", format: "%Y-%m-%d", label: "End date", name: "time_end", labelWidth: 150, width: 400, labelAlign:"right"}
                            ]},


                            { cols: [
                                {view: "button", align: "center", type: "submit", label: "Edit", autowidth: true, click: () => {
                                    var valid = $$('edit_release_form').validate();
                                        if (valid) {
                                            webix.ajax().sync().post(beta_url + "/release/" + $$('edit_release_form').getValues()["id"], $$('edit_release_form').getValues());
                                            $$('edit_window').close();
                                            $$("mytable").load(beta_url + "/release?is_archive=false");
                                        }

                                    }},
                                {view: "button", align: "center", label: "Cancel", autowidth: true, click:("$$('edit_window').close();")}
                                ]
                            }
                        ]
                      }
                    }

                    webix.ui(window).show();

                    webix.ajax().get(beta_url + "/release/" + id.row, function(text, data){
                        var response = data.json()
                        $$('edit_release_form').setValues(response);
                    });

                 },

                "mdi-archive":function(ev, id){

                    var test = this.getItem(id.row).name
                    var confirmArchive = {
                        view:"window",
                        id: "confirm_archive",
                        position:"center",
                        height:250,
                        width:300,
                        head: "Archive release \"" + test + "\"?",
                        body: {
                            cols: [
                                {view:"button", label:"OK", click: () =>
                                    {
                                        webix.ajax().bind(this).post(beta_url + "/release/" + id.row, {"is_archive": true}, function(text, data){
                                            $$('confirm_archive').close();
                                            this.$scope.refresh();
                                        });
                                    }
                                },
                                {view:"button", label:"Close", click:("$$('confirm_archive').close();")}
                            ]
                        }
                    }
                    webix.ui(confirmArchive).show();
                    return false;
                 }
            }
        }

        return {type: "layout",
           rows: [
           { cols: [ addButton ]},
           grid
           ]};
	}

	init() {

	    $$("mytable").attachEvent("onAfterSelect", function(selection, preserve){
	            if ($$("edit_release_form") == undefined && $$('confirm_archive') == undefined) {
	                this.$scope.show("/top/release.dashboard?id=" + selection.id);
	            }
	            else {
	                $$("mytable").unselectAll()
	            }
        })
	}
}