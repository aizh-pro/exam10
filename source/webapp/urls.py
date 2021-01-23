from webapp.views import FriendAddView, FriendRemoveView, MessageCreateView, MessageListView

from django.urls import path
app_name = 'webapp'

urlpatterns = [
    path('like/', FriendAddView.as_view(), name='add_friend'),
    path('unlike/', FriendRemoveView.as_view(), name='remove_friend'),
    path('<int:profile_pk>/message/send/', MessageCreateView.as_view(), name='message_send'),
    path('outcome/messages', MessageListView.as_view(), name='outcome_list'),
]