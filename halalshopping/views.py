from django.shortcuts import render, get_object_or_404, redirect
from .models import ShoppingCollection, ShoppingSchedule, ExceptionDate, MissedCollectionDate
from client.models import Client
from django.contrib.auth.decorators import login_required
from .forms import ShoppingScheduleForm, ShoppingCollectionForm, ExceptionDateForm, MissedCollectionDateForm
from .filters import ShoppingCollectionFilter
import datetime
from django.http import HttpResponse
import csv


@login_required
def shopping_collection_today(request):
    return redirect('/halalshopping/shoppingcollection?date=' + str(datetime.date.today()))


@login_required
def export_shopping_collections(request, datestring):
    pass


@login_required
def shopping_collection_list(request):
    date = datetime.datetime.strptime(request.GET.get('date'), '%Y-%m-%d').date()
    if date.weekday() == 0:
        shopping_collections_filter = ShoppingCollectionFilter(request.GET, queryset=ShoppingCollection.objects.all())
        client_ids = list(shopping_collections_filter.qs.values_list('client__pk', flat=True))
        exception_date_ids = list(ExceptionDate.objects.filter(date=date).values_list('pk', flat=True))
        schedules = ShoppingSchedule.objects.filter(status='active').filter(start_date__lte=date).filter(end_date__gte=date).exclude(client__pk__in=client_ids).exclude(exception_dates__pk__in=exception_date_ids).order_by('time')
        total_count = len(schedules) + len(shopping_collections_filter.qs)
    else:
        shopping_collections_filter = ShoppingCollectionFilter(request.GET, queryset=ShoppingCollection.objects.none())
        schedules = []
        total_count = 0
    return render(request, 'halalshopping/shoppingcollection/list.html', {'shopping_collections_filter': shopping_collections_filter, 'schedules': schedules, 'date': date, 'total_count': total_count})


@login_required
def create_shopping_collection(request):
    client_id = request.GET.get('client')
    type = request.GET.get('type')
    client = get_object_or_404(Client, pk=client_id)
    initial = {'client': client_id, 'type': type}
    if hasattr(client, 'halal_shopping_schedule'):
        schedule = client.halal_shopping_schedule
        initial['number_of_adults'] = schedule.number_of_adults
        initial['number_of_children'] = schedule.number_of_children
        initial['dietary_requirements'] = ', '.join(schedule.get_dietary_requirements())
    new_shopping_collection = None
    if request.method == 'POST':
        shopping_collection_form = ShoppingCollectionForm(request.POST)
        if shopping_collection_form.is_valid():
            new_shopping_collection = shopping_collection_form.save()
            return redirect(client.get_absolute_url() + '#halal-shopping')
    else:
        shopping_collection_form = ShoppingCollectionForm(initial=initial)
    return render(request, 'halalshopping/shoppingcollection/edit.html', {'new_shopping_collection': new_shopping_collection, 'shopping_collection_form': shopping_collection_form, 'client': client})

@login_required
def edit_shopping_collection(request, pk):
    shopping_collection = get_object_or_404(ShoppingCollection, pk=pk)
    client = shopping_collection.client
    if request.method == 'POST':
        shopping_collection_form = ShoppingCollectionForm(request.POST, instance=shopping_collection)
        if shopping_collection_form.is_valid():
            shopping_collection = shopping_collection_form.save()
            if request.GET.get('referrer') == 'client':
                return redirect(client.get_absolute_url() + '#halal-shopping')
            else:
                date = request.GET.get('date')
                return redirect('/halalshopping/shoppingcollection?date=' + str(date))
    else:
        shopping_collection_form = ShoppingCollectionForm(instance=shopping_collection)
    return render(request, 'halalshopping/shoppingcollection/edit.html', {'shopping_collection_form': shopping_collection_form, 'client': client})


@login_required
def delete_shopping_collection(request, pk):
    shopping_collection = get_object_or_404(ShoppingCollection, pk=pk)
    client = shopping_collection.client
    shopping_collection.delete()
    if request.GET.get('referrer') == 'client':
        return redirect(client.get_absolute_url() + '#halal-shopping')
    else:
        date = request.GET.get('date')
        return redirect('/halalshopping/shoppingcollection?date=' + date)


