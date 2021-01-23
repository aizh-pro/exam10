from django.conf import settings
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import RegisterView, RegisterActivateView, UserDetailView, \
    UserChangeView, UserPasswordChangeView, UserPasswordResetEmailView, UserPasswordResetView, UserListView
from webapp.views import MessageListView, IncomeMessageListView, AddFriendView, RemoveFriendView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='create'),
    path('activate/<uuid:token>/', RegisterActivateView.as_view(), name='activate'),
    path('<int:pk>/', UserDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', UserChangeView.as_view(), name='change'),
    path('password-change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('password-reset/', UserPasswordResetEmailView.as_view(), name='password_reset_email'),
    path('password-reset/<uuid:token>/', UserPasswordResetView.as_view(), name='password_reset'),
    path('<int:pk>/addfriend/', AddFriendView.as_view(), name='add_friend'),
    path('<int:pk>/removefriend/', RemoveFriendView.as_view(), name='remove_friend'),
]
