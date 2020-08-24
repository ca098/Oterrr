from django.urls import include, path
from rest_framework import routers
from . import views
from .views import *

router = routers.DefaultRouter()
router.register(r'modules', views.ModuleViewSet)
router.register(r'professors', views.ProfessorViewSet)
router.register(r'ratings', views.RatingViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('register/', create_user),
    path('login/', login_request),
    path('logout/', logout_request),
    path('post_rating/<str:prof>/<str:code>/<int:year>/<int:semester>/<int:rating>/', post_rating),
    path('get_rating/', get_rating),
    path('get_prof_ratings/', get_prof_ratings),
    path('avg_module/<str:profID>/<str:code>/', average_prof_rating),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
