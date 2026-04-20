*** Установка ***

cd site
python3 -m venv venv
source venv/bin/activate
pip install django

sudo iptables -A INPUT -p tcp --dport 8000 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 8001 -j ACCEPT

sudo netfilter-persistent save

python manage.py collectstatic --noinput

python manage.py runserver 0.0.0.0:8001
