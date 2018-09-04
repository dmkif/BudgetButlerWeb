set -e

# Installation
cd online_install

sudo apt update
sudo apt install apache2

echo "Create virtualhost file"
python create_virtualhost.py
echo "move virtualhost file"
sudo cp budget.online.conf /etc/apache2/sites-available/
echo "installed confs:"
ls -l  /etc/apache2/sites-available/

echo "Enable site"
sudo a2ensite budget.online.conf
echo "Copy apache configuration"
sudo cp apache.conf /etc/apache2/

echo "reload apache"
sudo service apache2 reload

echo "install database"
pip install -r requirements.txt

python install_database.py
cd ..
echo "database installed"

curl 'localhost/login.php'
echo "DONE"

