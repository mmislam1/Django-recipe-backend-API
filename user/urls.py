from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('update/', views.UpdateUserView.as_view(), name='update'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('view/', views.ListUsersView.as_view(), name='view'),
    path('<int:pk>/delete/', views.DeleteUserView.as_view(), name='delete')
]
