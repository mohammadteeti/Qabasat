

from django.urls import path,include
from . import views
urlpatterns = [
    path("download/",views.mainView,name="download")
    
]
