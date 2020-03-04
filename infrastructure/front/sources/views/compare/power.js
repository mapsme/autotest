import {JetView} from "webix-jet";
import {beta_url} from "models/beta"
import {iterationCopy, isEmpty} from "utils/func"

export default class ComparingPowerView extends JetView{
	config(){

        document.title = "Compare power tests";
		var form = {
            view:"form",  id:"comparing_form", scroll: true,
            elements: [
                { rows:[
                    {view:"fieldset", width:600, maxWidth:600, borderless: true,
                            label: "Choose comparing type",
                            body:{
                                rows:[
                                    { view:"combo", name:"compare_by", id: "compare_by", required: true, labelWidth: 200, width: 500, inputAlign: "right", labelAlign:"right", label:"Compare test results by:", value:"",
                                    options:[ "Device",  "Test", "One test average" /*, "Release" */] },
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

	init() {

	    webix.extend($$("comp_layout"), webix.ProgressBar);

	    function show_progress_icon(delay){
            $$("comp_layout").disable();
            $$("comp_layout").showProgress({
                type:"icon",
                delay:delay,
                hide:true
            });
            setTimeout(function(){
                $$("comp_layout").enable();
            }, delay);
        };


	    var test_res_list_template = {
            view:"datatable",
            maxHeight:300,
            width: 500,
            multiselect:true,
            columns: [
                {id: "checkbox", width:50, header: { content:"masterCheckbox" }, checkValue:'on', uncheckValue:'off', template:"{common.checkbox()}" },
                {id:"id",  width:150, name:"id", header: "Test result ID", template: function(obj) {
                    return '<a href="/#!/top/testresult?id='+ obj.id + '">' + obj.id + '</a>'}},
                {id:"average", name: "average", fillspace: true, header: "Average mAh"},
                {id:"time", name: "time", fillspace: true, header: "Time, minutes"}
            ],
            on:{
                onCheck:function(rowId, colId, state){
                    if (state == "on") this.select(rowId, true);
                    if (state == "off") this.unselect(rowId);
                }
            },
            select:"row"
        };


        function get_chosen_values(id) {
            var test_items = []
            var i = 0
            $$(id).eachRow(function(row){
                var record = $$(id).getItem(row);
                if (record.checkbox == "on") {
                    test_items[i] = record.id
                    i++
                }

            })
            return test_items
        }

        function wrap_test_results(id){
            $$(id).eachRow(function(row){
                var record = $$(id).getItem(row);
                webix.ajax().get(beta_url + "/average/power/" + record.id,  function(text, data){
                    var info = data.json()
                    $$(id).mapCells(record.id,"average",1,1,
                        function(value, row_id, column_id, row_ind, col_ind){
                            return info.average_charge;
                        }
                    );
                    $$(id).refresh();
                 });
            });
        }


	    $$("next1").attachEvent("onItemClick", function(){
	        var valid = $$('comparing_form').validate();
            if (valid) {

                $$("next_layout").removeView("next1")
                var chosen = $$("compare_by").getValue()
                console.log(chosen)
                if (chosen == "Test") {

                    var set = {view:"fieldset", width:600, maxWidth:600, borderless: true,
                            label:"Choose test results",
                            body:{
                                rows:[
                                    { view:"combo", id: "device", required: true, labelWidth: 200, width: 500,
                                    inputAlign: "right", labelAlign:"right", label:"Device:", value:"" },
                                    { view:"combo", id: "first_test", required: true, labelWidth: 200, width: 500,
                                    inputAlign: "right", labelAlign:"right", label:"First test item:", disabled: true, value:""},
                                    { view:"combo", id: "second_test", required: true, labelWidth: 200, width: 500,
                                     inputAlign: "right", labelAlign:"right", label:"Second test item:", disabled: true, value:""},
                                    {view: "datepicker", id: "date_from", labelWidth: 200, width: 500, format:  "%Y-%m-%d",
                                     inputAlign: "right", labelAlign:"right", label:"From:"},
                                    {view: "datepicker", id: "date_to", labelWidth: 200, width: 500, format:  "%Y-%m-%d",
                                     inputAlign: "right", labelAlign:"right", label:"To:", value: new Date()}
                                ]
                            }}
                     $$("next_layout").addView(set)

                     webix.ajax().get(beta_url + "/hardwaredevices", function(text, data){
                        var info = data.json()
                        var opts = []
                        for (var i=0; i<info.length; i++){
                            opts[i] = {id: info[i].id, value: info[i].name}
                        }
                        $$("device").define("options", opts)
                     })

                     $$("device").attachEvent("onChange", function(newv, oldv){
                        webix.ajax().get(beta_url + "/hardwaretesitems", {"device_id": newv}, function(text, data){
                            var info = data.json()
                            var opts = []
                            for (var i=0; i<info.length; i++){
                                opts[i] = {id: info[i].id, value: info[i].name}
                            }
                            $$("first_test").enable()
                            $$("first_test").setValue("")
                            $$("second_test").setValue("")
                            $$("second_test").define("placeholder", "")
                            $$("second_test").refresh()
                            $$("first_test").define("options", opts)
                        })
                     })

                     $$("first_test").attachEvent("onChange", function(newv, oldv){
                        if (newv != "") {
                            webix.ajax().get(beta_url + "/hardwaretesitems", {"device_id": $$("device").getValue(), "exclude": newv}, function(text, data){
                                var info = data.json()
                                if (info.length == 0){
                                    $$("second_test").disable();
                                    $$("second_test").define("placeholder", "There are no test items to compare!")
                                    $$("second_test").refresh()
                                } else {
                                    var opts = []
                                    for (var i=0; i<info.length; i++){
                                        opts[i] = {id: info[i].id, value: info[i].name}
                                    }
                                    $$("second_test").enable()
                                    $$("second_test").setValue("")
                                    $$("second_test").define("options", opts)
                                }
                            })
                        }
                     })

                     $$("next_layout").addView({view: "button", id: "next2", label: "Next", autowidth: true})

                    $$("next2").attachEvent("onItemClick", function(){
                        var valid = $$('comparing_form').validate();
                        var valid2 = $$("second_test").config.disabled
                        if (valid && !valid2) {
                            $$("next_layout").removeView("next2")

                             var test_res_list1 = iterationCopy(test_res_list_template);
                             test_res_list1.id = "test_result_list1"
                             var test_res_list2 = iterationCopy(test_res_list_template);
                             test_res_list2.id = "test_result_list2"


                             var set_test1 = {view:"fieldset", id: "fieldset1", width:600, maxWidth:600, borderless: true,
                                label: "Select test results for " + $$("first_test").getText(),
                                body:{
                                    rows:[
                                        { view: "forminput", name:"test_res1", body:test_res_list1
                                         }
                                    ]
                                }}

                              var set_test2 = {view:"fieldset",  width:600, maxWidth:600, borderless: true,
                                label: "Select test results for " + $$("second_test").getText(),
                                body:{
                                    rows:[
                                        { view: "forminput", name:"test_res2", body:test_res_list2
                                         }
                                    ]
                                }}


                            $$("next_layout").addView(set_test1)
                            $$("next_layout").addView(set_test2)
                            $$("next_layout").addView({view: "button", id: "go", label: "Go", autowidth: true})

                            webix.ajax().get(beta_url + "/hardwaretestresults", {"device_id": $$("device").getValue(), "test_item_id": $$("first_test").getValue(),
                                                                                 "date_from": $$("date_from").getValue(), "date_to": $$("date_to").getValue()},
                            function(text, data){
                                var options = data.json();
                                var list = $$("test_result_list1");
                                list.parse(options)
                                if (options.length == 0) {
                                    $$("test_result_list1").showOverlay("No test results found. Try other dates.");
                                }

                                wrap_test_results("test_result_list1")

                             if (isEmpty($$("test_result_list1").data.pull)) {
                                $$("go").disable()
                             }
                            });

                            webix.ajax().get(beta_url + "/hardwaretestresults", {"device_id": $$("device").getValue(), "test_item_id": $$("second_test").getValue(),
                                                                                  "date_from": $$("date_from").getValue(), "date_to": $$("date_to").getValue()},
                                function(text, data){
                                var options = data.json();
                                var list = $$("test_result_list2");
                                list.parse(options)

                                if (options.length == 0) {
                                    $$("test_result_list2").showOverlay("No test results found. Try other dates.");
                                }
                                wrap_test_results("test_result_list2")

                             if (isEmpty($$("test_result_list2").data.pull)) {
                                $$("go").disable()
                             }
                            });


                             $$("go").attachEvent("onItemClick", function(){
                                show_progress_icon(90000)
                                webix.ajax().bind(this).post(beta_url + "/jsonmetrics/power", {"first_ids": get_chosen_values("test_result_list1"),
                                                                                    "second_ids": get_chosen_values("test_result_list2"),
                                                                                    "first_name": $$("first_test").getText(),
                                                                                    "second_name": $$("second_test").getText()},
                                function(text, data){
                                    var info = data.json()
                                    this.$scope.show("/top/uuid_"+info.uuid);
                                });

                             })

                        }
                    })
                }
                if (chosen == "Device") {

                    var set = {view:"fieldset", width:600, maxWidth:600, borderless: true,
                            label:"Choose test results",
                            body:{
                                rows:[
                                    { view:"combo", id: "test_item", required: true, labelWidth: 200, width: 500,
                                    inputAlign: "right", labelAlign:"right", label:"Test item:", value:"" },
                                    { view:"combo", id: "first_device", required: true, labelWidth: 200, width: 500,
                                    inputAlign: "right", labelAlign:"right", label:"First device:", disabled: true, value:""},
                                    { view:"combo", id: "second_device", required: true, labelWidth: 200, width: 500,
                                     inputAlign: "right", labelAlign:"right", label:"Second device:", disabled: true, value:""},
                                     {view: "datepicker", id: "date_from", labelWidth: 200, width: 500, format:  "%Y-%m-%d",
                                     inputAlign: "right", labelAlign:"right", label:"From:"},
                                    {view: "datepicker", id: "date_to", labelWidth: 200, width: 500, format:  "%Y-%m-%d",
                                     inputAlign: "right", labelAlign:"right", label:"To:", value: new Date()}
                                ]
                            }}
                     $$("next_layout").addView(set)
                     webix.ajax().get(beta_url + "/hardwaretesitems", function(text, data){
                        var info = data.json()
                        var opts = []
                        for (var i=0; i<info.length; i++){
                            opts[i] = {id: info[i].id, value: info[i].name}
                        }
                        $$("test_item").define("options", opts)
                     })

                     $$("test_item").attachEvent("onChange", function(newv, oldv){
                        webix.ajax().get(beta_url + "/hardwaredevices", {"test_item_id": newv}, function(text, data){
                            var info = data.json()
                            var opts = []
                            for (var i=0; i<info.length; i++){
                                opts[i] = {id: info[i].id, value: info[i].name}
                            }
                            $$("first_device").enable()
                            $$("first_device").setValue("")
                            $$("second_device").setValue("")
                            $$("second_device").define("placeholder", "")
                            $$("second_device").refresh()
                            $$("first_device").define("options", opts)
                        })
                     })

                     $$("first_device").attachEvent("onChange", function(newv, oldv){
                        if (newv != "") {
                            webix.ajax().get(beta_url + "/hardwaredevices", {"test_item_id": $$("test_item").getValue(), "exclude": newv}, function(text, data){
                                var info = data.json()
                                if (info.length == 0){
                                    $$("second_device").disable();
                                    $$("second_device").define("placeholder", "There are no devices to compare!")
                                    $$("second_device").refresh()
                                } else {
                                    var opts = []
                                    for (var i=0; i<info.length; i++){
                                        opts[i] = {id: info[i].id, value: info[i].name}
                                    }
                                    $$("second_device").enable()
                                    $$("second_device").setValue("")
                                    $$("second_device").define("options", opts)
                                }
                            })
                        }
                     })

                      $$("next_layout").addView({view: "button", id: "next2", label: "Next", autowidth: true})
                      $$("next2").attachEvent("onItemClick", function(){
                        var valid = $$('comparing_form').validate();
                        var valid2 = $$("second_device").config.disabled
                        if (valid && !valid2) {
                            $$("next_layout").removeView("next2")

                             var test_res_list1 = iterationCopy(test_res_list_template);
                             test_res_list1.id = "test_result_list1"
                             var test_res_list2 = iterationCopy(test_res_list_template);
                             test_res_list2.id = "test_result_list2"

                             var set_test1 = {view:"fieldset",  width:600, maxWidth:600, borderless: true,
                                label: "Select test results for " + $$("test_item").getText() + " on device " + $$("first_device").getText(),
                                body:{
                                    rows:[
                                        { view: "forminput", name:"test_res1", body:test_res_list1
                                         }
                                    ]
                                }}

                              var set_test2 = {view:"fieldset",  width:600, maxWidth:600, borderless: true,
                                label: "Select test results for " + $$("test_item").getText() + " on device " + $$("second_device").getText(),
                                body:{
                                    rows:[
                                        { view: "forminput", name:"test_res2", body:test_res_list2
                                         }
                                    ]
                                }}

                            $$("next_layout").addView(set_test1)
                            $$("next_layout").addView(set_test2)
                            $$("next_layout").addView({view: "button", id: "go", label: "Go", autowidth: true})
                            webix.ajax().get(beta_url + "/hardwaretestresults", {"device_id": $$("first_device").getValue(), "test_item_id": $$("test_item").getValue(),
                                                                                 "date_from": $$("date_from").getValue(), "date_to": $$("date_to").getValue()},
                               function(text, data){
                                var options = data.json();
                                var list = $$("test_result_list1");
                                list.parse(options)
                                if (options.length == 0) {
                                    $$("test_result_list1").showOverlay("No test results found. Try other dates.");
                                }

                                wrap_test_results("test_result_list1")

                             if (isEmpty($$("test_result_list1").data.pull)) {
                                $$("go").disable()
                             }
                            });
                            webix.ajax().get(beta_url + "/hardwaretestresults", {"device_id": $$("second_device").getValue(), "test_item_id": $$("test_item").getValue(),
                                                                                 "date_from": $$("date_from").getValue(), "date_to": $$("date_to").getValue()},
                               function(text, data){
                                var options = data.json();
                                var list = $$("test_result_list2");
                                list.parse(options)
                                if (options.length == 0) {
                                    $$("test_result_list2").showOverlay("No test results found. Try other dates.");
                                }

                                wrap_test_results("test_result_list2")

                             if (isEmpty($$("test_result_list2").data.pull)) {
                                $$("go").disable()
                             }
                            });

                             $$("go").attachEvent("onItemClick", function(){
                                //полторы минуты должно быть достаточно для прогресс бара
                                webix.ajax().bind(this).post(beta_url + "/jsonmetrics/power", {"first_ids": get_chosen_values("test_result_list1"),
                                                                                    "second_ids": get_chosen_values("test_result_list2"),
                                                                                    "first_name": $$("first_device").getText(),
                                                                                    "second_name": $$("second_device").getText()},
                                function(text, data){
                                    var info = data.json()
                                    this.$scope.show("/top/uuid_"+info.uuid);
                                });
                             })
                        }
                      });
                }

                if (chosen == "One test average") {

                    var set = {view:"fieldset", width:600, maxWidth:600, borderless: true,
                            label:"Choose test results",
                            body:{
                                rows:[
                                    { view:"combo", id: "device", required: true, labelWidth: 200, width: 500,
                                    inputAlign: "right", labelAlign:"right", label:"Device:", value:"" },
                                    { view:"combo", id: "first_test", required: true, labelWidth: 200, width: 500,
                                    inputAlign: "right", labelAlign:"right", label:"Test item:", disabled: true, value:""},
                                    {view: "datepicker", id: "date_from", labelWidth: 200, width: 500, format:  "%Y-%m-%d",
                                     inputAlign: "right", labelAlign:"right", label:"From:"},
                                    {view: "datepicker", id: "date_to", labelWidth: 200, width: 500, format:  "%Y-%m-%d",
                                     inputAlign: "right", labelAlign:"right", label:"To:", value: new Date()}
                                ]
                            }}
                     $$("next_layout").addView(set)

                     webix.ajax().get(beta_url + "/hardwaredevices", function(text, data){
                        var info = data.json()
                        var opts = []
                        for (var i=0; i<info.length; i++){
                            opts[i] = {id: info[i].id, value: info[i].name}
                        }
                        $$("device").define("options", opts)
                     })

                     $$("device").attachEvent("onChange", function(newv, oldv){
                        webix.ajax().get(beta_url + "/hardwaretesitems", {"device_id": newv}, function(text, data){
                            var info = data.json()
                            var opts = []
                            for (var i=0; i<info.length; i++){
                                opts[i] = {id: info[i].id, value: info[i].name}
                            }
                            $$("first_test").enable()
                            $$("first_test").setValue("")
                            $$("first_test").define("options", opts)
                        })
                     })

                     $$("next_layout").addView({view: "button", id: "next2", label: "Next", autowidth: true})

                    $$("next2").attachEvent("onItemClick", function(){
                        var valid = $$('comparing_form').validate();
                        if (valid) {
                            $$("next_layout").removeView("next2")

                           var test_res_list = iterationCopy(test_res_list_template);
                           test_res_list.id = "test_result_list1"

                             var set_test1 = {view:"fieldset",  width:600, maxWidth:600, borderless: true,
                                label: "Select test results for " + $$("first_test").getText(),
                                body:{
                                    rows:[
                                        { view: "forminput", name:"test_res1", body:test_res_list
                                         }
                                    ]
                                }}

                            $$("next_layout").addView(set_test1)
                            $$("next_layout").addView({view: "button", id: "go", label: "Go", autowidth: true})
                            webix.ajax().get(beta_url + "/hardwaretestresults", {"device_id": $$("device").getValue(), "test_item_id": $$("first_test").getValue(),
                                                                                 "date_from": $$("date_from").getValue(), "date_to": $$("date_to").getValue()},
                               function(text, data){
                                var options = data.json();
                                var list = $$("test_result_list1");
                                list.parse(options)

                                if (options.length == 0) {
                                    $$("test_result_list1").showOverlay("No test results found. Try other dates.");
                                }

                                wrap_test_results("test_result_list1")

                             if (isEmpty($$("test_result_list1").data.pull)) {
                                $$("go").disable()
                             }
                            });

                             $$("go").attachEvent("onItemClick", function(){
                                show_progress_icon(90000)
                                webix.ajax().bind(this).post(beta_url + "/jsonmetrics/power", {"first_ids": get_chosen_values("test_result_list1"),
                                                                                    "first_name": $$("first_test").getText()},
                                function(text, data){
                                    var info = data.json()
                                    this.$scope.show("/top/uuid_"+info.uuid);
                                });
                             })

                        }
                    })
                }
            }
	    })


	}
}