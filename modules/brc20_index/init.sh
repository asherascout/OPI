echo REPORT_NAME="1035038185652240406" > .env

apt update
apt install supervisor
pip3 install requests
pip3 install python-dotenv

cp -a brc20_index.conf /etc/supervisor/conf.d

