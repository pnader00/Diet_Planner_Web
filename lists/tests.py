from django.urls import resolve
from django.test import TestCase
from django.test import Client
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item


# Create your tests here.

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        # resolve łączy adres url z odpowiednia funlcją(widokiem, view) znalezioną w pliku views
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)

        expected_html = render_to_string('home.html')

        self.assertEqual(response.content.decode(), expected_html)
        # self.assertEqual(response.templates[0].name, 'home.html')

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'New list element'

        response = home_page(request)

        self.assertIn('New list element', response.content.decode())
        expected_html = render_to_string(
            'home.html',
            {'new_item_text': 'New list element'}
        )
        self.assertEqual(response.content.decode(), expected_html)


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'Absolutnie pierwszy element listy'
        first_item.save()

        second_item = Item()
        second_item.text = 'Drugi element'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'Absolutnie pierwszy element listy')
        self.assertEqual(second_saved_item.text, 'Drugi element')


