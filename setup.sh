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

echo "SQLALCHEMY_DATABASE_URI = postgresql://scratchunderflow:WcVfe2C]Ku-s><e9,.@localhost:5432/scratchunderflow" >.env
echo "DEBUG = False" >>.env
echo "ENV = Production" >>.env
echo "SECRET_KEY = 'fc036e4bc6rev974f92bb6577ae886t1hr1t4z84verve488y7uyi78i7e6r87y87yae113'" >>.env
echo "WTF_CSRF_SECRET_KEY = 'yr4gr4e845e1g53r1g85re4g6ar4g35re4haatjar534r3e8za9r7tryrth484gnwcbx47ry7TEAYHBe7k845gfd54h75'" >>.env
echo "WTF_CSRF_CHECK_DEFAULT = False" >>.env
echo "SQLALCHEMY_TRACK_MODIFICATIONS = True" >>.env
echo "SESSION_COOKIE_SECURE = False" >>.env
echo "REMEMBER_COOKIE_SECURE = True" >>.env
echo "SESSION_COOKIE_HTTPONLY = False" >>.env
echo "WTF_CSRF_SSL_STRICT = False" >>.env
echo "SESSION_COOKIE_DOMAIN = localhost.local" >>.env
echo "PERMANENT_SESSION_LIFETIME = 24" >>.env
echo "SESSION_COOKIE_SAMESITE = None" >>.env
echo "ENABLE_CSRF = False" >>.env
echo "PORT = 8009" >>.env

python3 main.py
if [[ $? -ne 0 ]]; then
  echo "Fail start API, code: $?"
  exit $?
fi
