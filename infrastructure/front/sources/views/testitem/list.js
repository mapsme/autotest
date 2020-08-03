import {JetView} from "webix-jet";
import MenuView from "views/top";
import {iterationCopy} from "utils/func"
import {beta_url} from "models/beta"

export default class TestItemsView extends JetView{
	config(){

	    document.title = "Test items list"

        var addButton = {
            view:"button",
            type:"icon",
            id: "add_item",
            icon:"mdi mdi-plus-box",
            label:"Add",
            width: 80,
            align: "left",
            click: () => {
                this.app.show("/top/testitem.add");
            }
        }



        var ui_grid = {
          view:"datatable",
          id: "mytable_ui",
          select:"cell",
          //url: beta_url + "/testitem?type=ui",
          on: {
                onAfterSelect: function(){
                if (this.getSelectedId().column == "name"){
                  var win = $$("popup")
                  if (win != undefined) win.close()
                    var selected = this.getSelectedItem()
                    var itemnode = this.getItemNode(selected.id)
                    var itempos = itemnode.getBoundingClientRect()

                      webix.ui({
                         view:"window",
                         id: "popup",
                         position:function(state){
                            state.left = itempos.left + 10
                            state.top = itempos.top + itempos.height
                            state.width = itempos.width
                         },
                         head: {cols: [{view: "label", label: "Test description"},{view:"button", label:"Close", width:70, click:("$$('popup').close();")}] },
                         body:{
                            template: function(){
                               return selected.comment
                            }
                      }}).show();
            }}},
            columns:[
              {id:"name", header:"Test name",width:650, sort:"string", dataIndex: "name"},
              {id:"method_name", header:"Method reference",width:500, sort:"string", dataIndex: "method_name"},
              {id: "actions", header: "Actions", fillspace: true, template:"{common.editIcon()} {common.trashIcon()}" }],
            onClick:{
                "wxi-pencil":function(ev, id){
                    this.$scope.show("/top/testitem.edit?id="+id.row);
                    return false;
                 },

                "wxi-trash":function(ev, id){

                    var test = this.getItem(id.row).name
                    var app = this.$scope
                    var confirmDelete = {
                        view:"window",
                        id: "confirm_delete",
                        modal:true,
                        position:"center",
                        height:250,
                        width:300,
                        head: { view: "label", template: function(){
                               return "Delete test \"" + test + "\"?"
                            }},
                        body: {
                            cols: [
                                {view:"button", label:"OK", click: () =>
                                    {
                                        webix.ajax().del(beta_url + "/testitem/"+id.row, function(text, xml, xhr){
                                            $$('confirm_delete').close();
                                            app.refresh();
                                        });
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

        function get_grid(type) {
            var new_grid = iterationCopy(ui_grid);
            new_grid.id = "mytable_" + type
            new_grid.url = beta_url + "/testitem?type=" + type
            return new_grid;
        };

        var tabview =
              {type: "layout",
              id: "main_layout",
               rows: [
               { cols: [addButton], id: "header_layout"},
               ui_grid
              // get_grid("ui")
              ]}


       return tabview;

	}
};