from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms


from posts.models import Group, Post

TEST_POST: int = 13
User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='Test')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',)
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/post_create.html': reverse('posts:post_create'),
            'posts/post_detail.html': (
                reverse('posts:post_detail', 
                        kwargs={'post_id': f'{self.post.pk}'})),
            'posts/profile.html': reverse('posts:profile', 
                                          kwargs={'username':'Test'}),
            'posts/group_list.html': (
                reverse('posts:group_list', kwargs={'slug': 'test-slug'})
            ),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_home_page_show_correct_context(self):
        """Шаблон post_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        post_author_0 = first_object.author
        post_group_0 = first_object.group
        self.assertEqual(post_author_0, self.user)
        self.assertEqual(post_group_0, self.group)

    def test_group_list_page_correct_context(self):
        '''Проверяем, что в список постов передается правильный контекст '''
        response = self.authorized_client.get(reverse('posts:group_list',
                                         kwargs={'slug': 'test-slug'}))
        self.assertEqual(response.context['group'], self.group)

    def test_post_detail_pages_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = (self.authorized_client.
            get(reverse('posts:post_detail', kwargs={'post_id': '1'})))
        self.assertEqual(response.context.get('post').text, 'Тестовый пост')

    def test_post_create_context(self):
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'group': forms.fields.ChoiceField,
            'text': forms.fields.CharField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_context(self):
        response = self.authorized_client.get(reverse('posts:post_edit', kwargs={'post_id':self.post.id}))
        form_fields = {
            'group': forms.fields.ChoiceField,
            'text': forms.fields.CharField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)  

class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='Test')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
            )

        posts = []
        for _ in range(TEST_POST):
            post = Post(
                author=cls.user,
                text='Тестовый пост',
                group=cls.group
            )
            posts.append(post)
        Post.objects.bulk_create(posts)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_first_page_contains_ten_records(self):
        '''Проверка: количество постов на первой странице равно 10.'''
        urls = {
            reverse('posts:index'): 'index.html',
            reverse('posts:group_list', kwargs={'slug': 'test-slug'}): 'posts/group_list.html',
            reverse('posts:profile', kwargs={'username':'Test'}): 'profile.html',
        }
        for tested_url in urls.keys():
            response = self.client.get(tested_url)
            self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_three_records(self):
        '''Проверка: на второй странице должно быть три поста.'''
        urls = {
            reverse('posts:index') + '?page=2': 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': 'test-slug'}) + '?page=2':
            'posts/group_list.html',
            reverse('posts:profile', kwargs={'username':'Test'})+ '?page=2':
            'profile.html',
        }
        for tested_url in urls.keys():
            response = self.client.get(tested_url)
            self.assertEqual(len(response.context['page_obj']), 3)
