from rest_framework import status
from rest_framework.test import APITestCase
from BookStoreAPI.models import BookItem
from django.test import TestCase, modify_settings


class BooksTests(APITestCase):

    fixtures = ["book_init.json", "category_init.json"]

    def setUp(self) -> None:
        pass

    def test_get_all_books(self):
        url = "/api/books"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_get_single_book(self):
        url = "/api/books/3"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("author"), "James Clear")

    def tearDown(self) -> None:
        pass
