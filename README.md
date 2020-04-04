# ossaca
Open Source Software for Animal CAre (OSSACA)

Dependencies
============
 - python3
 - flask
 - flask-image :
 `pip install flask-images`
 - sqlite
 - python3-sqlite



Running Ossaca
==============

export PYTHONPATH=$(pwd)

# On debian
env FLASK_APP=main flask run

# On fedora
env FLASK_APP=main flask-3 run
