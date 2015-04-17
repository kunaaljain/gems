# Gems
Gymkhana Election Management System

# Requirements
Python 2.7 with Django framework
Python libraries: xlrd, xlsxwriter and crypto

## Installation

The following command should install everything in Ubuntu

### For Debians based systems:
```
sudo apt-get install python2.7 python-django python-xlrd python-xlsxwriter python-crypto
```
OR
```
pip -E install django xlrd xlsxwriter crypto
```
### Load database

#### Refreshing the database
```
rm db.sqlite3
```
```
python manage.py shell <dummydata.py
```
Note the above command will not generate an admin account. To do that make 'interactive = True' in dummydata.py then run
```
python manage.py shell < dummydata.py
```
