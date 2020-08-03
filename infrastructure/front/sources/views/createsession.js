import {JetView} from "webix-jet";
import {beta_url} from "models/beta"

export default class AddTestFormView extends JetView{
	config(){
        document.title = "Create new session";

        /*var doublelist = {
           view:"datatable",
          id: "test_items_list",
          autoheight: true,
          maxHeight:300,
          width: 500,
          multiselect:true,
          columns: [
          {id: "checkbox", width:50, header:{ content:"masterCheckbox" }, checkValue:'on', uncheckValue:'off', template:"{common.checkbox()}" },
          {id:"name", header: "Test name", fillspace: true, template:"#name#"}
          ],
          on:{
            onCheck:function(rowId, colId, state){
            if (state == "on") this.select(rowId, true);
            if (state == "off") this.unselect(rowId);
            }
          },
          select:"row"
        };*/

        var combo = {
            view:"combo", name: "device", id: "device",
            required: true, labelWidth: 200, width: 500,
            inputAlign: "right", labelAlign:"right",
            label:"Select device", value:"", options: [],
            placeholder: "Select device"
        }

        var properties = { view:"property", id:"device_properties", width:500, maxWidth:500, nameWidth: 200, height: 200,
                           elements:[
                               { label:"Selected device", type:"label"},
                               { label:"Name", type:"text", id:"name"},
                               { label:"Device ID", type:"text", id:"device_id"},
                               { label:"Platform", type:"text", id:"platform_name"},
                               { label: "Platform version", type:"text", id:"platform_version"}
                            ],
                            hidden: true,
                            editable: false,
                            css: "property_qwe"
                        }

        var combo2 = {
            view:"combo", name: "test_type", id: "test_type",
            required: true, labelWidth: 200, width: 500,
            inputAlign: "right", labelAlign:"right",
            label:"Tests to run", value:"", options: ["Build check"],
            placeholder: "Select test to run"
        }

        var skip_webview = {
            view:"checkbox",
            id:"skip_webview_checkbox",
            label:"Skip webview tests",
            labelWidth: 200, width: 500,
            inputAlign: "right", labelAlign:"right",
            value:0
        }

        var build_number = { view:"text", id: "build",  name: "build", required: true, labelWidth: 200, width: 500,
                            inputAlign: "right", labelAlign:"right", label:"Build type", value:"release", placeholder:"\"beta\" or \"release\" or build number(eg 5678)" }

		var form = {
            view:"form",  id:"create_session_form", scroll: true,
            elements: [
            { view:"label", label:"Create new session", css: {"font-size": "120%"}},
            { template:"Device", type:"section"},
            { rows: [ combo, properties ] },
            /*{cols: [
                { rows: [ combo, properties ] },
                { view: "forminput", name:"test_items", body:doublelist, labelWidth: 150,
                    labelAlign:"right", label:"Select test items"
                 }
            ]},
            */
            { template:"Tests", type:"section"},
            { rows: [ combo2, skip_webview ] },
            { template:"Build", type:"section"},
            { rows: [ build_number ] },
            { cols: [
                {view: "button", label: "Start", autowidth: true, click: onStart},
                 {view: "button", label: "Cancel", autowidth: true, click: () => {this.app.show("/top/sessions.all");}}
              ]
             }
            ],
            //rules: {"test_items": validateTestItems}
        };


        function validateTestItems() {
          var valid = $$("test_items_list").getSelectedItem() != undefined;
          if (!valid) webix.message({type:"error", text:"Choose at list one test item!"});
          return valid;
          }


        function onStart() {

            var valid = $$('create_session_form').validate();
            if (valid) {
                const vals = $$('device_properties').getValues()
                //const vals2 = $$("test_items_list").getSelectedItem()

                /*var test_items = []
                if (vals2.length == undefined) test_items[0] = vals2.method_name;
                else {
                    for (var i=0;i<vals2.length;i++){
                         test_items[i] = vals2[i].method_name
                    }
                }*/

                var build_type = $$("test_type").getValue()

               if (build_type == "Build check"){
                   webix.ajax().post(beta_url + "/start/buildcheck", {"device_id": vals.device_id,
                                                                      "device_platform": vals.platform_name,
                                                                      "build_number": $$("build").getValue(),
                                                                      "skip_webview": $$("skip_webview_checkbox").getValue()});
               }

                this.$scope.show("/top/sessions.all");
            }
        }

        return form;
	}

	init() {
	    var params = this.getUrl()[0].params;
	    var url = beta_url + "/device"
	    //if (!("id" in params)) {
	        url = url + "?status=Active"
	    //}
        webix.ajax().get(url, function(text, data){
            var options = data.json();
            var new_options = []
            for (var i=0;i<options.length;i++){
                new_options[i] = {id: options[i].id, value: options[i].name + " (" + options[i].platform_name + " " + options[i].platform_version + ")"}
            }

            if (new_options.length == 0) {$$("device").disable();
            $$("device").define("placeholder", "There are no active devices!")
            $$("device").refresh()

            }
            else {

            var list = $$("device").getPopup().getList();
            list.clearAll();
            list.parse(new_options);}

            if ("id" in params) {
                webix.ajax().bind(options).get(beta_url + "/session/"+params.id, function(text, data){
                    var info = data.json();
                    console.log(this)
                    $$("device").setValue(info.device_id)
                    if (info.device_status=="Disabled") {
                        $$('device').setBottomText("Warning! Device disabled now! Please choose another!")
                    }
                    $$("build").setValue(info.release_type)
                });
            }
        });

        /*webix.ajax().get(beta_url + "/testitem", {"type": params.type}, function(text, data){
            var options = data.json();
            var list = $$("test_items_list");
            list.parse(options)

            if ("id" in params) {
                webix.ajax().get(beta_url + "/testresult", {"id": params.id}, function(text, data){
                    var options =  data.json();
                    var list = $$("test_items_list");
                    for (var i=0;i<options.length;i++){
                        list.select(options[i].test_item_id, true);
                    }

                    for (var i=0;i<options.length;i++){
                        var checkbox = list.getItemNode({row:options[i].test_item_id, column:"checkbox"}).firstChild;
                        checkbox.checked = true;
                    }

                });

            }
        }); */

        $$("device").attachEvent("onChange", function(newv, oldv){
            $$('device').setBottomText("")
            webix.ajax().get(beta_url + "/device/"+newv, function(text, data){
                var prop = $$("device_properties");
                prop.setValues(data.json());
                prop.show()
            });
        });

	}
}