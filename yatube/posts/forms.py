from django.forms import ModelForm
from .models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["group", "text"]
        labels = {'group': 'Группа', 'text': 'Сообщение'}
        help_texts = {'group': 'Выберите группу', 'text': 'Введите ссообщение'}
