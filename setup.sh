# This file sets up the virtual environment.
# Run "source setup.sh" each time you want to run the app.
# This file is all the requirements needed to run the app
# Add packages here as you install to do development


if [ ! -d venv ]
then
  virtualenv -p python3.6 venv
fi

. venv/bin/activate

sudo apt-get install python3-dev libmysqlclient-dev python3-all-dev

pip install Flask
pip install sqlalchemy
pip install flask_sqlalchemy
pip install mysqlclient
pip install sqlalchemy-migrate
pip install flask_wtf
pip install Flask-Mail
pip install Flask-Misaka
pip install steem

sed -i '44s/.*/Requires-Dist: toml (==0.9.3)/' ./venv/lib/python3.5/site-packages/steem-0.18.103.dist-info/METADATA
