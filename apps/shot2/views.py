from __future__ import unicode_literals

from django.shortcuts import render, redirect
from models import User, Item
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'shot2/index.html')


def register(request):
    result = User.objects.validate_registration(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    return redirect('/success')


def login_view(request):
    result = User.objects.validate_login(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    return redirect('/home')


def logout(request):
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')


def success(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'shot2/success.html', context)


def home(request):
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'items': Item.objects.filter(added_by = request.session['user_id']),
        'others': Item.objects.exclude(added_by = request.session['user_id'])
    }
    return render(request, 'shot2/home.html', context)


def items(request):
    return render(request, 'shot2/add_item.html')


def add_item(request):
    errs = Item.objects.validate_item(request.POST)
    added_by = User.objects.get(id=request.session['user_id'])
    if errs:
        for e in errs:
            messages.error(request, e)
        return redirect('/items/')

    else:
        Item.objects.create(
        item = request.POST['item'],
        added_by = added_by,
    )
    return redirect('/home')



def show(request, id):
    context = {
    'items': Item.objects.get(id = id),
    'others': Item.objects.exclude(added_by = request.session['user_id'])
    }
    return render(request, 'shot2/show.html', context)


def delete(request, item_id):
    Item.objects.get(id=item_id).delete()
    return redirect('/home')



def remove(request, item_id):
    added_by = User.objects.get(id=request.session['user_id'])
    item = Item.objects.get(id=item_id)
    item.users.exclude(added_by)
    return redirect('/home')


#couldnt figure out how to add. This is how close i could get :(
def add_to_wishlist(request, item_id):
    added_by = User.objects.get(id=request.session['user_id'])
    item = Item.objects.get(id=item_id)
    item.users.add(added_by)
    item.save()
    return redirect('/home')
