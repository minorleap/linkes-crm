from django.shortcuts import render, get_object_or_404, redirect
from .models import FoodhubCollection
from client.models import Client
from django.contrib.auth.decorators import login_required
from .forms import FoodhubCollectionForm
from .filters import FoodhubCollectionFilter
import datetime
from django.http import HttpResponse
import csv


@login_required
def foodhub_collection_today(request):
    return redirect('/foodhub/collection?date=' + str(datetime.date.today()))


@login_required
def foodhub_collection_list(request):
    foodhub_collection_filter = FoodhubCollectionFilter(request.GET, queryset=FoodhubCollection.objects.all())
    date = datetime.datetime.strptime(request.GET.get('date'), '%Y-%m-%d').date()
    return render(request, 'foodhub/collection/list.html', {'foodhub_collection_filter': foodhub_collection_filter, 'date': date})


@login_required
def create_foodhub_collection(request):
    client_id = request.GET.get('client')
    type = request.GET.get('type')
    client = get_object_or_404(Client, pk=client_id)
    initial = {'client': client_id, 'date': datetime.date.today()}
    new_foodhub_collection = None
    if request.method == 'POST':
        foodhub_collection_form = FoodhubCollectionForm(request.POST)
        if foodhub_collection_form.is_valid():
            new_foodhub_collection = foodhub_collection_form.save()
            return redirect(client.get_absolute_url() + '#foodhub')
    else:
        foodhub_collection_form = FoodhubCollectionForm(initial=initial)
    return render(request, 'foodhub/collection/edit.html', {'new_foodhub_collection': new_foodhub_collection, 'foodhub_collection_form': foodhub_collection_form, 'client': client})

@login_required
def edit_foodhub_collection(request, pk):
    foodhub_collection = get_object_or_404(FoodhubCollection, pk=pk)
    client = foodhub_collection.client
    if request.method == 'POST':
        foodhub_collection_form = FoodhubCollectionForm(request.POST, instance=foodhub_collection)
        if foodhub_collection_form.is_valid():
            foodhub_collection = foodhub_collection_form.save()
            if request.GET.get('referrer') == 'client':
                return redirect(client.get_absolute_url() + '#foodhub')
            else:
                date = request.GET.get('date')
                return redirect('/foodhub/collection?date=' + str(date))
    else:
        foodhub_collection_form = FoodhubCollectionForm(instance=foodhub_collection)
    return render(request, 'foodhub/collection/edit.html', {'foodhub_collection_form': foodhub_collection_form, 'client': client})


@login_required
def delete_foodhub_collection(request, pk):
    foodhub_collection = get_object_or_404(FoodhubCollection, pk=pk)
    client = foodhub_collection.client
    foodhub_collection.delete()
    if request.GET.get('referrer') == 'client':
        return redirect(client.get_absolute_url() + '#foodhub')
    else:
        date = request.GET.get('date')
        return redirect('/foodhub/collection?date=' + date)
