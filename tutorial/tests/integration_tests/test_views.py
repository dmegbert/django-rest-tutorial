import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient, APIRequestFactory, force_authenticate
from rest_framework.views import status

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from snippets.views import SnippetViewSet


class BaseViewTest(APITestCase):
    @staticmethod
    def create_snippet(code, owner):
        snippet = Snippet(title='test',
                          code=code,
                          linenos=True,
                          language='python',
                          style='friendly',
                          owner=owner)
        snippet.save()

    def setUp(self):
        self.user = User.objects.create_superuser(username='joe', password='tester', email='joe@testy.com')
        self.create_snippet(code='java is not so cool', owner=self.user)
        self.create_snippet(code='python is cool', owner=self.user)
        self.create_snippet(code='Pirates love to code in R', owner=self.user)


class SnippetsTest(BaseViewTest):
    def test_get_all_snippets(self):
        factory = APIRequestFactory()
        request = factory.get('/snippets/')
        response = self.client.get('/snippets/', request=request)
        expected = Snippet.objects.all()
        serialized_expected = SnippetSerializer(expected, many=True, context={'request': request})

        self.assertEqual(response.data['results'], serialized_expected.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_new_snippet(self):
        # client = APIClient()
        # client.login(username=self.user.username, password='tester')
        data = {
            "title": "test_post",
            "code": "Hello Post",
            "linenos": False,
            "language": 'python',
            "style": 'friendly'
        }

        factory = APIRequestFactory()
        user = User.objects.get(username='joe')
        view = SnippetViewSet.as_view({'post': 'create'})

        # Make an authenticated request to the view
        request = factory.post('/snippets/', data=data, format='json')
        force_authenticate(request, user=user)
        response = view(request)

        self.assertContains(response, text='Hello Post', count=1, status_code=201)

    def test_put_update_snippet(self):
        snippet_to_update = Snippet.objects.get(code='python is cool')
        data = {
            "id": str(snippet_to_update.id),
            "title": "test_put",
            "code": "Hello Put",
            "linenos": False,
            "language": 'python',
            "style": 'friendly'
        }
        factory = APIRequestFactory()
        user = User.objects.get(username='joe')
        view = SnippetViewSet.as_view({'put': 'update'})

        # Make an authenticated request to the view
        request = factory.put('/snippets/', data=data, format='json')
        force_authenticate(request, user=user)
        response = view(request, pk=snippet_to_update.id)

        self.assertContains(response, text='Hello Put', count=1, status_code=200)

