import {JetView} from "webix-jet";
import {getJenkinsLink} from "utils/func"
import {beta_url} from "models/beta"

export default class SessionView extends JetView{
    config(){

        var params = this.getUrl()[0].params;
        document.title = "Session info"


        var title = { view:"label", label:"Session info", css: {"font-size": "150%", "margin-left" : "50px"}}
        var properties = { type:"layout", id: "info_layout", rows: []}
        var test_list = {
            view:"datatable",
            url: beta_url + "/testresult?session_id=" + params.id,
            id: "mytable",
            select:"row",
            columns:[
              {id:"test_name", header:"Test name",width:650, sort:"string", dataIndex: "build_number"},
              {id:"time_start", header:"Start time",fillspace:true, sort:"string", dataIndex: "time_start"},
              {id:"time_end", header:"End time",fillspace:true,sort:"string", dataIndex: "time_end"},
              {id:"status", name: "status", header:"Status", sort:"string",fillspace:true, dataIndex: "status" }],
        }

       var rebuild_button = {
            view:"button",
            type:"icon",
            id: "rebuild",
            icon:"mdi mdi-restart",
            label:"Rebuild",
            autowidth: true,
            align: "left",
       }

       var csv_button = {
            view:"button",
            type:"icon",
            id: "csv",
            icon:"mdi mdi-file-delimited",
            label:"CSV",
            autowidth: true,
            align: "left",
       }

       return {type: "layout",
       rows: [
            {cols: [title,  csv_button,  rebuild_button]},
            properties,
           test_list
       ]};
    }

    init() {

        function getCause(started_by, job, build_num, url) {
            if (job != null && job != ""){
                return "<span>Job " + job + "&nbsp;<a href=\"" + url + "\">#" + build_num + "</a>&nbsp; started by " + started_by + "</span>"
            }
            if (started_by != null && started_by != "") {
                return "Started by " + started_by
            }
            return null
        }

        var params = this.getUrl()[0].params;
        webix.ajax().bind(this).get(beta_url + "/session/" + params.id, function(text, data){
            var info = data.json()
            $$("rebuild").config.click = function() {this.$scope.show("/top/createsession?id=" + params.id + "&type=" + info.type);}
            $$("csv").config.click = function() {
                    window.open(beta_url + "/download/csv/" + params.id, '_blank');
            }
                 //webix.ajax().bind(this).get(beta_url + "/download/csv/" + params.id, function(text, data){)
            //}
            var info_layout = $$("info_layout")
            info_layout.addView({view: "label", label: info.status, id: "session_status", css: {"font-size": "150%", "margin-left" : "50px"}})
            var jenkins = getJenkinsLink(info.type, info.build_number)
            if (info.hasOwnProperty("jenkins_job")) {
                jenkins = getJenkinsLink(info.type, info.build_number, info.jenkins_job)
            }
            info_layout.addView({view: "label", template: "<div class=\"webix_el_box\">Build number: " + jenkins + "</div>", css: {"color": "#797a7c"}})
            info_layout.addView({view: "label", label: "Device: " + info.device_name, css: {"color": "#797a7c"}})

            var cause =  getCause(info.caused_by, info.upstream_job, info.upstream_build_number, info.upstream_url)
            if (cause != null) info_layout.addView({view: "label", label: "Caused by: " + cause, css: {"color": "#797a7c"}})
            info_layout.addView({view: "label", label: "Time start: " + info.time_start, css: {"color": "#797a7c"}})
            info_layout.addView({view: "label", label: "Time end: " + info.time_end, css: {"color": "#797a7c"}})

            var css = null
            if (info.status == "Passed") css = "status_passed";
            if (info.status == "Failed") css = "status_failed";
            if (info.status == "In progress") css = "status_inprogress";
            $$("session_status").define("css", css)
        })

        function reload() {

            setTimeout(function () {
                $$("mytable").load(beta_url + "/testresult?session_id=" + params.id)
                reload();
            }, 30000);
        }

        reload();

        $$("mytable").attachEvent("onAfterLoad", function(){
            $$("mytable").eachRow(function(row){
                var record = $$("mytable").getItem(row);
                var css = null
                if (record.status == "Passed") css = "status_passed";
                if (record.status == "Failed") css = "status_failed";
                if (record.status == "In progress") css = "status_inprogress";
                $$("mytable").addCellCss(record.id, "status", css);
                $$("mytable").refresh();
        }, true);

        });

        $$("mytable").attachEvent("onAfterSelect", function(selection, preserve){
                console.log(selection)
                this.$scope.show("/top/testresult?id=" + selection.id)
        });
    }



}
