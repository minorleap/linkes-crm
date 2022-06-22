from django.shortcuts import render, get_object_or_404, redirect
from .models import ShoppingDelivery, ShoppingSchedule, ExceptionDate, MissedDeliveryDate
from client.models import Client
from django.contrib.auth.decorators import login_required
from .forms import ShoppingScheduleForm, ShoppingDeliveryForm, ExceptionDateForm, MissedDeliveryDateForm
from .filters import ShoppingDeliveryFilter
import datetime
from django.http import HttpResponse
import csv


@login_required
def shopping_delivery_today(request):
    return redirect('/foodshopping/shoppingdelivery?date=' + str(datetime.date.today()))


@login_required
def export_shopping_deliveries(request, datestring):
    pass


@login_required
def shopping_delivery_list(request):
    date = datetime.datetime.strptime(request.GET.get('date'), '%Y-%m-%d').date()
    if date.weekday() == 3:
        shopping_deliveries_filter = ShoppingDeliveryFilter(request.GET, queryset=ShoppingDelivery.objects.all())
        client_ids = list(shopping_deliveries_filter.qs.values_list('client__pk', flat=True))
        exception_date_ids = list(ExceptionDate.objects.filter(date=date).values_list('pk', flat=True))
        schedules = ShoppingSchedule.objects.filter(status='active').filter(start_date__lte=date).filter(end_date__gte=date).exclude(client__pk__in=client_ids).exclude(exception_dates__pk__in=exception_date_ids)
        schedule_ids = [schedule.pk for schedule in schedules if not schedule.includes_date(date)]
        schedules = schedules.exclude(pk__in=schedule_ids)
        total_count = len(schedules) + len(shopping_deliveries_filter.qs)
    else:
        shopping_deliveries_filter = ShoppingDeliveryFilter(request.GET, queryset=ShoppingDelivery.objects.none())
        schedules = []
        total_count = 0
    return render(request, 'foodshopping/shoppingdelivery/list.html', {'shopping_deliveries_filter': shopping_deliveries_filter, 'schedules': schedules, 'date': date, 'total_count': total_count})


@login_required
def create_shopping_delivery(request):
    client_id = request.GET.get('client')
    type = request.GET.get('type')
    client = get_object_or_404(Client, pk=client_id)
    initial = {'client': client_id, 'type': type}
    if hasattr(client, 'foood_shopping_schedule'):
        schedule = client.food_shopping_schedule
        initial['number_of_adults'] = schedule.number_of_adults
        initial['number_of_children'] = schedule.number_of_children
        initial['dietary_requirements'] = ', '.join(schedule.get_dietary_requirements())
        initial['delivery_notes'] = schedule.delivery_notes
    new_shopping_delivery = None
    if request.method == 'POST':
        shopping_delivery_form = ShoppingDeliveryForm(request.POST)
        if shopping_delivery_form.is_valid():
            new_shopping_delivery = shopping_delivery_form.save()
            return redirect(client.get_absolute_url() + '#shopping-deliveries')
    else:
        shopping_delivery_form = ShoppingDeliveryForm(initial=initial)
    return render(request, 'foodshopping/shoppingdelivery/edit.html', {'new_shopping_delivery': new_shopping_delivery, 'shopping_delivery_form': shopping_delivery_form, 'client': client})

@login_required
def edit_shopping_delivery(request, pk):
    shopping_delivery = get_object_or_404(ShoppingDelivery, pk=pk)
    client = shopping_delivery.client
    if request.method == 'POST':
        shopping_delivery_form = ShoppingDeliveryForm(request.POST, instance=shopping_delivery)
        if shopping_delivery_form.is_valid():
            shopping_delivery = shopping_delivery_form.save()
            if request.GET.get('referrer') == 'client':
                return redirect(client.get_absolute_url() + '#shopping-deliveries')
            else:
                date = request.GET.get('date')
                return redirect('/foodshopping/shoppingdelivery?date=' + str(date))
    else:
        shopping_delivery_form = ShoppingDeliveryForm(instance=shopping_delivery)
    return render(request, 'foodshopping/shoppingdelivery/edit.html', {'shopping_delivery_form': shopping_delivery_form, 'client': client})


