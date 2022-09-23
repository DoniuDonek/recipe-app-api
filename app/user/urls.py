"""URL mapping for user API"""
from django.urls import path
from user import views

app_name = 'user' #w test user api.py mamy CREATE_USER_URL z metodą reverse, która wskazuje na tę apkę

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name = 'create'),
]
