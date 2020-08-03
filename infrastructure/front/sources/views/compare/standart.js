import {JetView} from "webix-jet";
import {beta_url} from "models/beta"
import {iterationCopy, isEmpty} from "utils/func"

export default class ComparingPowerView extends JetView{
	config(){

        document.title = "Compare test results";
		var form = {
            view:"form",  id:"comparing_form", scroll: true,
            elements: [
                { rows:[
                    {view:"fieldset", width:600, maxWidth:600, borderless: true,
                            label: "Choose test type",
                            body:{
                                rows:[
                                    { view:"combo", name:"compare_by", id: "compare_by", required: true, labelWidth: 200, width: 500, inputAlign: "right", labelAlign:"right", label:"Compare test results by:", value:"",
                                    options:[ "Power",  "Memory"] },
                                ]
                            }},
                     {view: "button", id: "next1", label: "Next", autowidth: true}
                     ],
                     id: "next_layout"
                }
            ]

        };

        return { type: "layout", id: "comp_layout",
            rows: [form]
        };

	}

	init(){

	function wrap_test_results(id){
	        var rows = $$(id).find(function(obj){ return obj; })
            for (var i=0; i < rows.length; i++){
                webix.ajax().bind(rows[i]).get(beta_url + "/average/" +$$("compare_by").getValue().toLowerCase() + "/" + rows[i].id,  function(text, data){
                    var info = data.json()
                    var key = $$("compare_by").getValue() == "Memory" ? "average_memory" : "average_charge"
                    $$(id).getItemNode(this.id).innerHTML = $$(id).getItemNode(this.id).innerHTML.replace("    ", info[key])
                 });

            }
        };

	$$("next1").attachEvent("onItemClick", function(){
	    var valid = $$('comparing_form').validate();
        if (valid) {
        $$("next_layout").removeView("next1")
        var set = {view:"fieldset", width:600, maxWidth:600, borderless: true,
                   label:"Choose standart",
                   body:{
                    rows:[
                        { view:"combo", id: "test_item", required: true, labelWidth: 200, width: 500,
                          inputAlign: "right", labelAlign:"right", label:"Test item:", value:"" },
                        { view:"combo", id: "device", required: true, labelWidth: 200, width: 500,
                          inputAlign: "right", labelAlign:"right", label:"Device:", disabled: true, value:""},
                        { view:"combo", id: "release", required: true, labelWidth: 200, width: 500,
                          inputAlign: "right", labelAlign:"right", label:"Release:", disabled: true, value:""},
                    ]}
                    }
        $$("next_layout").addView(set)
        webix.ajax().get(beta_url + "/standart/testitems", {"type": $$("compare_by").getValue()}, function(text, data){
                        var info = data.json()
                        var opts = []
                        for (var i=0; i<info.length; i++){
                            opts[i] = {id: info[i].id, value: info[i].name}
                        }
                        $$("test_item").define("options", opts)
                     })
        $$("compare_by").disable();

        $$("test_item").attachEvent("onChange", function(newv, oldv){
                        webix.ajax().get(beta_url + "/standart/devices", {"test_item_id": newv, "type": $$("compare_by").getValue()},
                        function(text, data){
                            var info = data.json()
                            var opts = []
                            for (var i=0; i<info.length; i++){
                                opts[i] = {id: info[i].id, value: info[i].name}
                            }
                            $$("device").enable()
                            $$("device").setValue("")
                            $$("device").define("options", opts)
                        })
                     })

        $$("device").attachEvent("onChange", function(newv, oldv){
                        webix.ajax().get(beta_url + "/standart/releases", {"test_item_id": $$("test_item").getValue(), "device_id": newv,
                                                                            "type": $$("compare_by").getValue()},
                        function(text, data){
                            var info = data.json()
                            var opts = []
                            for (var i=0; i<info.length; i++){
                                opts[i] = {id: info[i].id, value: info[i].release}
                            }
                            $$("release").enable()
                            $$("release").setValue("")
                            $$("release").define("options", opts)
                        })
                     })


        $$("next_layout").addView({view: "button", id: "next2", label: "Next", autowidth: true})
        $$("next2").attachEvent("onItemClick", function(){
                        var valid2 = $$("device").config.disabled
                        if (!valid2) {
                            $$("next_layout").removeView("next2");
                            $$("test_item").disable()
                            $$("device").disable()
                            $$("release").disable()
                            var test_res_list = {
                                view:"list",
                                id: "test_result_list",
                                maxHeight:300,
                                width: 500,

                                template: function(obj) {
                                    return '<a href="/#!/top/testresult?id='+ obj.id + '">' + obj.id
                                    + '</a>,  Average:    '+ ', Time: ' + obj.time
                                },
                                select:true

                            }

                            var set_test = {view:"fieldset", id: "fieldset1", width:600, maxWidth:600, borderless: true,
                                label: "Select test results for " + $$("test_item").getText() + ", Device " + $$("device").getText(),
                                body:{
                                    rows:[
                                        { view: "forminput", name:"test_res1", body:test_res_list
                                         }
                                    ]
                                }}

                            $$("next_layout").addView(set_test)
                            $$("next_layout").addView({view: "button", id: "go", label: "Go", autowidth: true})

                            webix.ajax().get(beta_url + "/hardwaretestresults", {"device_id": $$("device").getValue(), "test_item_id": $$("test_item").getValue(),

                                                                                 "is_memory": $$("compare_by").getValue()=="Memory" ? true : false},
                            function(text, data){
                                var options = data.json();
                                var list = $$("test_result_list");
                                list.parse(options)
                                if (options.length == 0) {
                                    $$("test_result_list").showOverlay("No test results found");
                                }

                                wrap_test_results("test_result_list")

                             if (isEmpty($$("test_result_list").data.pull)) {
                                $$("go").disable()
                             }
                            });

                            $$("test_result_list").attachEvent("onSelectChange", function() {wrap_test_results("test_result_list")})

                            $$("go").attachEvent("onItemClick", function(){
                                webix.ajax().bind(this).post(beta_url + "/standartmetrics/" + $$("compare_by").getValue().toLowerCase(), {"chosen": $$("test_result_list").getSelectedId(),
                                "device_id": $$("device").getValue(), "release_id": $$("release").getValue(), "test_item_id": $$("test_item").getValue()},
                                function(text, data){
                                    var info = data.json()
                                    this.$scope.show("/top/uuid_"+info.uuid);
                                });
                             });

                        }
        })

        }
    });


	}
}