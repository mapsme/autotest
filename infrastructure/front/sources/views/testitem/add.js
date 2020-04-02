import {JetView} from "webix-jet";
import {beta_url} from "models/beta"

export default class AddTestFormView extends JetView{

	config(){
        document.title = "Add new test"
        var params = this.getUrl()[0].params;

		var form = {
            view:"form",  id:"add_test_form", scroll: true,
            elements: [
            { view:"label", label: "Add new test", css: {"font-size": "120%"}},
                { rows:[
                    { template:"Test name", type:"section"},
                    { view:"text", required: true,  invalidMessage:"Test name can not be empty", name: "name", label:"Name", labelWidth: 200, width: 800, inputAlign: "right",labelAlign:"right"},
                    { view:"text", required: true, invalidMessage:"Method name can not be empty",  name: "method_name", label:"Method reference", inputAlign: "right", labelWidth: 200, width: 800, labelAlign:"right" },
                    { view:"combo", name: "type", id: "type", required: true, labelWidth: 200, width: 800, inputAlign: "right", labelAlign:"right", label:"Type", value:params.type,
                      options:[ "ui", "hardware", "booking"]
                    },
                    { view:"textarea", label:"Comment", name: "comment", labelWidth: 200, width: 800, inputAlign: "right", labelAlign:"right", height: 200}
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
                    {view: "button", label: "Add", autowidth: true, click: () => {
                        var valid = $$('add_test_form').validate();
                            if (valid) {
                                webix.ajax().sync().post(beta_url + "/testitem", $$('add_test_form').getValues());
                                this.app.show("/top/testitem.list." + params.type);

                            }

                        }
                    },

                    {view: "button", label: "Cancel", autowidth: true, click: () => {this.app.show("/top/testitem.list." + params.type);}}
                    ]
                },

            ]
        };

        function addStepInput(){
            var add_step = $$('add_test_form').getChildViews()[2];
            var childs = add_step.$view.childNodes
            var i = childs.length - 1
            add_step.addView({cols:[{ view:"textarea", height:80, labelAlign:"right", labelWidth: 200, label: (i-1) + ".", value:"" , id: "step"+(i-2), gravity: 3}, {$subview:true}]}, i);
        }

        return form;
     }

}