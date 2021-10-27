#!/bin/bash
apt -y update
if [[ $? -ne 0 ]]; then
  echo "Fail apt update, code: $?"
  exit $?
fi

apt -y install python3 python3-venv python3-pip python-dev
if [[ $? -ne 0 ]]; then
  echo "Fail apt install, code: $?"
  exit $?
fi

python3 -m pip install --upgrade pip
if [[ $? -ne 0 ]]; then
  echo "Fail python3 pip install --upgrade pip, code: $?"
  exit $?
fi

python3 -m venv venv
if [[ $? -ne 0 ]]; then
  echo "Fail python3 -m venv venv, code: $?"
  exit $?
fi

source venv/bin/activate
if [[ $? -ne 0 ]]; then
  echo "Fail source venv, code: $?"
  exit $?
fi

python3 -m pip install -r ./requirements.txt
if [[ $? -ne 0 ]]; then
  echo "Fail python3 install requirements, code: $?"
  exit $?
fi

chown -R ./

python3 main.py
if [[ $? -ne 0 ]]; then
  echo "Fail start API, code: $?"
  exit $?
fi
