from accounts.views import UserListView
from webapp.views import MessageCreateView, MessageListView, IncomeMessageListView

from django.urls import path
app_name = 'webapp'

urlpatterns = [

    path('<int:profile_pk>/message/send/', MessageCreateView.as_view(), name='message_send'),
    path('', UserListView.as_view(), name='user_list'),
]