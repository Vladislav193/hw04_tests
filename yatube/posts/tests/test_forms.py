from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Group, Post

User = get_user_model()


class PostCreateFormTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            text='Тестовый текст',
            slug='тест'
        )
        cls.author = User.objects.create(username = 'Test_name')
        cls.post = Post.objects.create(
            text='Тестовый текст2',
            author=cls.author
        )

    def setUp(self) -> None:
        self.authorized_client = Client()
        self.authorized_client.force_login(self.author)

    def new_post_create_form(self):
        """При отправке валидной формы создаётся новая запись в БД"""
        posts_count = Post.objects.count()
        form_date = {
            'text': 'текст из формы',
            'group': self.group.pk
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_date,
            follow=True
        )
        self.assertEqual(posts_count, posts_count + 1)
        self.assertRedirects(response, reverse('posts:profile', 
                             kwargs={'username': 'Test_name'}))

    def create_post_form(self):
        """При отправке валидной формы происходит изменение поста в БД"""
        posts_count = Post.objects.count()
        form_date = {
            'text': 'Измененый текст'
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', args=('post_id',)),
            data=form_date,
            follow=True
        )
        self.assertRedirects(response, reverse('posts:detail', 
                                               kwargs={'post_id': f'{self.post.pk}'}))
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertEqual(Post.objects.get('id').text, form_date['text'])
