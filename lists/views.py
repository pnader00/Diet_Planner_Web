from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists.models import Item, List
# Create your views here.


def home_page(request):
    # render szuka w katralogu templates pliku 'home.html'
    # aplikacja która korzysta z szablonu musi być dodan ado pliku settings.py

    return render(request, 'home.html')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})


def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/the-only-list-in-the-world/')
