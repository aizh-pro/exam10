from django.conf.global_settings import AUTH_USER_MODEL
from django.contrib.auth import get_user_model
from django.db import models

#
# class Message(models.Model):
#     message = models.TextField(default='',  verbose_name='Сообщение')
#     sender = models.ForeignKey(get_user_model(), related_name='sent_messages', verbose_name="Отправитель", on_delete=models.PROTECT)
#     recipient = models.ForeignKey(AUTH_USER_MODEL, related_name='received_messages', null=True, blank=True, verbose_name="Получатель", on_delete=models.SET_NULL)
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

# class Friends(models.Model):
#     users = models.ManyToManyField(get_user_model())
#     current_user = models.ForeignKey(get_user_model(), related_name="owner", null=True)