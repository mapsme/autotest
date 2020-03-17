#!/bin/bash

export WORKSPACE=`pwd`

python3 -m venv ./autotest
source ./autotest/bin/activate

pip3 install -r $WORKSPACE/mapsme/requirements.txt
pip3 install $WORKSPACE/mapsme_appium-0.1-py3-none-any.whl
pytest $WORKSPACE/mapsme --rootdir $WORKSPACE/mapsme --html=report.html --log-cli-level=INFO --device-id=$1 -k "$2" --apk-name=$3 --build-number=$4 --time=$5 --session-info="$6" --clean-device=$7 --report-host=$8 --is-memory