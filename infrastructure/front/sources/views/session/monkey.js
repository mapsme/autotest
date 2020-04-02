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
            url: beta_url + "/monkeycrash?session_id=" + params.id,
            id: "mytable",
            select:"row",
            columns:[
              {id:"crash_number", name: "crash_number", header:"Crashes",width:300, sort:"string"}]
        }

       return {view: "scrollview", scroll: "y", body: { id: "acc_layout",
       rows: [
            {cols: [title]},
            properties,
           //test_list
       ]} };
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

        webix.ajax().get(beta_url + "/monkeycrash",  {"session_id": params.id}, function(text, data){

            var info = data.json()
            var columns = []
            for (var i=0; i<info.length; i++) {
                var text = "Crash #" +  info[i].unique_crash
                if (info[i].is_new == true) {
                    text = text + "    NEW!"
                }
                var body = "<span><b><a href=\"#!/top/unique.crash?id=" + info[i].unique_crash + "\">See crash info here</a></b></span><br><br>" + info[i].crash_text
                columns[i] = {header: text, body: {view: "scrollview", scroll: "y", height: 500, body: {rows: [ {template: body, autoheight: true}] }}, height: 500 }
            }

            var accordion = {
                view:"accordion",
                type:"wide",
                collapsed: true,
                multi:true,
                rows:columns
            }

            $$("acc_layout").addView(accordion);

        } );
    }


}