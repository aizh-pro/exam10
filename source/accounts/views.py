from django.contrib.auth import get_user_model, authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View, FormView, DetailView, CreateView, UpdateView, ListView
from django.conf import settings

from accounts.forms import MyUserCreationForm, UserChangeForm, ProfileChangeForm, \
    PasswordChangeForm, PasswordResetEmailForm, PasswordResetForm
from .models import AuthToken, Profile


class RegisterView(CreateView):
    model = User
    template_name = 'user_create.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        if settings.ACTIVATE_USERS_EMAIL:
            return redirect('accounts:user_list')
        else:
            login(self.request, user)
            return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('accounts:user_list')
        return next_url


class RegisterActivateView(View):
    def get(self, request, *args, **kwargs):
        token = AuthToken.get_token(self.kwargs.get('token'))
        if token:
            if token.is_alive():
                self.activate_user(token)
            token.delete()
        return redirect('')

    def activate_user(self, token):
        user = token.user
        user.is_active = True
        user.save()
        Profile.objects.create(user=user)
        login(self.request, user)


class UserListView(ListView):
    template_name = 'user_list.html'
    queryset = get_user_model().objects.all()
    context_object_name = 'users_list'
    paginate_by = 10
    paginate_orphans = 4
    ordering = ['-id']

class UserDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'
    paginate_messages_orphans = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages, page, is_paginated = self.paginate_messages(self.object)
        context['messages'] = messages
        context['page_obj'] = page
        context['is_paginated'] = is_paginated
        return context

    def paginate_messages(self, guest):
        messages = recipient.messages.all().order_by('-created_at')
        if messages.count() > 0:
            paginator = Paginator(messages, orphans=self.paginate_messages_orphans)
            page_number = self.request.GET.get('page', 1)
            page = paginator.get_page(page_number)
            is_paginated = paginator.num_pages > 1  # page.has_other_pages()
            return page.object_list, page, is_paginated
        else:
            return messages, None, False


class UserChangeView(UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'user_change.html'
    context_object_name = 'user_obj'

    def test_func(self):
        return self.request.user == self.get_object()

    def get_context_data(self, **kwargs):
        if 'profile_form' not in kwargs:
            kwargs['profile_form'] = self.get_profile_form()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        profile_form = self.get_profile_form()
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def form_valid(self, form, profile_form):
        form.save()
        profile_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, profile_form):
        context = self.get_context_data(form=form, profile_form=profile_form)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse('accounts:detail', kwargs={'pk': self.object.pk})

    def get_profile_form(self):
        form_kwargs = {'instance': self.object.profile}
        if self.request.method == 'POST':
            form_kwargs['data'] = self.request.POST
            form_kwargs['files'] = self.request.FILES
        return ProfileChangeForm(**form_kwargs)



class UserPasswordChangeView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'user_password_change.html'
    form_class = PasswordChangeForm
    context_object_name = 'user_obj'

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('accounts:detail', kwargs={'pk': self.object.pk})



class UserPasswordResetEmailView(FormView):
    form_class = PasswordResetEmailForm
    template_name = 'password_reset_email.html'
    success_url = reverse_lazy('accounts:user_list')

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class UserPasswordResetView(UpdateView):
    model = User
    form_class = PasswordResetForm
    template_name = 'password_reset.html'
    success_url = reverse_lazy('accounts:login')

    def get_object(self, queryset=None):
        token = self.get_token()
        if token and token.is_alive():
            return token.user
        raise Http404('Ссылка не существует или её срок действия истёк')

    def form_valid(self, form):
        token = self.get_token()
        token.delete()
        return super().form_valid(form)

    def get_token(self):
        return AuthToken.get_token(self.kwargs.get('token'))
