
#!/bin/bash
apt -y update
if [[ $? -ne 0 ]] ; then
    echo "Fail apt update, code: $?"
    exit $?
fi

apt -y install python3 python3-venv python3-pip python-dev
if [[ $? -ne 0 ]] ; then
    echo "Fail apt install, code: $?"
    exit $?
fi

python3 -m pip install --upgrade pip
if [[ $? -ne 0 ]] ; then
    echo "Fail python3 pip install --upgrade pip, code: $?"
    exit $?
fi

python3 -m venv venv
if [[ $? -ne 0 ]] ; then
    echo "Fail python3 -m venv venv, code: $?"
    exit $?
fi

source venv/bin/activate
if [[ $? -ne 0 ]] ; then
    echo "Fail source venv, code: $?"
    exit $?
fi

python3 -m pip install -r ./requirements.txt
if [[ $? -ne 0 ]] ; then
    echo "Fail python3 install requirements, code: $?"
    exit $?
fi

echo "SQLALCHEMY_DATABASE_URI = postgresql://scratchunderflow:WcVfe2C]Ku-s><e9,.@localhost:5432/scratchunderflow" > .env
echo "DEBUG = 0" >> .env
echo "ENV = Production" >> .env
echo "SECRET_KEY = 'fc036e4bc6974f92bb6577ae886ae113'" >> .env
echo "WTF_CSRF_SECRET_KEY = 'csrf_secret_keyXXX'" >> .env
echo "WTF_CSRF_FIELD_NAME = 'X-CSRFToken'" >> .env
echo "WTF_CSRF_CHECK_DEFAULT = False" >> .env
echo "SQLALCHEMY_TRACK_MODIFICATIONS = True" >> .env
echo "SESSION_COOKIE_SECURE = True" >> .env
echo "REMEMBER_COOKIE_SECURE = True" >> .env
echo "PORT = 8009" >> .env

python3 main.py
if [[ $? -ne 0 ]] ; then
    echo "Fail start API, code: $?"
    exit $?
fi
