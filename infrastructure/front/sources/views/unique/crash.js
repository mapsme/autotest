import {JetView} from "webix-jet";
import {beta_url} from "models/beta"
import Highcharts from 'highcharts';
import Exporting from 'highcharts/modules/exporting';
Exporting(Highcharts);

export default class UniqueCrashView extends JetView{
    config(){
        document.title = "Monkey crash"

        var title = { view:"label", label:"Crash info", css: {"font-size": "150%", "margin-left" : "50px"}}

        var properties = { type:"layout", id: "info_layout", rows: [ ]}

       return {view: "scrollview", scroll: "y", body: {
       rows: [
            {view: "button", id: "goBack", label: "Back to list", autowidth: true, type:"icon", icon:"mdi mdi-arrow-left",},
            {cols: [title]},
            properties
       ]}};
    }

     init() {
        var global_charts={};
        var params = this.getUrl()[0].params;
        webix.ajax().bind(params).get(beta_url + "/crashes/unique/" + params.id, function(text, data){
            var info = data.json()
            var info_layout = $$("info_layout")
            $$("goBack").config.click = function(){this.$scope.show("/top/unique.list");}
            //info_layout.addView({view: "label", label: info.status, id: "test_status", css: {"font-size": "150%", "margin-left" : "50px"}})
            info_layout.addView({view: "label", label: "Crash #" + info.id})
            info_layout.addView({view: "label", label: "Time of first crash: " + info.date})
            info_layout.addView({view: "label", label: "Release: " + info.release})
            info_layout.addView({view: "label", label: "Device: " + info.device_name})

            var text = info.crash_text.split("\n").join("<br>")

            var column  = {header: "Crash text", body: {view: "scrollview", scroll: "y", height: 500, body: {rows: [ {template: text, autoheight: true, id: "acc"}] }}, height: 500 }

            var accordion = {
                view:"accordion",
                type:"wide",
                collapsed: true,
                multi:true,
                rows:[column]
            }

            info_layout.addView(accordion);

            info_layout.addView({view: "label", label: "Crash stats"})
            info_layout.addView({id: "filter_layout", view:"form", cols: [{view:"combo", name: "period", id: "period", labelWidth: 180, width: 300,
                                inputAlign: "left", labelAlign:"right", label:"Show stats for period:", value:"all",
                      options:[ "all", "month", "release"]},
                      {view: "button", id: "show_stats", label: "Go", autowidth: true, click: () => {

                        if ($$("stats_layout") != undefined){
                            $$("stats_layout").reconstruct()
                        } else {
                            info_layout.addView({ type:"layout", id: "stats_layout", rows: [ ]})
                        }
                        var parameters = {"period": $$("period").getValue()}
                        if ($$("release") != undefined) {
                            parameters["release"] = $$("release").getValue()
                        }
                        var valid = $$("filter_layout").validate()
                        if (valid) {
                            webix.ajax().bind(this).get(beta_url + "/crashes/stats/" + params.id, parameters, function(text, data){
                                 var info = data.json()
                                 var stats_layout = $$("stats_layout")
                                 stats_layout.addView({view: "label", label: "Crashes for this period: " + info.len})
                                 if (info.len > 0){
                                     var container = { id: "container_stats", rows: [ {view:"template",
                                          template:"<div id=\"container_stats\" style=\"width:100%; height:400px;\"></div>",autoheight: true}  ]
                                     }
                                     stats_layout.addView({view: "label", label: "Releases: " + info.releases})
                                     stats_layout.addView({view: "label", label: "Devices: " + info.devices})
                                     stats_layout.addView(container);
                                     var chart2 = Highcharts.chart('container_stats', {
                                        chart: { type: 'spline' },
                                        title: { text: "Crashes" },
                                        xAxis: {
                                            type: 'datetime',
                                            title: { text: 'Date' }
                                        },
                                        yAxis: {
                                            title: { text: 'Crashes count' }
                                        },
                                        credits: { enabled: false },
                                        exporting: { enabled: false },
                                        plotOptions: {
                                            series: {
                                                pointStart: Date.parse(info.start),
                                                pointInterval: 24 * 3600 * 1000 // one day
                                                //connectNulls: true
                                            }
                                        },
                                        series: [{
                                            name: "#" + params.id,
                                            data: info.timeline
                                        }]
                                      });
                                 }
                            })
                       }
                      }
             }]})

             $$("period").attachEvent("onChange", function(newv, oldv){
                 if (newv == "release") {
                    $$("filter_layout").addView({view:"combo", name: "release", id: "release", width: 100, required: true,
                                inputAlign: "left", value:"", options:[]}, $$("filter_layout").getChildViews().length-1)
                    webix.ajax().get(beta_url + "/crashes/releases/" + params.id, function(text, data){
                        $$("release").define("options", data.json())
                    })
                 } else {
                    if ($$("release") != undefined) {
                        $$("release").destructor()
                        $$("filter_layout").getChildViews().splice(1, 1)
                        console.log($$("filter_layout").getChildViews())
                    }
                 }
             });
        })
     }
}