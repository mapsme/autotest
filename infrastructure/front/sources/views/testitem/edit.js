import {JetView} from "webix-jet";
import {beta_url} from "models/beta"

export default class EditTestFormView extends JetView{

	config(){

        var params = this.getUrl()[0].params;


		var form = {
            view:"form",  id:"edit_test_form", scroll: true,
            elements: [
            { view:"label", label: "Edit test", css: {"font-size": "120%"}},
                { rows:[
                    { template:"Test name", type:"section"},
                    { view:"text", required: true, name: "name", label:"Name", labelWidth: 200, width: 800, labelAlign:"right", inputAlign: "right"},
                    { view:"text", required: true, name: "method_name", label:"Method reference", labelWidth: 200, width: 800, labelAlign:"right", inputAlign: "right" },
                    { view:"combo", name: "type", id: "type", required: true, labelWidth: 200, width: 800, inputAlign: "right", labelAlign:"right", label:"Type",
                      options:[ "ui", "hardware", "booking"]
                    },
                    { view:"textarea", label:"Comment", name: "comment", labelWidth: 200, width: 800,labelAlign:"right", inputAlign: "right", height: 200}
                ]},
                /*{ rows:[
                    { template:"Test steps", type:"section"},
                    { view: "label", label: "Steps"},
                    { view:"button", id: "add_step_button", type:"icon", icon:"mdi mdi-plus-box", label:"Add step", autowidth: true , align: "left", click: addStepInput }
                ]},*/
                { rows:[
                    { template:"Related requirements", type:"section"},
                    { view: "label", label: "Requirements"},
                    { view:"button", id: "link_requirement_button", type:"icon", icon:"mdi mdi-plus-box", label:"Link requirement", autowidth: true , align: "left" /*, click: rebuildForm*/ }
                ]},
                { cols: [
                    {view: "button", id: "edit_button", label: "Edit", autowidth: true, click: () => {
                        var valid = $$('edit_test_form').validate();
                        if (valid) {
                            webix.ajax().post(beta_url + "/testitem/" + $$('edit_test_form').getValues()["id"], $$('edit_test_form').getValues());
                            this.app.show("/top/testitem.list");
                            }
                        }
                    },
                    {view: "button", id: "cancel_button", label: "Cancel", autowidth: true}
                    ]
                },

            ]
        };

        /*function addStepInput(){
            var add_step = $$('edit_test_form').getChildViews()[2];
            var childs = add_step.$view.childNodes
            var i = childs.length - 1
            add_step.addView({cols:[{ view:"textarea", height:80, labelAlign:"right", labelWidth: 200, label: (i-1) + ".", value:"" , id: "step"+(i-2), gravity: 3}, {$subview:true}]}, i);
        }*/

        return form;
    }

        init() {
            var params = this.getUrl()[0].params;
            if (params.id != undefined) {
                webix.ajax().bind(this).get(beta_url + "/testitem/" + params.id, function(text, data){
                    $$('edit_test_form').setValues(data.json());
                    document.title = "Edit test " + data.json().name

                    console.log($$('edit_test_form').getChildViews()[0])
                    var ch = $$('edit_test_form').getChildViews()[0]
                    ch.data.label = "Edit test " + data.json().name
                    ch.refresh()

                    $$("cancel_button").config.click = function(){
                        this.$scope.show("/top/testitem.list." + data.json()["type"])
                    }

                    $$("edit_button").config.click = function(){
                        var valid = $$('edit_test_form').validate();
                        if (valid) {
                            webix.ajax().bind(this).post(beta_url + "/testitem/" + $$('edit_test_form').getValues()["id"], $$('edit_test_form').getValues(),
                            { error:function(text, data, XmlHttpRequest){ webix.alert("Error") },
                              success:function(text, data, XmlHttpRequest){
                                this.$scope.show("/top/testitem.list." + $$('edit_test_form').getValues()["type"])
                             } });

                        }
                    }

                });
            }
	}
}