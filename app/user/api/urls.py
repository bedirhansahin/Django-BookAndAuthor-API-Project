from django.urls import path

from user.api import views

app_name = 'api_user'

urlpatterns = [
    path('list/', views.UserListView.as_view(), name='list'),
    path('create/', views.UserCreateView.as_view(), name='create'),
    path('me/', views.UserManageView.as_view(), name='me')
]
