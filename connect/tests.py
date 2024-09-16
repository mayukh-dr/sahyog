#connect/tests.py

from django.test import Client, TestCase
from django.urls import reverse 
from django.contrib.auth import get_user_model
from datetime import date 
from .models import Post 

# Create your tests here.

class PostModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret',
            about_me = 'Just a humble test',
        )

        self.post = Post.objects.create(
            flight_number='ABC123',
            traveler='testuser',
            travel_date = date.today(),
            message = 'I am Thanos!'
        )

    def test_string_representation(self):
        post=Post(flight_number='ABC123')
        self.assertEqual(str(post), post.flight_number)

    def test_post_content(self):
        self.assertEqual(f'{self.post.flight_number}','ABC123')
        self.assertEqual(f'{self.post.traveler}','testuser')
        self.assertEqual(self.post.travel_date,date.today())


    def test_flight_number(self):
        post = Post.objects.get(id=1)
        expected_object_name = f'{post.flight_number}'
        self.assertEqual(expected_object_name, 'ABC123')


    def test_post_listview(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,'ABC123')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detailview(self):
        response = self.client.get('/post/1/')
        no_response = self.client.get('/post/10000/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'ABC123')
        self.assertTemplateUsed(response, 'post_detail.html')


    def test_post_create_view(self):
        response = self.client.post(reverse('post_new'),{
            'flight_number' : '6E234',
            'travel_date'   : date.today(),
            'message'      : 'I would like to learn from your insights.',
            'traveler'      : 'testuser'
        })
        print(response)
        #self.assertEqual(response.status_code, 302)
        #self.assertContains(response, '6E234')
        #self.assertContains(response, 'I would like to learn from your insights.')


    #def test_post_update_view(self):
     #   response = self.client.post(reverse('post_edit', args='1'),{
      #      'flight_number' : '6E345'
       # })
        #self.assertEqual(response.status_code, 200)

    def test_post_delete_view(self):
        response = self.client.get(
            reverse('post_delete', args='1'))
        self.assertEqual(response.status_code, 200)

class SignupPageTests(TestCase):
    username = 'newuser'
    email = 'newuser@email.com'
    about_me = 'just a humble unit test'

    def test_signup_page_status_code(self):
        response = self.client.get('/users/signup')
        self.assertEqual(response.status_code, 301)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

    def test_signup_form(self):
        new_user = get_user_model().objects.create_user(
            self.username, self.email
        )
        self.assertEqual(get_user_model().objects.all().count(),1)
        self.assertEqual(get_user_model().objects.all()[0].username,
                         self.username)
        self.assertEqual(get_user_model().objects.all()[0].email, self.email)
        #self.assertEqual(get_user_model().objects.all()[0].about_me,
        #                 self.about_me)
