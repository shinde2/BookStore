from rest_framework import status
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework.authtoken.models import Token
from BookStoreAPI import views
from BookStoreAPI.permissions import IsManager
from BookStoreAPI.models import Cart, BookItem
from django.contrib.auth.models import User, Group, Permission
from django.test import override_settings, modify_settings
from django.shortcuts import get_object_or_404


class BooksTests(APITestCase):

    fixtures = ["book_init.json", "category_init.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        # will be run once for test class
        pass 

    def setUp(self) -> None:
        # will be run before every test
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

    def test_post_user(self):
        url = "/api/books"
        data = {
          "title": "x",
          "author": "y",
          "price": 15.00,
          "book_category": 2,
        }
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Post unit test should only test post request.
    # Auth and group permissions should be tested separately.
    # So use superuser to bypass permissions and force auth.
    def test_post_superuser(self):
        url = "/api/books"
        data = {
          "title": "x",
          "author": "y",
          "price": 15.00,
          "book_type": "Horror",
        }
        user = User.objects.create_superuser(username="manager")
        self.client.force_authenticate(user)
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # This post test is more of a integration test as it tests,
    # user login and group permissions.
    def test_post_manager(self):
        url = "/api/books"
        data = {
          "title": "x",
          "author": "y",
          "price": 15.00,
          "book_type": "Horror",
        }

        group, __ = Group.objects.get_or_create(name="Manager")
        all_perms = Permission.objects.all()
        group.permissions.set(all_perms)
        
        user = User.objects.create(username="manager", password="password")
        user.groups.add(group)

        rf = APIRequestFactory()
        request = rf.post(url, data, format="json")
        request.user = user

        view = views.BookItemsList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def tearDown(self) -> None:
        pass

class LoginTests(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        # will be run once for test class
        pass 

    def setUp(self) -> None:
        # will be run before every test
        pass 

    def test_register_get(self):
        url = "/register"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
    def test_register_post(self):
        url = "/register"
        data = {
          "username": "username",
          "password": "fksjfsfjksdj",
        }
        response = self.client.post(url, data=data, format="json")
        #print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_get(self):
        url = "/login"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # User is not registered
    def test_login_post_invalid(self):
        url = "/login"
        data = {
          "username": "username",
          "password": "fksjfsfjksdj",
        }
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_post_valid(self):
        url = "/login"
        data = {
          "username": "username",
          "password": "fksjfsfjksdj",
        }
        user = User.objects.create(**data)
        user.set_password("fksjfsfjksdj")
        user.save()
        token, __ = Token.objects.get_or_create(user=user)

        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("token"), token.key)

    def test_logout(self):
        url = "/logout"
        data = {
          "username": "username",
          "password": "fksjfsfjksdj",
        }
        user = User.objects.create(**data)
        user.set_password("fksjfsfjksdj")
        user.save()
        token, __ = Token.objects.get_or_create(user=user)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.post(url, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertRaises(Token.DoesNotExist)

class OrderTests(APITestCase):

    fixtures = ["book_init.json", "category_init.json"]

    @classmethod
    def setUpTestData(cls) -> None:
        # will be run once for test class
        pass 

    def setUp(self) -> None:
        # will be run before every test
        pass 

    def test_order(self):
        data = [{
          "book": "Dune",
          "quantity": 3,
        },
        {
          "book": "Contact",
          "quantity": 10,
        }]

        user = User.objects.create(username="username")
        user.set_password("fksjfsfjksdj")
        user.save()

        for cartItem in data:
            bookitem = get_object_or_404(BookItem, title=cartItem["book"])
            cart = Cart.objects.create(
                user=user,
                bookitem=bookitem,
                quantity=cartItem["quantity"],
                price=bookitem.price,
                total=bookitem.price * cartItem["quantity"]
            )

        self.client.force_authenticate(user)
        response = self.client.post("/api/orders", format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get("/api/orders", format="json")
        self.assertEqual(response.data[0]["total"], "165.00")
