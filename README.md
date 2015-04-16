# gems
Gymkhana Election Management System

#requirements
Python 2.7 with Django framework
Python libraries: xlrd, xlsxwriter and crypto

The following command should install everything in Ubuntu
sudo apt-get install python2.7 python-django python-xlrd python-xlsxwriter python-crypto
or use pip to install the libraries

## How to contribute
### Load database

#refreshing the database
rm db.sqlite3
python manage.py shell <dummydata.py
#note the above command will not generate an admin account. To do that make 'interactive = True' in dummydata.py and copy-paste dummydata.py in `python manage.py shell`

Run
```
python manage.py shell < dummydata.py
```
