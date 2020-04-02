import {JetView} from "webix-jet";
import {android_ver_options} from "models/android_versions"
import {ios_ver_options} from "models/ios_versions"
import {beta_url} from "models/beta"

export default class AddDeviceFormView extends JetView{
	config(){
        document.title = "Add device";

		var form = {
            view:"form",  id:"add_device_form", scroll: true,
            elements: [
            { view:"label", label:"Add new device", css: {"font-size": "120%"}},
                { rows:[

                    { template:"Device", type:"section"},
                    { view:"text",  name: "name", required: true, labelWidth: 150, width: 500, inputAlign: "right", labelAlign:"right", label:"Name", value:"" },
                    { view:"text",  name: "device_id", required: true, labelWidth: 150, width: 500, inputAlign: "right", labelAlign:"right", label:"Device ID", value:"" },
                    { view:"combo", name: "platform_name", id: "platform_name", required: true, labelWidth: 150, width: 500, inputAlign: "right", labelAlign:"right", label:"Platform name", value:"",
                      options:[ "Android", "IOS"]
                    },

                    { view:"combo", name:"platform_version", id: "platform_version", required: true, labelWidth: 150, width: 500, inputAlign: "right", labelAlign:"right", label:"Platform version", value:"",
                        disabled: true
                    },
                    { view:"text",  name: "udid",id: "udid", labelWidth: 150, width: 500, inputAlign: "right", labelAlign:"right", label:"UDID", value:"", hidden: true },
                    { view:"combo", name: "status", required: true, labelWidth: 150, width: 500, inputAlign: "right", labelAlign:"right", label:"Status", value:"",
                        options:[ "Active", "Disabled"]
                     }
                ]},


                { cols: [
                    {view: "button", type: "submit", label: "Add", autowidth: true, click: () => {
                        var valid = $$('add_device_form').validate();
                            if (valid) {
                                webix.ajax().sync().post(beta_url + "/device", $$('add_device_form').getValues());
                                this.app.show("/top/devices.list");
                            }

                        }},
                    {view: "button", label: "Cancel", autowidth: true, click: () => {this.app.show("/top/devices");}}
                    ]
                }
            ]

        };

        return form;

	}

	init () {

	    $$("platform_name").attachEvent("onChange", function(newv, oldv){
            var ver_combo = $$('platform_version')
	        ver_combo.enable()
	        ver_combo.setValue("")

            if (newv == "Android") {
                $$('udid').setValue("")
                $$('udid').hide()
                ver_combo.define("options", android_ver_options)
            }

            else {
                $$('udid').setValue("")
                $$('udid').show()
                ver_combo.define("options", ios_ver_options)
            }
        });

	}
}