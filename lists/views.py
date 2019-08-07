from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Item


def home_page(request):
    return render(request, 'home.html')


def new_list(request):
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/new-list/')


def view_list(request):
    return render(request, 'list.html', {'items': Item.objects.all()})
