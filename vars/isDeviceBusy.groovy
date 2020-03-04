def call(device) {
    def shell = 'curl http://localhost:4723/wd/hub/sessions | python3 -c \"import sys, json; print([x[\'capabilities\'][\'deviceName\'] for x in json.load(sys.stdin)[\'value\']])\"'
    def busy = sh returnStdout: true, script: shell
    echo busy
    while (busy.toString().contains("'${device}'")) {
        echo "Device ${device} is busy"
        sleep 60
        busy = sh returnStdout: true, script: shell
    }
}