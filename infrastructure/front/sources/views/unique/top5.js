import {JetView} from "webix-jet";
import {beta_url} from "models/beta"
import Highcharts from 'highcharts';
import Exporting from 'highcharts/modules/exporting';
Exporting(Highcharts);

export default class TopUniqueCrashesView extends JetView{
    config(){
        document.title = "Top 5 crashes"

        var title = { view:"label", label:"Top 5 crashes info", css: {"font-size": "150%", "margin-left" : "50px"}}

        var properties = { type:"layout", id: "info_layout", rows: [ ]}

       return {view: "scrollview", scroll: "y", body: {
       rows: [
            {cols: [title]},
            properties
       ]}};
    }

     init() {
        webix.ajax().get(beta_url + "/crashes/top", {"period": "month", "count": 5}, function(text, data){
            var info = data.json()
            var info_layout = $$("info_layout")

                        if ($$("stats_layout") != undefined){
                            $$("stats_layout").reconstruct()
                        } else {
                            info_layout.addView({ type:"layout", id: "stats_layout", rows: [ ]})
                        }
                        var parameters = {"period": "month"}
                        var top_data = []
                            webix.ajax().bind(info.crashes).get(beta_url + "/crashes/stats/" + info.crashes[0], parameters, function(text, data){
                                 var res = data.json()
                                 var stats_layout = $$("stats_layout")
                                 if (res.len > 0){
                                     var container = { id: "container_stats", rows: [ {view:"template",
                                          template:"<div id=\"container_stats\" style=\"width:100%; height:400px;\"></div>",autoheight: true}  ]
                                     }
                                     stats_layout.addView(container);
                                     top_data[top_data.length] = {"id": "<a href=\"" + beta_url +  "#!/top/unique.crash?id=" + info.crashes[0] + "\">#"+ info.crashes[0] + "</a>",
                                                    "releases": res.releases,
                                                    "devices": res.devices,
                                                    "count": res.len}
                                     var t = chart(res, info.crashes[0])
                                     for (var i=1; i<info.crashes.length;i++) {
                                        webix.ajax().bind(info.crashes[i]).get(beta_url + "/crashes/stats/" + info.crashes[i], parameters, function(text, data){
                                            var res1 = data.json()
                                            top_data[top_data.length] = {"id": "<a href=\"#!/top/unique.crash?id=" + this + "\">#"+ this + "</a>",
                                                    "releases": res1.releases,
                                                    "devices": res1.devices,
                                                    "count": res1.len}
                                            t.addSeries({ pointStart: Date.parse(res1.start),
                                                           pointInterval: 24 * 3600 * 1000, // one day
                                                           name: "#" + this,
                                                          data: JSON.parse(JSON.stringify(res1.timeline))})
                                            if (top_data.length == 5) {
                                                console.log(top_data)

                                                var table = {
                                                    view:"datatable",
                                                    id: "top_table",
                                                      columns:[
                                                          {id:"id", header:"Number",width:100, sort:"int"},
                                                          {id:"releases", header:"Releases", fillspace:true, sort:"string"},
                                                          {id:"devices", header:"Devices",fillspace:true, sort:"string"},
                                                          {id:"count", header:"Count for period",fillspace:true, sort:"int"}
                                                          ],
                                                     data: top_data
                                                }
                                                info_layout.addView(table)
                                            }
                                        })

                                     }
                                 }
                            })

                            function chart(data, name) {
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

                                        series: [{
                                            pointStart: Date.parse(data.start),
                                            pointInterval: 24 * 3600 * 1000, // one day
                                            name: "#" + name,
                                            data: data.timeline
                                        }]
                                      });
                                      return chart2
                            }

        })
     }
}