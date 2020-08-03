import {JetView} from "webix-jet";
import {getJenkinsLink} from "utils/func"
import {beta_url} from "models/beta"
import {release_statuses} from "models/release_statuses"

export default class ReleaseView extends JetView{
    config(){

        var params = this.getUrl()[0].params;
        document.title = "Release info"

        var title = {id: "title_info", cols: [{ view:"label", label:"Release info"}]}
        var properties = { type:"layout", id: "info_layout", rows: []}
        var test_list = {
            view:"datatable",
            url: beta_url + "/feature?release_id=" + params.id,
            id: "mytable",
            select:false,
            borderless: false,
            columns:[
              {id:"name", header:"Feature name",width:300, sort:"string",name: "name"},
              {id:"requirements_status", header:"Requirements",fillspace:true, sort:"string", name: "requirements_status"},
              {id:"dev_status", header:"Development",fillspace:true,sort:"string", dataIndex: "dev_status"},
              {id:"testing_status", name: "testing_status", header:"Testing", sort:"string",fillspace:true },
              {id: "actions", header: "Edit", width:48, template:"<span class='webix_icon mdi mdi-pencil'></span>" }
              ],
            onClick:{
                "mdi-pencil":function(ev, id){
                    var window = {
                      view:"window",
                      id: "edit_window",
                      height:350,
                      width:500,
                      modal: true,
                      head:"Edit feature",
                      position:"center",
                      body:{
                        view:"form",
                        id: "edit_release_form",
                        elements: [
                            { rows:[

                                { view:"text",  name: "name", required: true, labelWidth: 150, width: 400, inputAlign: "right", labelAlign:"right", label:"Feature name", value:"Feature 1" },
                                { view:"combo", name: "requirements_status", required: true, labelWidth: 150, width: 400, inputAlign: "right", labelAlign:"right", label:"Requirements", value:"Done", options:release_statuses},
                                { view:"combo", name: "dev_status", required: true, labelWidth: 150, width: 400, inputAlign: "right", labelAlign:"right", label:"Development", value:"Work", options:release_statuses},
                                { view:"combo", name: "testing_status", required: true, labelWidth: 150, width: 400, inputAlign: "right", labelAlign:"right", label:"Testing", value:"New", options:release_statuses},

                                  ]},


                            { cols: [
                                {view: "button", align: "center", type: "submit", label: "Edit", autowidth: true, click: () => {
                                    var valid = $$('edit_release_form').validate();
                                        if (valid) {
                                            webix.ajax().sync().post(beta_url + "/feature/" + $$('edit_release_form').getValues()["id"], $$('edit_release_form').getValues());
                                            $$('edit_window').close();
                                            $$("mytable").load(beta_url + "/feature?release_id=" + params.id);
                                        }

                                    }},
                                {view: "button", align: "center", label: "Cancel", autowidth: true, click:("$$('edit_window').close();")}
                                ]
                            }
                        ]
                      }
                    }

                    webix.ui(window).show();

                    webix.ajax().get(beta_url + "/feature/" + id.row, function(text, data){
                        var response = data.json()
                        $$('edit_release_form').setValues(response);
                    });

                 }
            }
        }


        var addButton = {
            view:"button",
            type:"icon",
            id: "add_button",
            icon:"mdi mdi-plus-box",
            label:"Add feature",
            autowidth: true,
            align: "left",
            hidden: true,
            click: () => {
                var window = {
                      view:"window",
                      id: "add_window",
                      height:350,
                      width:500,
                      modal: true,
                      head:"Add feature",
                      position:"center",
                      body:{
                        view:"form",
                        id: "add_release_form",
                        elements: [
                            { rows:[


                                { view:"text",  name: "name", required: true, labelWidth: 150, width: 400, inputAlign: "right", labelAlign:"right", label:"Feature name", value:"" },
                                { view:"combo", name: "requirements_status", required: true, labelWidth: 150, width: 400, inputAlign: "right", labelAlign:"right", label:"Requirements", value:"New", options:release_statuses},
                                { view:"combo", name: "dev_status", required: true, labelWidth: 150, width: 400, inputAlign: "right", labelAlign:"right", label:"Development", value:"New", options:release_statuses},
                                { view:"combo", name: "testing_status", required: true, labelWidth: 150, width: 400, inputAlign: "right", labelAlign:"right", label:"Testing", value:"New", options:release_statuses},

                            ]},


                            { cols: [
                                {view: "button", align: "center", type: "submit", label: "Add", autowidth: true, click: () => {
                                    var valid = $$('add_release_form').validate();
                                        if (valid) {
                                           var vals = $$('add_release_form').getValues()
                                           vals["release_id"] = params.id
                                           webix.ajax().sync().post(beta_url + "/feature", vals);
                                           $$('add_window').close();
                                           $$("mytable").load(beta_url + "/feature?release_id=" + params.id);
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

       return {type: "layout",
       rows: [
            title,
            properties,
           test_list,
           addButton
       ]};
    }

    init(){
        var params = this.getUrl()[0].params;
        webix.ajax().bind(this).get(beta_url + "/release/" + params.id, function(text, data){
            var info = data.json()
            var info_layout = $$("info_layout")
            var title = $$("title_info")
            var ch = title.getChildViews()[0]
            ch.data.label = "Release \"" + info.name + "\" info"
            ch.refresh()
            info_layout.addView({view: "label", label: "Status: " + info.status, id: "release_status", css: {"font-size": "150%", "margin-left" : "50px"}})
            if (info.time_start != "") {
                info_layout.addView({view: "label", label: "Start time: " + info.time_start, id: "time_start"})
            }
            if (info.time_end != "") {
                info_layout.addView({view: "label", label: "End time: " + info.time_end, id: "time_end"})
            }
            if (info.is_archive == true) {
                title.addView({view: "label", align: "right", template: "<span class='archive'><b>ARCHIVED</b></span>", autowidth: true})
                $$("add_button").destructor()
            }
            else {
                $$("add_button").show()
            }
        });
        $$("mytable").attachEvent("onAfterLoad", function(){
                $$("mytable").eachRow(function(row){
                    var record = $$("mytable").getItem(row);
                    var css = null
                    if (record.requirements_status == "New") css = "release_status_new";
                    if (record.requirements_status == "Work") css = "release_status_work";
                    if (record.requirements_status == "Done") css = "release_status_done";
                    $$("mytable").addCellCss(record.id, "requirements_status", css);

                    if (record.dev_status == "New") css = "release_status_new";
                    if (record.dev_status == "Work") css = "release_status_work";
                    if (record.dev_status == "Done") css = "release_status_done";

                    $$("mytable").addCellCss(record.id, "dev_status", css);

                    if (record.testing_status == "New") css = "release_status_new";
                    if (record.testing_status == "Work") css = "release_status_work";
                    if (record.testing_status == "Done") css = "release_status_done";

                    $$("mytable").addCellCss(record.id, "testing_status", css);

                    $$("mytable").refresh();
            }, true);
        });
    }
}