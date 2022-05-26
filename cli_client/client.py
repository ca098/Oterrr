import json
import requests

from decimal import *

from prettytable import PrettyTable

BASE_URL = 'http://127.0.0.1:8000/'

session = requests.Session()


def listModules():
    url = BASE_URL + 'modules/'
    response = session.get(url)

    jsonData = json.loads(response.text)

    try:
        table = PrettyTable(['Code', 'Name', 'Year', 'Semester', 'Taught by'])

        for data in jsonData:

            code = data['code']
            name = data['name']
            year = str(data['year'])
            semester = str(data['semester'])
            profName = []

            for professor in data['professor']:
                profName.append(professor['name'])

            table.add_row([code, name, year, semester, ','.join(profName)])

        print(table)
    except:
        print(jsonData['detail'])


def listProfessorRatings():
    url = BASE_URL + 'get_prof_ratings/'
    try:
        response = session.get(url)
        jsonData = json.loads(response.text)

        for name in jsonData['ratings']:
            star = ""
            avg = Decimal(jsonData['ratings'][name]).quantize(0, ROUND_HALF_UP)
            for i in range(int(avg)):
                star += "*"

            output = "The rating of Professor {} is: {}".format(name, star)
            print(output)

    except:
        print("Authentication is required")


def prof_module_rating(input):
    tokens = input.split()

    professor_id = tokens[1]
    module_code = tokens[2]

    url = BASE_URL + 'avg_module/{}/{}/'.format(professor_id, module_code)
    response = session.get(url)

    jsonData = json.loads(response.text)

    try:

        avg = Decimal(jsonData['avg_rating']).quantize(0, ROUND_HALF_UP)
        star = ""
        for i in range(int(avg)):
            star += "*"

        output = "The rating of Professor {} ({}) in module {} ({}) is: {}".format(jsonData['professor'], professor_id,
                                                                                   jsonData['name'], module_code,
                                                                                   star)

        print(output)

    except:
        print("Exception occured: " + jsonData)


def rate(input):
    tokens = input.split()

    professor_id = tokens[1]
    module_code = tokens[2]
    year = tokens[3]
    semester = tokens[4]
    rating = tokens[5]

    url = BASE_URL + 'post_rating/{}/{}/{}/{}/{}/'.format(professor_id, module_code,
                                                          year, semester, rating)

    try:
        response = session.post(url)
        jsonData = json.loads(response.text)
        print("The rating for: {}\nwas submitted successfully".format(jsonData['rating']))

    except:
        print("An Exception occurred, ensure that you have logged in...")


def login():
    username = input("\nPlease input your username : ")
    password = input("Please input your password : ")

    url = BASE_URL + 'login/'

    payload = {'username': username,
               'password': password}

    response = session.post(url, data=json.dumps(payload))

    print(response.text)


def register():
    username = input("\nPlease provide a username : ")
    email = input("Please provide an email : ")
    password = input("Please provide a password : ")

    url = BASE_URL + 'register/'

    payload = {'username': username,
               'email': email,
               'password': password}

    response = requests.post(url, data=json.dumps(payload))

    print(response.text)


def logout():
    url = BASE_URL + 'logout/'

    response = session.post(url)

    print(response.text)


def usr_input(input):
    if input.lower() == "register":
        register()
        # Done

    elif input.lower() == "login":
        login()
        # Done

    elif input.lower() == "logout":
        logout()
        # Done

    elif input.lower() == "list":
        listModules()
        # Done

    elif input.lower() == "view":
        listProfessorRatings()
        # Done

    elif input.lower().startswith('average'):
        prof_module_rating(input)
        # Done

    elif input.lower().startswith('rate'):
        rate(input)
        # Done


while True:
    cmd = input("\nEnter your command : ")
    usr_input(cmd)
