from rest_framework import status
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework.authtoken.models import Token
from BookStoreAPI import views
from BookStoreAPI.permissions import IsManager
from django.contrib.auth.models import User, Group, Permission


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

    '''
    # Login authentication should be tested in a separate login view unit test
    def test_post_manager(self):
        url = "/api/books"
        data = {
          "title": "x",
          "author": "y",
          "price": 15.00,
          "book_type": 2,
        }

        #user, __ = User.objects.get_or_create(username="manager")
        #user.set_password("password")
        #user.save()
        #token, __ = Token.objects.get_or_create(user=user)
        group, __ = Group.objects.get_or_create(name="Manager")
        print("---------------------------------------------")
        all_perms = Permission.objects.all()
        group.permissions.set(all_perms)
        #print(group.permissions.all())
        
        user = User.objects.create(username="manager")
        user.set_password("password")
        user.save()
        user.groups.add(group)
        user.is_superuser = True
        user.save(update_fields=["is_superuser"])
        #print(user.groups.all())
        #print(user.get_group_permissions())
        token, __ = Token.objects.get_or_create(user=user)
        #self.client.force_authenticate(user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        response = self.client.post(url, data=data, format="json")
        #print(response)
        #self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    '''

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
