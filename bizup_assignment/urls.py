
from django.contrib import admin
from django.urls import path
from api_endpoints.views import (apiView)

urlpatterns = [
    
    path('',apiView ),
]
