from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
# Create your views here.


def home_page(request):
    # render szuka w katralogu templates pliku 'home.html'
    # aplikacja która korzysta z szablonu musi być dodan ado pliku settings.py
    return render(request, 'home.html', {
        'new_item_text': request.POST.get('item_text', '')
    })


if __name__ == '__main__':
    request = HttpRequest()
    # response = home_page(request)
    print("ff")