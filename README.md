# Rate Professors API

A Python Django API to add modules, students and professors as well as allocating parties accordingly.

# Set-up

To run this project:

```
sh install_modules.sh

(venv) python ./manage.py runserver
```

The `.sh` file will create a virtual environment for you and install and dependencies. After the virtual environment `venv` has been successfully created you're all good to run the server.

This project also comes bundled with a client in order to interact with the API, which is actually just a simple CLI. To run this you need to run:

```
(venv) python cli_client/client.py
```

You will need to log-in with the credentials outlined in `cli_client/readme.txt` before being able to explore additional features
