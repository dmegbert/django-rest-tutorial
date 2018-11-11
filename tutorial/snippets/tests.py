from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework.views import status

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer, UserSerializer
from snippets.views import SnippetViewSet


class BaseViewTest(APITestCase):
    client = APIClient()

    def create_snippet(self, code, username):
        user = self._create_user(username)
        snippet = Snippet(title='test',
                          code=code,
                          linenos=True,
                          language='python',
                          style='friendly',
                          owner=user)
        snippet.save()

    @staticmethod
    def _create_user(username):
        user = User(username=username)
        user.save()
        return user

    def setUp(self):
        self.create_snippet(code='java is not so cool', username='bob_1')
        self.create_snippet(code='python is cool', username='bob_2')
        self.create_snippet(code='Pirates love to code in R', username='bob_3')


class GetAllSnippetsTest(BaseViewTest):
    def test_get_all_snippets(self):
        factory = APIRequestFactory()
        request = factory.get('/snippets/')
        response = self.client.get('/snippets/', request=request)
        expected = Snippet.objects.all()
        serialized_expected = SnippetSerializer(expected, many=True, context={'request': request})
        
        self.assertEqual(response.data['results'], serialized_expected.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
