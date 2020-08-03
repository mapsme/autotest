import {JetView} from "webix-jet";
import MenuView from "views/top";
import {beta_url} from "models/beta"

export default class DevicesListView extends JetView{
	config(){

	    document.title = "Devices"

        var addButton = {
            view:"button",
            type:"icon",
            icon:"mdi mdi-plus-box",
            label:"Add",
            width: 80,
            align: "left",
            click: () => {
                this.app.show("/top/devices.add");
            }
        }

        var refreshButton = {
            view:"button",
            type:"icon",
            icon:"mdi mdi-cached",
            label:"Refresh",
            tooltip: "Might take some time. Please wait a minute before refreshing a page.",
            autowidth: true,
            align: "left",
            click: () => {
                webix.ajax().post(beta_url + "/start/refresh", {
                    error:function(text, data, XmlHttpRequest){
                        alert(data.json().error);
                    },
                    success:function(text, data, XmlHttpRequest){
                        $$('mytable').load("/device")
                        $$('mytable').callEvent("onAfterLoad")
                    }
                });
            }
        }



        var grid = {
          view:"datatable",
          url: beta_url + "/device",
          id: "mytable",
          select:"row",
          columns:[
              {id:"name", header:"Device name",width:230, sort:"string", dataIndex: "name"},
              {id:"device_id", header:"Device ID",width:180, sort:"string", dataIndex: "device_id"},
              {id:"udid", header:"UDID",width:330, sort:"string", dataIndex: "udid"},
              {id:"platform_name", header:"Platform name",fillspace:true, sort:"string", dataIndex: "platform_name"},
              {id:"platform_version", header:"Platform version",fillspace:true,sort:"string", dataIndex: "platform_version"},
              {id:"status", header:"Status", sort:"string",fillspace:true, dataIndex: "status"},
              {id:"battery_level", header:"Battery level, %", template: function(obj){if(obj.battery_level==-1 || obj.battery_level==null) return ""; else return obj.battery_level;}, fillspace:true},

              {id: "actions", header: "Actions", width:80, template:"<span class='webix_icon mdi mdi-pencil'></span> <span class='webix_icon mdi mdi-trash-can'></span> <span class='webix_icon mdi mdi-close'></span>" }],
            onClick:{
                "mdi-pencil":function(ev, id){
                    this.$scope.show("/top/devices.edit?id="+id.row);
                    return false;
                 },

                "mdi-trash-can":function(ev, id){

                    var test = this.getItem(id.row).name
                    var confirmDelete = {
                        view:"window",
                        id: "confirm_delete",
                        modal:true,
                        position:"center",
                        height:250,
                        width:300,
                        head: { view: "label", template: function(){
                               return "Delete device \"" + test + "\"?"
                            }},
                        body: {
                            cols: [
                                {view:"button", label:"OK", click: () =>
                                    {
                                        webix.ajax().bind(this).del(beta_url + "/device/"+id.row, { error:function(text, data, XmlHttpRequest){
                                            $$('confirm_delete').close();
                                            if (XmlHttpRequest.status == 418) webix.alert("There are sessions linked to this device");
                                            else webix.alert("Error")
                                        },
                                        success:function(text, data, XmlHttpRequest){
                                            console.log(this)
                                                $$('confirm_delete').close();
                                                this.$scope.refresh();
                                         } });
                                    }
                                },
                                {view:"button", label:"Close", click:("$$('confirm_delete').close();")}
                            ]
                        }
                    }
                    webix.ui(confirmDelete).show();
                    return false;
                 },

                 "mdi-close":function(ev, id){

                    var test = this.getItem(id.row).name
                    var confirmDelete = {
                        view:"window",
                        id: "confirm_kill_session",
                        modal:true,
                        position:"center",
                        height:250,
                        width:300,
                        head: { view: "label", template: function(){
                               return "Kill appium session for device \"" + test + "\"?"
                            }},
                        body: {
                            cols: [
                                {view:"button", label:"OK", click: () =>
                                    {
                                        webix.ajax().bind(this).post(beta_url + "/device/kill/"+id.row, { error:function(text, data, XmlHttpRequest){
                                            $$('confirm_kill_session').close();
                                            webix.alert("Error")
                                        },
                                        success:function(text, data, XmlHttpRequest){
                                            console.log(this)
                                                $$('confirm_kill_session').close();
                                                this.$scope.refresh();
                                         } });
                                    }
                                },
                                {view:"button", label:"Close", click:("$$('confirm_kill_session').close();")}
                            ]
                        }
                    }
                    webix.ui(confirmDelete).show();
                    return false;
                 }
            }
        }

       return {type: "layout",
       rows: [
       { cols: [ addButton,
       refreshButton]},
       grid
       ]};

	}

	init() {
	    $$("mytable").attachEvent("onAfterLoad", function(){
            $$("mytable").eachRow(function(row){
                var record = $$("mytable").getItem(row);
                var css = null
                if (record.status == "Active") css = "status_active";
                if (record.status == "Disabled") css = "status_inprogress";
                $$("mytable").addCellCss(record.id, "status", css);
                $$("mytable").refresh();
        }, true);

        });
	}
};