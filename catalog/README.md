# Item-Catalogue
project by
### GONUGUNTLA SAI AKHIL
# About Item-Catalogue
This contains the CRUD operations on items
# Files
1) database.py - contains the database tables and their attributes
2) inserting.py - contains the some data for the tables
3) main.py  - main python file to run the application
4) templates  - contains the html files
5) static - contains css and java script files
6) samsung.db  - database of samsung series
7) images - contains the output screens of project

# Requirements For Item-Catalogue
  [Vagrant](https://www.vagrantup.com/)
  [Udacity Vagrantfile](https://github.com/udacity/fullstack-nanodegree-vm)
  [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
  [python](https://www.python.org/downloads/)

# domain
It needs VM to run this project -- that way any changes that you make won't affect your personal machine setup.

1) Install Vagrant and Virtualbox.
2) Launch the Vagrant VM by using vagrant up in the directory.
3) Sign into the VM by using vagrant ssh in the directory.
4) This application needs dependency modules which are not present in the VM. so we need to install them by using
    pip install flask - for installing flask module
    pip install sqlalchemy  - for installing sqlalchemy module
    pip install oauth2client  - for installing oauth2client module
    pip install psycopg2  - for installing psycop2
    pip install requests  - for installing requests
5) To end the connection to the VM enter text: exit.
6) To shut down the VM while still saving your work, enter text: vagrant halt.
# How to Run
run the python file database.py by using python database.py
run the python file inserting.py by using python inserting.py
run the main python file by using python main.py
visit the google chrome and enter http://localhost:8000
# JSON endpoints
http://localhost:8000/serie/JSON  - displays all the series
http://localhost:8000/serie/<path:series_name>/serie/JSON- display specific series phones
http://localhost:8000/serie/<path:series_name>/<path:mobile_name>/JSON- display specific series and specific model
http://localhost:8000/serie/mobiles/JSON -  display all mobiles