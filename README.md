*** Установка ***

cd site
python3 -m venv venv
source venv/bin/activate
pip install django

# Для мониторинга папки с рисунками
pip install watchdog channels channels-redis
pip install watchdog channels channels-redis daphne

django-admin startproject core .

python3 manage.py startapp main

sudo iptables -A INPUT -p tcp --dport 8000 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 8001 -j ACCEPT

sudo netfilter-persistent save

python3 manage.py collectstatic --noinput

python3 manage.py runserver 0.0.0.0:8001


# Устанавливаем права на скачивание
chmod 644 downloads/download.txt

# Дать права папке на запись в неё через WinSCP
chmod 777 ./downloads
