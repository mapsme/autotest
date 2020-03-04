import {JetView, plugins} from "webix-jet";

export default class TopView extends JetView{
	config(){

		var menu = {
			view:"menu", id:"top:menu",
			css:"app_menu",
			width:190, layout:"y", select:true,
			template:"<span class='webix_icon #icon#'></span> #value# ",
			tooltip: {
				template: function(obj){
					return obj.$count?"":obj.details;
				}
			},
			view: "tree",
			id: "sidebar",
			type: "menuTree2",
			activeTitle: true,
			select: true,
			data:[
			    {id: 1, value: "Main", icon: "mdi mdi-chevron-right", open: true, data:[
			        { id: "devices.list", value: "Devices", icon: "mdi mdi-cellphone-iphone", details:"Devices list"},
			        {id: 4, value: "Test items", details:"Test items list", icon: "mdi mdi-chevron-right", open: true, data:[
			            { id: "testitem.list.ui", value: "UI", icon: "mdi mdi-menu-right", details:"UI tests"},
			            { id: "testitem.list.hardware", value: "Hardware", icon: "mdi mdi-menu-right", details:"Power and memory tests"},
			            { id: "testitem.list.booking", value: "Booking", icon: "mdi mdi-menu-right", details:"Booking.com tests"},
			        ]},
		            {id: 5, value: "Test scopes", details:"List of test sessions", icon: "mdi mdi-chevron-right", open: true, data:[
                        { id: "sessions.all", value: "UI sessions", icon: "mdi mdi-bug-check", details:"UI and hardware sessions"},
                        //{ id: "sessions.monkey", value: "Monkey sessions", icon: "mdi mdi-android", details:"Monkey sessions"},
                        { id: "sessions.booking", value: "Booking sessions", icon: "mdi mdi-hotel", details:"Booking.com sessions"},
		            ]},
		            {id: 6, value: "Monkey tests", details:"Monkey crashes and test sessions", icon: "mdi mdi-chevron-right", open: true, data:[
                        { id: "sessions.monkey", value: "Monkey sessions", icon: "mdi mdi-android", details:"Monkey sessions"},
                        { id: "unique.list", value: "Crashes", icon: "mdi mdi-alert-circle", details:"Unique monkey crashed"},
                        { id: "unique.top5", value: "Top 5", icon: "mdi mdi-numeric-5-box", details:"Unique monkey crashed"}
		            ]}

			    ]},

		        {id: 2, value: "Comparing", icon: "mdi mdi-chevron-right", open: true, data:[
		            { id: "compare.power", value: "Power", icon: "mdi mdi-battery-unknown", details:"Compare power metrics"},
		            { id: "compare.memory", value: "Memory", icon: "mdi mdi-memory", details:"Compare memory metrics"},
		            { id: "compare.standart", value: "Standart", icon: "mdi mdi-not-equal-variant", details:"Compare memory metrics"},
		        ]},

		        /*{id: 3, value: "Release", icon: "mdi mdi-chevron-right", open: true, data:[
		            { id: "release.list", value: "Release list", icon: "mdi mdi-developer-board", details: "Current releases list"},
		            { id: "release.archive", value: "Release archive", icon: "mdi mdi-archive", details: "Archive releases list"}
		        ]}*/

			],
			on:{
				onAfterSelect:function(id){
				    $$("sidebar").unselectAll();
				    if (isNaN(parseInt(id))){
					    this.$scope.show("/top/" + id)
					}
				}
			}
		};

		var ui = {
			type:"clean", id: "container", paddingX:5,  css:"app_layout", cols:[
				{  paddingX:5, paddingY:10, rows: [ {css:"webix_shadow_medium", rows:[menu]} ]},
				{ id: "child_container", type:"clean", paddingY:10, paddingX:5, rows:[
					{ $subview:true }
				]}
			]
		};

		return ui;
	}
	init(){
		//this.use(plugins.Menu, "top:menu");
		var x = $$("container").$width
		$$("child_container").define("width", x - 200)
	}
}