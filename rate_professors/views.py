import json

from django.contrib import auth
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from rest_framework import viewsets

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from json import loads, dumps

from rate_professors.serialisers import *


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all().order_by('code')
    serializer_class = ModuleSerializer


class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all().order_by('code')
    serializer_class = ProfessorSerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = PostRatingSerializer


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        if request.body is not None:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            username = body['username']
            email = body['email']
            password = body['password']

            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return HttpResponse('The account: "' + username + '" has been successfully created', status=200)
    else:
        return HttpResponse('Invalid request', status=400)


# {'username': content_username, 'password': content_password}

@csrf_exempt
def login_request(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        username = body['username']
        password = body['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
    else:
        return HttpResponse('Invalid request')

    # Login user and checks they were successfully authenticated
    if user is not None:
        if user.is_active:
            # Log user in and check user is authenticated
            login(request, user)
            request.session['username'] = username

            if user.is_authenticated:
                # Returns status 200 when user successfully logs in
                return HttpResponse('Welcome back, {}!'.format(user.username), status=200)
            else:
                # Returns status 401 unauthorised if user is not authorised
                return HttpResponse('User not authenticated', status=401)
        else:
            # Returns status 400 account disabled if user account is not active
            return HttpResponse('The account "{}" is disabled'.format(user.username), status=400)
    else:
        # Returns status 400 bad request if request is not of type POST
        return HttpResponse('Login Failed ', status=400)


@csrf_exempt
def logout_request(request):
    if request.method == 'POST':
        logout(request)
        return HttpResponse('You have been logged out, Goodbye', status=200)
    else:
        return HttpResponse('Bad request!', status=400)


@csrf_exempt
@require_http_methods(['GET'])
def get_rating(request):
    user = auth.get_user(request)
    if user.is_authenticated:
        rating = Rating.objects.all()
        data = GetRatingSerializer(rating, many=True).data
        return JsonResponse(data, safe=False)
    else:
        return HttpResponse('Bad request!', status=400)


"""
Add parameters passed in from client in the URL
Then query database for queryset and do the .save()
Also add a @require_http_methods(['POST']) above this
"""


#  professor_id module_code year semester rating
# post_rating/<str:prof>/<str:code>/<int:year>/<int:semester>/<int:rating>/
@csrf_exempt
@require_http_methods(['POST'])
def post_rating(request, prof, code, year, semester, rating):
    user = auth.get_user(request)
    if user.is_authenticated:
        obj = {}
        p = Professor.objects.filter(code=prof)
        if len(p) == 0:
            obj["Exist"] = False
            return JsonResponse(obj, status=400)
        else:
            module = Module.objects.filter(code=code, year=year, semester=semester)
            if len(module) == 0:
                obj["Exist"] = False
                return JsonResponse(obj, status=400)
            else:
                if type(rating) == int:
                    if 0 < rating < 6:
                        rate = Rating(module=module[0], professor=p[0], rating=rating)
                        rate.save()
                        obj["rating"] = str(rate)
                        return JsonResponse(obj, status=201)

    else:
        obj = {"User not authenticated": True}
        return JsonResponse(obj, status=400)


@csrf_exempt
@require_http_methods(['GET'])
def get_prof_ratings(request):
    user = auth.get_user(request)
    if user.is_authenticated:
        rating = Rating.objects.all()
        data = GetRatingSerializer(rating, many=True).data

        obj = loads(dumps(data))
        output = {"ratings": {}}
        for i in range(len(rating)):
            if obj[i]['professor']['name'] not in output["ratings"]:
                output['ratings'][obj[i]['professor']['name']] = [obj[i]['rating'], 1]
            else:
                output['ratings'][obj[i]['professor']['name']][0] += obj[i]['rating']
                output['ratings'][obj[i]['professor']['name']][1] += 1

        for professor in output["ratings"]:
            val = output["ratings"][professor]
            avg = val[0] / val[1]
            output["ratings"][professor] = avg
        print(output)

        return JsonResponse(output, safe=False)
    else:
        return HttpResponse('Bad request!', status=400)


@csrf_exempt
@require_http_methods(['GET'])
def average_prof_rating(request, profID, code):
    data = {}

    try:
        prof = Professor.objects.filter(code=profID).values('id')
        if len(prof) == 0:
            data["Does not exist"] = True
            return JsonResponse(data, status=400)
        #
        # prof_instance = Professor.objects.get(id=prof[0]['id'])
        # module = Module.objects.filter(code=code).values('id', 'name')

        prof_instance = Professor.objects.filter(code=profID)
        modules = Module.objects.filter(code=code)

        professor = prof_instance[0]

        amount_modules = len(modules)
        total_rating = 0
        for module in modules:
            rating = Rating.objects.filter(professor=professor, module=module)

            for i in range(len(rating)):
                total_rating += rating[i].rating
        avg_rating = total_rating / amount_modules

        data["professor"] = str(professor)
        data["name"] = modules[0].name
        data["avg_rating"] = avg_rating
        return JsonResponse(data, status=200)

    except:
        data["Server error"] = True
        return JsonResponse(data, status=500)