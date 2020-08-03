export function iterationCopy(src) {
    let target = {};
    for (let prop in src) {
        if (src.hasOwnProperty(prop)) {
            if (typeof(src[prop]) == "object") {
             if (src[prop] instanceof Array){
                target[prop] = JSON.parse(JSON.stringify(src[prop]))
             }
             else {
                target[prop] = iterationCopy(src[prop]);
             }
           }
        else {
            target[prop] = src[prop];
        }
        }
    }
    return target;
}

export function getJenkinsLink(type, buildNumber, job) {
     if (job != undefined && job != null) {
        return "<a href=\"" + job + "\">#" + buildNumber + "</a>";
     }
     var jobName = "ui-test-android"
     if (type == "hardware") {
        jobName = "power-test-android"
     }
     //console.log("job name = " + jobName + " job type = " + type)
     return "<a href=\"http://coruscant.mapsme.cloud.devmail.ru/jenkins/view/Autotest/job/"
        + jobName + "/" + buildNumber + "\">#" + buildNumber + "</a>";

}


export function isEmpty(obj){
    return Object.keys(obj).length === 0 && obj.constructor === Object
}