import {JetView} from "webix-jet";
import {beta_url} from "models/beta"
import Highcharts from 'highcharts';
import Exporting from 'highcharts/modules/exporting';
Exporting(Highcharts);
import * as ExpOff from "highcharts/modules/offline-exporting";
ExpOff(Highcharts)
import * as ExpLocal from "highcharts/modules/export-data";
ExpLocal(Highcharts)

export default class AveragePowerComparingView extends JetView{
    config(){
        document.title = "Average result";
        var title = { view:"label", label:"Average result", css: {"font-size": "150%", "margin-left" : "50px"}}
        var properties = { type:"layout", id: "info_layout", rows: []}

       return {type: "layout",
       rows: [
            {cols: [title]},
            properties
       ]};
    }

    init() {
            var uuid = this.getUrl()[0].page.split("uuid_")[1];
            console.log(this.getUrl())
            console.log(uuid)
            function add_warning(type, diff) {
                if (diff != undefined){
                    if (diff > 10) {
                        $$("info_layout").addView({view: "label", label: "Warning! Average " + type + " difference is " + diff +"%",
                                             id: "warning_label"}, 0)
                        $$("warning_label").getNode().firstElementChild.style.color="#f54242"
                    }
                }
            }

            webix.ajax().get(beta_url + "/comparing/result", {"uuid": uuid}, function(text, data){
                var info = data.json()
                var info_layout = $$("info_layout")

                function add_average(ave, label) {
                    info_layout.addView({view: "label", label: label + ave}, info_layout.getChildViews().length-1)
                }
                if (info.type == "hardware") {
                    add_warning("charge", info.diff)
                    add_average(info.data.first.average, "Average charge " + info.data.first.name + " (mAh): ")
                    if (info.data.second != undefined){
                        add_average(info.data.second.average, "Average charge " + info.data.second.name + " (mAh): ")
                    }


                    var tabview = { view:"tabview",
                      cells:[
                        {
                          header:"Electric charge",
                          body:{ id: "container_charge", rows: [ {view:"template",
                          template:"<div id=\"container_charge\" style=\"width:100%; height:400px;\"></div>",autoheight: true}  ]
                         }
                         },
                         {
                          header:"Energy",
                          body:{ id: "container_energy", rows: [ { view:"template", id: "container_energy_id",
                          template:"<div id=\"container_energy\" style=\"width:100%; height:400px;\"></div>",autoheight: true} ]
                          }
                         }, {

                          header:"Electric current",
                          body:{ id: "container_current", rows: [ { view:"template", id: "container_current_id",
                          template:"<div id=\"container_current\" style=\"width:100%; height:400px;\"></div>",autoheight: true} ] }
                        },
                        {
                          header:"Voltage",
                          body:{ id: "container_voltage", rows: [ {view:"template", id: "container_voltage_id",
                          template:"<div id=\"container_voltage\" style=\"width:100%; height:400px;\"></div>",autoheight: true} ] }
                        },
                         {
                          header:"Power",
                          body:{ id: "container_power", rows: [ { view:"template", id: "container_power_id",
                          template:"<div id=\"container_power\" style=\"width:100%; height:400px;\"></div>",autoheight: true} ] }
                        }
                      ]

                    }

                    $$("info_layout").addView(tabview);

                    render_chart("charge", "mAh", info.data);

                     $$("container_current_id").attachEvent("onAfterRender", function() {
                         render_chart("current", "A", info.data);
                     });

                      $$("container_voltage_id").attachEvent("onAfterRender", function() {
                          render_chart("voltage", "V", info.data);
                     });

                      $$("container_energy_id").attachEvent("onAfterRender", function() {
                          render_chart("energy", "mWh", info.data);
                     });

                     $$("container_power_id").attachEvent("onAfterRender", function() {
                        render_chart("power", "W", info.data);
                     });

                     }



                     if (info.type=="memory") {
                        add_warning("memory", info.diff)
                        add_average(info.data.first.average, "Average memory " + info.data.first.name + " (Mb): ")
                        if (info.data.second != undefined){
                            add_average(info.data.second.average, "Average memory " + info.data.second.name + " (Mb): ")
                        }

                        var container = { id: "container_memory", rows: [ {view:"template",
                          template:"<div id=\"container_memory\" style=\"width:100%; height:400px;\"></div>",autoheight: true}  ]
                            }


                        $$("info_layout").addView(container);

                         render_chart("memory", "Mb", info.data);
                     }


                     function render_chart(type, unit, metrics) {
                                 var first_name = metrics.first.name
                                 var metrics_first = metrics.first[type]
                                 var chart2 = Highcharts.chart('container_' + type, {
                                    chart: { type: 'spline' },
                                    title: { text: type },
                                    xAxis: {
                                        title: { text: 'Time, seconds' },
                                    },
                                    yAxis: {
                                        title: { text: type + ', ' + unit }
                                    },
                                    credits: { enabled: false },
                                    exporting: { url: "http://autotest.mapsme.cloud.devmail.ru/highchartsprint" },
                                    series: [{
                                        name: first_name,
                                        data: JSON.parse(JSON.stringify(metrics_first.sec))
                                    }]
                                });

                                $$("container_" + type).addView({cols: [
                                     {view: "button", id: "onesec_" + type, label: "Interval in seconds", autowidth: true},
                                     {view: "button", id:"onemin_" + type, label: "Interval in minutes", autowidth: true}]
                                 })

                                  if (metrics.second != undefined) {
                                    var compare_metrics = JSON.parse(JSON.stringify(metrics.second[type]))
                                        var sec_name = metrics.second.name
                                        chart2.addSeries({ name: sec_name,
                                        data: JSON.parse(JSON.stringify(compare_metrics.sec))})

                                        $$("onemin_" + type).attachEvent("onItemClick", function() {
                                            oneminInterval(chart2,  JSON.parse(JSON.stringify(metrics_first.min)),  JSON.parse(JSON.stringify(compare_metrics.min)));
                                          });

                                          $$("onesec_" + type).attachEvent("onItemClick", function() {
                                            onesecInterval(chart2, JSON.parse(JSON.stringify(metrics_first.sec)), JSON.parse(JSON.stringify(compare_metrics.sec)));
                                          });
                                  }
                                  else {
                                    $$("onemin_" + type).attachEvent("onItemClick", function() {
                                            oneminInterval(chart2,  JSON.parse(JSON.stringify(metrics_first.min)));
                                          });

                                          $$("onesec_" + type).attachEvent("onItemClick", function() {
                                            onesecInterval(chart2, JSON.parse(JSON.stringify(metrics_first.sec)));
                                          });
                                  }

                     }


                     function oneminInterval(chart, data, compare_to_data) {
                     var newData = data.slice()


                        chart.update({
                        xAxis: {
                                    title: { text: 'Time, minutes' }
                                }
                        }, true);


                        chart.series[0].setData(newData)

                        if (compare_to_data != undefined) {
                            chart.series[1].setData(compare_to_data)
                        }

                      }

                      function onesecInterval(chart, data, compare_to_data) {

                       var newData = data.slice()
                        chart.update({
                        xAxis: {
                                    title: { text: 'Time, seconds' }
                                }
                        }, true);

                        chart.series[0].setData(newData)

                        if (compare_to_data != undefined) {
                            chart.series[1].setData(compare_to_data)
                        }

                }
            })

    }
}