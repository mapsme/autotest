import {JetView} from "webix-jet";
import {beta_url} from "models/beta"
import Highcharts from 'highcharts';
import Exporting from 'highcharts/modules/exporting';
Exporting(Highcharts);

export default class TestResultView extends JetView{
    config(){
        document.title = "Test result info"

        var title = { view:"label", label:"Test result info", css: {"font-size": "150%", "margin-left" : "50px"}}

        var properties = { type:"layout", id: "info_layout", rows: [ ]}

       return {view: "scrollview", scroll: "y", body: {
       rows: [
            {view: "button", id: "goBack", label: "Back to session", autowidth: true, type:"icon", icon:"mdi mdi-arrow-left",},
            {cols: [title]},
            properties
       ]}};
    }

    init() {
        var global_charts={};
        var params = this.getUrl()[0].params;
        webix.ajax().bind(params).get(beta_url + "/testresult/" + params.id, function(text, data){
            var info = data.json()
            var info_layout = $$("info_layout")
            $$("goBack").config.click = function(){this.$scope.show("/top/session.hardware?id="+info.session_id);}
            info_layout.addView({view: "label", label: info.status, id: "test_status", css: {"font-size": "150%", "margin-left" : "50px"}})
            info_layout.addView({view: "label", label: "Test name: " + info.test_name, css: {"color": "#797a7c"}})
            info_layout.addView({view: "label", label: "Time start: " + info.time_start, css: {"color": "#797a7c"}})
            info_layout.addView({view: "label", label: "Time end: " + info.time_end, css: {"color": "#797a7c"}})
            info_layout.addView({ type:"layout", id: "ave_layout", rows: [ ]})
            var css = null
            if (info.status == "Passed") css = "status_passed";
            if (info.status == "Failed") css = "status_failed";
            if (info.status == "In progress") css = "status_inprogress";
            $$("test_status").define("css", css)

            if (info.type == "hardware") {

                if (info.is_memory_test == true) {
                    var container = { id: "container_meminfo", rows: [ {view:"template",
                          template:"<div id=\"container_meminfo\" style=\"width:100%; height:400px;\"></div>",autoheight: true}  ]
                    }


                    webix.ajax().get(beta_url + "/meminfo/" + info.id, function(text, data){
                             $$("info_layout").addView(container);
                             const metrics = data.json()
                             if(JSON.stringify(metrics) != JSON.stringify({})){
                                 $$("ave_layout").addView({view: "label", label: "Average memory (Mb): " + data.json().average})
                                 var chart2 = Highcharts.chart('container_meminfo', {
                                    chart: { type: 'spline' },
                                    title: { text: "Memory usage" },
                                    xAxis: {
                                        title: { text: 'Time, seconds' },
                                    },
                                    yAxis: {
                                        title: { text: 'Memory usage, Mb' }
                                    },
                                    credits: { enabled: false },
                                    exporting: { enabled: false },
                                    series: [{
                                        name: "Memory",
                                        data: JSON.parse(JSON.stringify(metrics.meminfo))
                                    }]
                                });
                            }
                          });
                }

                if (info.is_power_test == true || info.is_power_test == null) {

                webix.ajax().get(beta_url + "/average/power", {"test_result_id": info.id}, function(text, data){
                    console.log( info_layout.getChildViews())
                    console.log(info_layout.getChildViews())
                    $$("ave_layout").addView({view: "label", label: "Average charge (mAh): " + data.json().average_charge})
                });

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
                     const compare_to = this.compare_to
                     render_chart("charge", "mAh", compare_to);

                     $$("container_current_id").attachEvent("onAfterRender", function() {
                         render_chart("current", "A", compare_to);

                     });

                      $$("container_voltage_id").attachEvent("onAfterRender", function() {
                          render_chart("voltage", "V", compare_to);
                     });

                      $$("container_energy_id").attachEvent("onAfterRender", function() {
                          render_chart("energy", "mWh", compare_to);
                     });

                     $$("container_power_id").attachEvent("onAfterRender", function() {
                        render_chart("power", "W", compare_to);
                     });

                     function render_chart(type, unit, compare_to) {

                        webix.ajax().get(beta_url + "/metricsraw/" + info.id,  {"key": type}, function(text, data){
                             const metrics = data.json()
                             if(JSON.stringify(metrics) != JSON.stringify({})){
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
                                    exporting: { enabled: false },
                                    series: [{
                                        name: "Raw " + type,
                                        data: JSON.parse(JSON.stringify(metrics.sec))
                                    }]
                                });


                                $$("container_" + type).addView({cols: [
                                     {view: "button", id: "onesec_" + type, label: "Interval in seconds", autowidth: true},
                                     {view: "button", id:"onemin_" + type, label: "Interval in minutes", autowidth: true}]
                                 })

                                  $$("onemin_" + type).attachEvent("onItemClick", function() {
                                    oneminInterval(chart2, JSON.parse(JSON.stringify(metrics.min)));
                                  });

                                  $$("onesec_" + type).attachEvent("onItemClick", function() {
                                    onesecInterval(chart2, JSON.parse(JSON.stringify(metrics.sec)));
                                  });

                                   console.log(compare_to)

                                  if (compare_to != undefined) {

                                      webix.ajax().get(beta_url + "/metricsraw/" + compare_to,  {"key": type}, function(text, data){
                                        var compare_metrics = data.json()
                                        chart2.addSeries({ name: compare_to,
                                        data: JSON.parse(JSON.stringify(compare_metrics.sec))})

                                        $$("onemin_" + type).attachEvent("onItemClick", function() {
                                            oneminInterval(chart2,  JSON.parse(JSON.stringify(metrics.min)),  JSON.parse(JSON.stringify(compare_metrics.min)));
                                          });

                                          $$("onesec_" + type).attachEvent("onItemClick", function() {
                                            onesecInterval(chart2, JSON.parse(JSON.stringify(metrics.sec)), JSON.parse(JSON.stringify(compare_metrics.sec)));
                                          });
                                      });
                                  }

                              }
                          });
                     }



                     function oneminInterval(chart, data, compare_to_data) {
                     var newData = data.slice()


                        chart.update({
                        xAxis: {
                                    title: { text: 'Time, minutes' },
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
                                    title: { text: 'Time, seconds' },
                                }
                        }, true);

                        chart.series[0].setData(newData)

                        if (compare_to_data != undefined) {
                            chart.series[1].setData(compare_to_data)
                        }

                      }
                }
            }
            if (info.type == "booking") {
                var bookings = {
                      view:"datatable",
                      select:"row",
                      url: beta_url + "/booking?test_result_id=" + params.id,
                      columns:[
                          {id:"name", header:"Hotel name",width:300, sort:"string"},
                          {id:"booking_time", header:"Time of booking",width:200, sort:"string"},
                          {id:"status", header:"Status",fillspace:true, sort:"string"},
                          {id:"reservation_id", header:"Reservation id",fillspace:true},
                      ]
                }
                info_layout.addView(bookings)
                console.log("this is booking test")
            }
        })
    }
}