@login_required
def create_shopping_schedule(request):
    client_id = request.GET.get('client')
    client = get_object_or_404(Client, pk=client_id)
    initial = {'client': client_id}
    new_shopping_schedule = None
    if request.method == 'POST':
        shopping_schedule_form = ShoppingScheduleForm(request.POST)
        if shopping_schedule_form.is_valid():
            new_shopping_schedule = shopping_schedule_form.save()
            return redirect(client.get_absolute_url() + '#halal-shopping')
    else:
        shopping_schedule_form = ShoppingScheduleForm(initial=initial)
    return render(request, 'halalshopping/shoppingschedule/edit.html', {'new_shopping_schedule': new_shopping_schedule, 'shopping_schedule_form': shopping_schedule_form, 'client': client})


@login_required
def edit_shopping_schedule(request, pk):
    shopping_schedule = get_object_or_404(ShoppingSchedule, pk=pk)
    client = shopping_schedule.client
    if request.method == 'POST':
        shopping_schedule_form = ShoppingScheduleForm(request.POST, instance=shopping_schedule)
        if shopping_schedule_form.is_valid():
            shopping_schedule = shopping_schedule_form.save()
            return redirect(client.get_absolute_url() + '#halal-shopping')
    else:
        shopping_schedule_form = ShoppingScheduleForm(instance=shopping_schedule)
    return render(request, 'halalshopping/shoppingschedule/edit.html', {'shopping_schedule_form': shopping_schedule_form, 'client': client})


@login_required
def create_exception_date(request):
    schedule_id = request.GET.get('schedule')
    schedule = get_object_or_404(ShoppingSchedule, pk=schedule_id)
    initial = {'schedule': schedule}
    new_exception_date = None
    if request.method == 'POST':
        exception_date_form = ExceptionDateForm(request.POST)
        if exception_date_form.is_valid():
            new_exception_date = exception_date_form.save()
            for collection in schedule.client.shopping_collections.all():
                if collection.date == new_exception_date.date:
                    collection.delete()
            return redirect(schedule.client.get_absolute_url() + '#halal-shopping')
    else:
        exception_date_form = ExceptionDateForm(initial=initial)
    return render(request, 'halalshopping/exceptiondate/edit.html', {'new_exception_date': new_exception_date, 'exception_date_form': exception_date_form, 'schedule': schedule})


@login_required
def delete_exception_date(request, pk):
    exception_date = get_object_or_404(ExceptionDate, pk=pk)
    client = exception_date.schedule.client
    exception_date.delete()
    return redirect(client.get_absolute_url() + '#halal-shopping')


@login_required
def create_missed_collection_date(request):
    schedule_id = request.GET.get('schedule')
    schedule = get_object_or_404(ShoppingSchedule, pk=schedule_id)
    initial = {'schedule': schedule}
    new_missed_collection_date = None
    if request.method == 'POST':
        missed_collection_date_form = MissedCollectionDateForm(request.POST)
        if missed_collection_date_form.is_valid():
            new_missed_collection_date = missed_collection_date_form.save()
            for collection in schedule.client.shopping_collections.all():
                if collection.date == new_missed_collection_date.date:
                    collection.delete()
            return redirect(schedule.client.get_absolute_url() + '#halal-shopping')
    else:
        missed_collection_date_form = MissedCollectionDateForm(initial=initial)
    return render(request, 'halalshopping/missedcollectiondate/edit.html', {'new_missed_collection_date': new_missed_collection_date, 'missed_collection_date_form': missed_collection_date_form, 'schedule': schedule})


@login_required
def delete_missed_collection_date(request, pk):
    missed_collection_date = get_object_or_404(MissedCollectionDate, pk=pk)
    client = missed_collection_date.schedule.client
    missed_collection_date.delete()
    return redirect(client.get_absolute_url() + '#halal-shopping')


@login_required
def generate_shopping_collections(request, datestring):
    date = datetime.datetime.strptime(datestring, '%Y-%m-%d').date()
    schedules = ShoppingSchedule.objects.filter(status='active').filter(start_date__lte=date).filter(end_date__gte=date)

    for schedule in schedules:
        if schedule.client.shopping_collections.filter(date=date) or schedule.exception_dates.filter(date=date):
            continue
        collection = ShoppingCollection(
            client=schedule.client,
            date=date,
            time=schedule.time,
            number_of_adults=schedule.number_of_adults,
            number_of_children=schedule.number_of_children,
            dietary_requirements=', '.join(schedule.get_dietary_requirements()),
        )
        collection.save()

    return redirect('/halalshopping/shoppingcollection?date=' + datestring)