@login_required
def delete_shopping_delivery(request, pk):
    shopping_delivery = get_object_or_404(ShoppingDelivery, pk=pk)
    client = shopping_delivery.client
    shopping_delivery.delete()
    if request.GET.get('referrer') == 'client':
        return redirect(client.get_absolute_url() + '#shopping-deliveries')
    else:
        date = request.GET.get('date')
        return redirect('/foodshopping/shoppingdelivery?date=' + date)


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
            return redirect(client.get_absolute_url() + '#shopping-deliveries')
    else:
        shopping_schedule_form = ShoppingScheduleForm(initial=initial)
    return render(request, 'foodshopping/shoppingschedule/edit.html', {'new_shopping_schedule': new_shopping_schedule, 'shopping_schedule_form': shopping_schedule_form, 'client': client})


@login_required
def edit_shopping_schedule(request, pk):
    shopping_schedule = get_object_or_404(ShoppingSchedule, pk=pk)
    client = shopping_schedule.client
    if request.method == 'POST':
        shopping_schedule_form = ShoppingScheduleForm(request.POST, instance=shopping_schedule)
        if shopping_schedule_form.is_valid():
            shopping_schedule = shopping_schedule_form.save()
            return redirect(client.get_absolute_url() + '#shopping-deliveries')
    else:
        shopping_schedule_form = ShoppingScheduleForm(instance=shopping_schedule)
    return render(request, 'foodshopping/shoppingschedule/edit.html', {'shopping_schedule_form': shopping_schedule_form, 'client': client})


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
            for delivery in schedule.client.shopping_deliveries.all():
                if delivery.date == new_exception_date.date:
                    delivery.delete()
            return redirect(schedule.client.get_absolute_url() + '#shopping-deliveries')
    else:
        exception_date_form = ExceptionDateForm(initial=initial)
    return render(request, 'foodshopping/exceptiondate/edit.html', {'new_exception_date': new_exception_date, 'exception_date_form': exception_date_form, 'schedule': schedule})


@login_required
def delete_exception_date(request, pk):
    exception_date = get_object_or_404(ExceptionDate, pk=pk)
    client = exception_date.schedule.client
    exception_date.delete()
    return redirect(client.get_absolute_url() + '#shopping-deliveries')


@login_required
def create_missed_delivery_date(request):
    schedule_id = request.GET.get('schedule')
    schedule = get_object_or_404(ShoppingSchedule, pk=schedule_id)
    initial = {'schedule': schedule}
    new_missed_delivery_date = None
    if request.method == 'POST':
        missed_delivery_date_form = MissedDeliveryDateForm(request.POST)
        if missed_delivery_date_form.is_valid():
            new_missed_delivery_date = missed_delivery_date_form.save()
            for delivery in schedule.client.shopping_deliveries.all():
                if delivery.date == new_missed_delivery_date.date:
                    delivery.delete()
            return redirect(schedule.client.get_absolute_url() + '#shopping-deliveries')
    else:
        missed_delivery_date_form = MissedDeliveryDateForm(initial=initial)
    return render(request, 'foodshopping/misseddeliverydate/edit.html', {'new_missed_delivery_date': new_missed_delivery_date, 'missed_delivery_date_form': missed_delivery_date_form, 'schedule': schedule})


@login_required
def delete_missed_delivery_date(request, pk):
    missed_delivery_date = get_object_or_404(MissedDeliveryDate, pk=pk)
    client = missed_delivery_date.schedule.client
    missed_delivery_date.delete()
    return redirect(client.get_absolute_url() + '#shopping-deliveries')


@login_required
def generate_shopping_deliveries(request, datestring):
    date = datetime.datetime.strptime(datestring, '%Y-%m-%d').date()
    schedules = ShoppingSchedule.objects.filter(status='active').filter(start_date__lte=date).filter(end_date__gte=date)

    for schedule in schedules:
        if schedule.client.shopping_deliveries.filter(date=date) or schedule.exception_dates.filter(date=date):
            continue
        if not schedule.includes_date(date):
            continue
        delivery = ShoppingDelivery(
            client=schedule.client,
            date=date,
            number_of_adults=schedule.number_of_adults,
            number_of_children=schedule.number_of_children,
            dietary_requirements=', '.join(schedule.get_dietary_requirements()),
            delivery_notes=schedule.delivery_notes
        )
        delivery.save()

    return redirect('/foodshopping/shoppingdelivery?date=' + datestring)
