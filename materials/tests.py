from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(
            email='test@test.com',
            password='1111'
        )

        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='test',
            description='test',
            owner=self.user
        )

    def test_create_lesson(self):
        data = {
            'title': 'test',
            'description': 'test',
            'owner': self.user.pk,
            'course': self.course.pk,
            'link': 'https://www.youtube.com/watch?v=GpD4bDDSvFo&ab'
        }

        response = self.client.post(reverse('materials:lesson_create'), data=data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Lesson.objects.all().count(), 1)

    def test_list_lesson(self):
        response = self.client.get(reverse('materials:lesson_list'))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {'count': 0, 'next': None, 'previous': None, 'results': []}
        )

    def test_update_lesson(self):
        lesson = Lesson.objects.create(
            course=self.course,
            title='test',
            link='https://www.youtube.com/watch?v=amOnhiWKkts',
            owner=self.user,
            pk=2
        )
        data = {
            'title': 'modified_test',
            'course': self.course.pk,
            'owner': self.user.pk,
            'link': 'https://www.youtube.com/watch?v=9oQds3Glyy0',

        }

        response = self.client.put(
            reverse('materials:lesson_update', kwargs={'pk': lesson.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_delete_lesson(self):
        lesson = Lesson.objects.create(
            course=self.course,
            title='test',
            link='https://www.youtube.com/watch?v=amOnhiWKkts',
            owner=self.user,
            pk=2
        )

        response = self.client.delete(
            reverse('materials:lesson_delete', kwargs={'pk': lesson.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscriptionTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(
            email='test@test.com',
            password='1111'
        )

        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='test',
            description='test',
            owner=self.user
        )

    def test_create_subs(self):
        data = {
            'user': self.user.pk,
            'course': self.course.pk
        }
        response = self.client.post(
            reverse('materials:subscription_create', kwargs={'pk': self.course.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_delete_subs(self):
        subscription = Subscription.objects.create(
            course=self.course,
            user=self.user
        )

        response = self.client.delete(
            reverse('materials:subscription_delete', kwargs={'pk': self.course.pk})
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
