from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import CreateView, ListView
from django_filters.views import FilterView

from accounts.models import Profile, AuthToken
from webapp.forms import MessageForm
from webapp.models import Friend, Message


from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class AddFriendView(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, pk=None):
        to_user = get_object_or_404(User, pk=pk)
        friends, create = Friend.objects.get_or_create(from_user=request.user, to_user=to_user)
        if create:
            return Response({'pk': pk})
        else:
            return Response(status=403)


class RemoveFriendView(APIView):
    permission_classes = [IsAuthenticated]


    @method_decorator(ensure_csrf_cookie)
    def delete(self, request, pk=None):
        to_user = get_object_or_404(User, pk=pk)
        friends = Friend.objects.filter(to_user=to_user)
        friends.delete()
        return Response({'pk': pk})


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'create_message.html'

    def form_valid(self, form):
        recipient = get_object_or_404(Profile, pk=self.kwargs.get('profile_pk'))
        message = form.save(commit=False)
        message.recipient = recipient
        message.sender = self.request.user
        message.save()
        return redirect(
            'accounts:detail',
            pk=recipient.pk)

class MessageListView(ListView):
    template_name = 'outcome_message.html'
    model = Message
    context_object_name = 'messages'
    paginate_by = 5

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user)


class IncomeMessageListView(FilterView):
    template_name = 'income_messages.html'
    model = Message
    context_object_name = 'messages'
    paginate_by = 5

    def get_queryset(self):
        return Message.objects.filter(recipient=self.request.user.pk)
