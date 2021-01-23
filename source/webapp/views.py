from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import CreateView, ListView

from accounts.models import Profile
from webapp.forms import MessageForm
from webapp.models import Friend, Message


# class FriendAddView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         to_user = get_object_or_404(Profile, pk=kwargs.get('pk'))
#         friend, created = Friend.objects.get_or_create(friend=to_user, user=request.user)
#         if created:
#             return HttpResponse()
#         else:
#             return HttpResponseForbidden()
#
#
# class FriendRemoveView(LoginRequiredMixin, View):
#     def post(self, request, *args, **kwargs):
#         to_user = get_object_or_404(Profile, pk=kwargs.get('pk'))
#         friend = get_object_or_404(photo.likes, user=request.user)
#         friend.delete()
#         photo.save()
#         return HttpResponse()


class FriendAddView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=kwargs.get('pk'))
        like, created = Friend.objects.get_or_create(to_user=profile, from_user=request.user)
        if created:
            return HttpResponse()
        else:
            return HttpResponseForbidden()


class FriendRemoveView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=kwargs.get('pk'))
        like = get_object_or_404(profile.friendship_received, from_user=request.user)
        like.delete()
        profile.save()
        return HttpResponse()


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
    template_name = 'message_list.html'
    model = Message
    context_object_name = 'messages'
    paginate_by = 5

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user)
