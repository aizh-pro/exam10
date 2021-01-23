from django import forms

from webapp.models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']