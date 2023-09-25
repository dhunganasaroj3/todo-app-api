"""
Tests for todo APIs.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Todo

from todo.serializers import TodoSerializer

TODOS_URL = reverse('todo:todo-list')


def create_todo(user, **params):
    """Create and return a sample todo."""
    defaults = {
        'title': 'Sample todo title',
        'description': 'Sample todo description',
    }
    defaults.update(params)

    todo = Todo.objects.create(user=user, **defaults)
    return todo


class PublicTodoAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(TODOS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTodoApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrive_todos(self):
        """Test retrieving a list of todos."""
        create_todo(user=self.user)
        create_todo(user=self.user)

        res = self.client.get(TODOS_URL)

        todos = Todo.objects.all().order_by('-id')
        serializer = TodoSerializer(todos, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


