#!/bin/bash
#Build and run


echo Setting up Virtual Environment...

echo Installing modules...
virtualenv env
source env/bin/activate
pip install flatten_json
pip install prettytable
pip install pandas
pip install requests