import groovy.json.JsonOutput

def call(apk_name, isAndroid) {
    def build = currentBuild.rawBuild
    def upstreamCause = build.getCause(hudson.model.Cause$UpstreamCause)
    def job_name = "", build_num = "", url = "", user = "\"timer\""
    if (upstreamCause != null) {
        def by = upstreamCause.getUpstreamRun().getCause(hudson.model.Cause$UserIdCause)
        if (by != null) {
            user = "\"${by.userId}\""
            by = null
        }
        else {
            if (upstreamCause.getUpstreamRun().getCause(org.jenkinsci.plugins.ghprb.GhprbCause) != null) {
                user = "\"pull_request\""
            }
        }
        job_name = upstreamCause.getUpstreamProject()
        build_num = upstreamCause.getUpstreamBuild()
        url = env['JENKINS_URL'] + upstreamCause.getUpstreamUrl() + "${build_num}"
        upstreamCause = null
    }
    else {
        by = build.getCause(hudson.model.Cause$UserIdCause)
        if (by != null){
            user =  "\"${by.userId}\""
            by = null
        }
    }
    def beta = ""
    def release = ""
    if (isAndroid) {
        beta = apk_name.split("-")[-3]
        release = apk_name.split("-")[-2]
        def dots = release.split("\\.")
        if(dots.size() > 3) {
            def sublist = dots.toList().subList(0,3)
            release = sublist.join(".")
            print release.toString()
        }
    } else {
        beta = apk_name.split("-")[-2].toLowerCase()
    }


    def upstream_job_info = ['\"name\"': "\"${job_name}\"",
                               '\"build_number\"': "\"${build_num}\"",
                               '\"url\"': "\"${url}\"",
                               '\"started_by\"': user,
                               '\"jenkins_job\"': "\"${env['BUILD_URL']}\"",
                               '\"release\"': "\"${release}\"",
                               '\"release_type\"': "\"${beta}\""]
    return JsonOutput.toJson(upstream_job_info)
}