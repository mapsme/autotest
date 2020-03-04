import {JetView} from "webix-jet";
import MenuView from "views/top";
import {beta_url} from "models/beta"

export default class ReleasesArchiveView extends JetView{
	config(){
	    document.title = "Release archive"

        var grid = {
          view:"datatable",
          url: beta_url + "/release?is_archive=true",
          id: "mytable",
          select:"row",
          columns:[
              {id:"name", header:"Release name",width:500, sort:"string", dataIndex: "name"},
              {id:"status", header:"Release status", sort:"string",fillspace:true, dataIndex: "status"},
              {id: "actions", header: "Actions", fillspace:true, template:"<span class='webix_icon mdi mdi-trash-can'></span>" }],
            onClick:{

                "mdi-trash-can":function(ev, id){

                    var test = this.getItem(id.row).name
                    var confirmDelete = {
                        view:"window",
                        id: "confirm_delete",
                        modal:true,
                        position:"center",
                        height:250,
                        width:300,
                        head: "Delete release \"" + test + "\"?",
                        body: {
                            cols: [
                                {view:"button", label:"OK", click: () =>
                                    {
                                        webix.ajax().bind(this).del(beta_url + "/release/"+id.row, { error:function(text, data, XmlHttpRequest){
                                            $$('confirm_delete').close();
                                            webix.alert("Something gone wrong.")
                                        },
                                        success:function(text, data, XmlHttpRequest){
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
                 }
             }
        }


        return {type: "layout",
           rows: [
           grid
           ]};
	}


	init() {

	    $$("mytable").attachEvent("onAfterSelect", function(selection, preserve){
	            if ($$('confirm_delete') == undefined) {
	                this.$scope.show("/top/release.dashboard?id=" + selection.id);
	            }
	            else {
	                $$("mytable").unselectAll()
	            }
        })
	}
}