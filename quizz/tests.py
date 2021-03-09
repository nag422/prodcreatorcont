from django.test import TestCase
from .models import Profile,Books
from django.contrib.auth.models import User

class TestBooksModel(TestCase):

    def setUp(self):
        self.data1 = Books.objects.create(title="The Ultimate Guide to using YouTube Live to Engage Your Audience",genre="Entertainments",author="nagendra",isbn="redflowers5235sf423gh")
    def test_books_model_entry(self):
        """
        Test Books model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data,Books))
    def test_books_model_name(self):
        """
        Test Books model data name
        """
        data = self.data1
        self.assertEqual(str(data),"The Ultimate Guide to using YouTube Live to Engage Your Audience")

class TestProfileModel(TestCase):
    def setUp(self):
        User.objects.create(username='admin')
        self.data1 = Profile.objects.create(user_ptr_id=1,content="The Ultimate Guide to using YouTube Live to Engage Your Audience")
    def test_profile_model_entry(self):
        data = self.data1
        self.assertTrue(isinstance(data,Profile))
        self.assertEqual(str(data),"The Ultimate Guide to using YouTube Live to Engage Your Audience")

        