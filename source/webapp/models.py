from django.contrib.auth import get_user_model
from django.db import models
from accounts.models import Profile


class Message(models.Model):
    message = models.TextField(default='',  verbose_name='Сообщение')
    sender = models.ForeignKey(get_user_model(), related_name='sent_messages', verbose_name="Отправитель", on_delete=models.PROTECT)
    recipient = models.ForeignKey(Profile, related_name='received_messages', null=True, blank=True, verbose_name="Получатель", on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    def __str__(self):
        return f'{self.sender} sent to {self.recipient}'


class Friend(models.Model):
    from_user = models.ForeignKey(get_user_model(), related_name='friendship_sent', verbose_name='Приглашающий', on_delete=models.CASCADE)
    to_user = models.ForeignKey(get_user_model(), related_name='friendship_received', verbose_name='Принявший', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Friendship Request"
        verbose_name_plural = "Friendship Requests"
        unique_together = ("from_user", "to_user")


    def __str__(self):
        return f'{self.from_user} invited {self.to_user}'