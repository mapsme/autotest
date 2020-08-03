import MenuView from "views/top";
import TestItemsView from "views/testitem/list"
import {iterationCopy} from "utils/func"
import {beta_url} from "models/beta"
import {help_button, handleHelpPopup} from "models/templates"

export default class TestItemsUIView extends TestItemsView{


	init(){
	    console.log($$("header_layout"))
	    $$("header_layout").addView({view:"combo", label:"Filter by marker:", value: "",
	                                options:[], id: "mark_filter", labelAlign:"right",
	                                labelWidth: 150, width: 300}
	                                )
	    $$("header_layout").addView(help_button)

	    $$("help_button").attachEvent("onItemClick", function(){
	        handleHelpPopup("help_button", "help_popup", "You can filter test items by marks")
	    })

	    webix.ajax().get(beta_url + "/markers", {"type": "ui"}, function(text, data){
            $$("mark_filter").define("options", data.json())
        })

	    $$("mark_filter").attachEvent("onChange", function(newv, oldv){
	        if(newv != ""){
                $$("mytable_ui").clearAll()
                $$("mytable_ui").load(beta_url + "/testitem?type=ui&marker=" + newv)
                if ($$("clear_filter") == undefined){
                    $$("header_layout").addView({view:"button", type:"icon", id: "clear_filter",
                                                icon: "mdi mdi-close", width: 40, tooltip: "Clear filter",
                                                css: "webix_transparent.webix_button"})
                    $$("clear_filter").attachEvent("onItemClick", function(){
                        $$("mark_filter").setValue("")
                        $$("mytable_ui").clearAll()
                        $$("mytable_ui").load(beta_url + "/testitem?type=ui")
                        $$("clear_filter").hide()
                    })
                } else {
                    $$("clear_filter").show()
                }
            }
        });
	    $$("mytable_ui").load(beta_url + "/testitem?type=ui")
	    $$("add_item").config.click = () => {
                this.app.show("/top/testitem.add?type=ui");
        }
	}
};