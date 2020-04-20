#!/bin/bash

export WORKSPACE=`pwd`

python3 -m venv ./autotest
source ./autotest/bin/activate

pip3 install -r requirements.txt
pip3 install $WORKSPACE/mapsme_appium-0.1-py3-none-any.whl
pytest $WORKSPACE/mapsme --rootdir $WORKSPACE/mapsme --html=report.html --log-cli-level=INFO -k "test_monkey" --clean-device=true --device-id $1 --apk-name $2 --monkey-time $3 --apk-version $4 --apk-type $5 --report-host $6 --session-info="$7" --build-number=$8
