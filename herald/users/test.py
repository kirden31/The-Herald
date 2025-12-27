__all__ = ()

import datetime
import http

import django.core.exceptions
import django.test
import django.urls
import django.utils

import users.models
import users.validators


class UserModelTest(django.test.TestCase):
    def setUp(self):
        self.user = users.models.User.objects.create(
            username='testuser',
            email='test@example.com',
            password='testpass123',
        )

    def test_profile_created_on_user_save(self):
        self.assertIsInstance(self.user.profile, users.models.Profile)
        self.assertEqual(self.user.profile.user, self.user)

    def test_email_normalization(self):
        user = users.models.User.objects.create(
            username='test2',
            email='Test.User+tag@Gmail.COM',
            password='pass',
        )
        self.assertEqual(user.email, 'testuser@gmail.com')

        user_yandex = users.models.User.objects.create(
            username='testya',
            email='test.user@ya.ru',
            password='pass',
        )
        self.assertEqual(user_yandex.email, 'test-user@yandex.ru')


class ValidateBirthdayDateTest(django.test.TestCase):
    def setUp(self):
        self.validator = users.validators.ValidateBirthdayDate(max_age_years=150)

    def test_valid_birthday(self):
        valid_date = django.utils.timezone.now().date() - django.utils.timezone.timedelta(
            days=365 * 30,
        )
        self.assertEqual(self.validator(valid_date), valid_date)

    def test_too_old(self):
        too_old = django.utils.timezone.now().date() - django.utils.timezone.timedelta(
            days=365 * 151,
        )
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.validator(too_old)

    def test_future_date(self):
        future = django.utils.timezone.now().date() + django.utils.timezone.timedelta(days=1)
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.validator(future)


class ProfileViewsTest(django.test.TestCase):
    def setUp(self):
        self.user = users.models.User.objects.create(
            username='viewer',
            email='viewer@example.com',
            password='testpass123',
        )
        self.client.force_login(self.user)

    def test_profile_view(self):
        response = self.client.get(django.urls.reverse('users:profile'))
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertContains(response, self.user.username)

    def test_profile_update_view(self):
        response = self.client.get(django.urls.reverse('users:profile_edit'))
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/profile_update.html')

        data = {
            'first_name': 'New',
            'last_name': 'Name',
            'email': self.user.email,
            'birthday': datetime.date.today() - datetime.timedelta(days=365*30),
            'favorite_categories': ['technology', 'science'],
        }
        response = self.client.post(django.urls.reverse('users:profile_edit'), data, follow=True)
        self.assertRedirects(response, django.urls.reverse('users:profile'))

        self.user.refresh_from_db()
        profile = self.user.profile
        self.assertEqual(self.user.first_name, 'New')
        self.assertIn('technology', profile.favorite_categories)


class SignupViewTest(django.test.TestCase):
    def test_signup_success(self):
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'verystrongpass123',
            'password2': 'verystrongpass123',
        }

        response = self.client.post(django.urls.reverse('users:signup'), data)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertTrue(users.models.User.objects.filter(username='newuser').exists())

        user = users.models.User.objects.get(username='newuser')
        self.assertTrue(user.is_active)
        self.assertTrue(user.profile)
