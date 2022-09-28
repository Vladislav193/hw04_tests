from django.forms import ModelForm
from django import forms
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["group", "text"]
        labels = {'group': 'Группа', 'text': 'Сообщение'}
        help_texts = {'group': 'Выберите группу', 'text': 'Введите ссообщение'}

    def clean_subject(self):
        data = self.changed_data['text']
        if data == '':
            raise forms.ValidationError('заполните поле')
        return data
