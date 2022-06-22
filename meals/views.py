from django.shortcuts import render, get_object_or_404, redirect
from .models import MealsDelivery, MealsSchedule, ExceptionDate, MissedDeliveryDate
from client.models import Client
from django.contrib.auth.decorators import login_required
from .forms import MealsDeliveryForm, MealsScheduleForm, ExceptionDateForm, MissedDeliveryDateForm
from .filters import MealsDeliveryFilter
import datetime
from django.http import HttpResponse
import csv


@login_required
def meal_delivery_today(request):
    return redirect('/meals/mealdelivery?date=' + str(datetime.date.today()))


@login_required
def export_meal_deliveries(request, datestring):
    date = datetime.datetime.strptime(datestring, '%Y-%m-%d').date()
    deliveries = MealsDelivery.objects.filter(date=date)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="' + str(date) + ' Deliveries.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Address', 'Postcode', 'Emergency Contact', 'Emergency Contact Phone', 'Contact Person Relation', 'Dietary Requirements', 'Delivery Notes', 'Number of Adults', 'Number of Children'])
    for delivery in deliveries:
        client = delivery.client
        name = client.first_name + ' ' + delivery.client.last_name
        address = client.get_address()
        postcode = client.postcode
        emergency_contact_name = client.emergency_contact_name
        emergency_contact_phone = client.emergency_contact_phone
        dietary_requirements = delivery.dietary_requirements
        delivery_notes = delivery.delivery_notes
        number_of_adults = delivery.number_of_adults
        number_of_children = delivery.number_of_children
        writer.writerow([name, address, postcode, emergency_contact_name, emergency_contact_phone, emergency_contact_relation, dietary_requirements, delivery_notes, number_of_adults, number_of_children])
    return response

@login_required
def meal_delivery_list(request):
    meal_deliveries_filter = MealsDeliveryFilter(request.GET, queryset=MealsDelivery.objects.all())
    date = datetime.datetime.strptime(request.GET.get('date'), '%Y-%m-%d').date()
    weekday = date.weekday()
    client_ids = list(meal_deliveries_filter.qs.values_list('client__pk', flat=True))
    exception_date_ids = list(ExceptionDate.objects.filter(date=date).values_list('pk', flat=True))
    schedules = MealsSchedule.objects.filter(status='active').filter(start_date__lte=date).filter(end_date__gte=date).exclude(client__pk__in=client_ids).exclude(exception_dates__pk__in=exception_date_ids)
    if weekday == 0:
        schedules = schedules.filter(monday_delivery=True)
    elif weekday == 2:
        schedules = schedules.filter(wednesday_delivery=True)
    elif weekday == 4:
        schedules = schedules.filter(friday_delivery=True)
    else:
        schedules = []
    total_count = len(meal_deliveries_filter.qs) + len(schedules)
    return render(request, 'meals/mealdelivery/list.html', {'meal_deliveries_filter': meal_deliveries_filter, 'schedules': schedules, 'date': date, 'total_count': total_count})


@login_required
def create_meal_delivery(request):
    client_id = request.GET.get('client')
    type = request.GET.get('type')
    client = get_object_or_404(Client, pk=client_id)
    initial = {'client': client_id, 'type': type}
    if hasattr(client, 'meals_schedule'):
        schedule = client.meals_schedule
        initial['number_of_adults'] = schedule.number_of_adults
        initial['number_of_children'] = schedule.number_of_children
        initial['dietary_requirements'] = ', '.join(schedule.get_dietary_requirements())
        initial['delivery_notes'] = schedule.delivery_notes
    new_meal_delivery = None
    if request.method == 'POST':
        meal_delivery_form = MealsDeliveryForm(request.POST)
        if meal_delivery_form.is_valid():
            new_meal_delivery = meal_delivery_form.save()
            return redirect(client.get_absolute_url() + '#meal-deliveries')
    else:
        meal_delivery_form = MealsDeliveryForm(initial=initial)
    return render(request, 'meals/mealdelivery/edit.html', {'new_meal_delivery': new_meal_delivery, 'meal_delivery_form': meal_delivery_form, 'client': client})


@login_required
def edit_meal_delivery(request, pk):
    meal_delivery = get_object_or_404(MealsDelivery, pk=pk)
    client = meal_delivery.client
    if request.method == 'POST':
        meal_delivery_form = MealsDeliveryForm(request.POST, instance=meal_delivery)
        if meal_delivery_form.is_valid():
            meal_delivery = meal_delivery_form.save()
            if request.GET.get('referrer') == 'client':
                return redirect(client.get_absolute_url() + '#meal-deliveries')
            else:
                date = request.GET.get('date')
                return redirect('/meals/mealdelivery?date=' + str(date))
    else:
        meal_delivery_form = MealsDeliveryForm(instance=meal_delivery)
    return render(request, 'meals/mealdelivery/edit.html', {'meal_delivery_form': meal_delivery_form, 'client': client})


@login_required
def delete_meal_delivery(request, pk):
    meal_delivery = get_object_or_404(MealsDelivery, pk=pk)
    client = meal_delivery.client
    meal_delivery.delete()
    if request.GET.get('referrer') == 'client':
        return redirect(client.get_absolute_url() + '#meal-deliveries')
    else:
        date = request.GET.get('date')
        return redirect('/meals/mealdelivery?date=' + date)


@login_required
def create_meal_schedule(request):
    client_id = request.GET.get('client')
    client = get_object_or_404(Client, pk=client_id)
    initial = {'client': client_id}
    new_meal_schedule = None
    if request.method == 'POST':
        meal_schedule_form = MealsScheduleForm(request.POST)
        if meal_schedule_form.is_valid():
            new_meal_schedule = meal_schedule_form.save()
            return redirect(client.get_absolute_url() + '#meal-deliveries')
    else:
        meal_schedule_form = MealsScheduleForm(initial=initial)
    return render(request, 'meals/mealschedule/edit.html', {'new_meal_schedule': new_meal_schedule, 'meal_schedule_form': meal_schedule_form, 'client': client})


@login_required
def edit_meal_schedule(request, pk):
    meal_schedule = get_object_or_404(MealsSchedule, pk=pk)
    client = meal_schedule.client
    if request.method == 'POST':
        meal_schedule_form = MealsScheduleForm(request.POST, instance=meal_schedule)
        if meal_schedule_form.is_valid():
            meal_schedule = meal_schedule_form.save()
            return redirect(client.get_absolute_url() + '#meal-deliveries')
    else:
        meal_schedule_form = MealsScheduleForm(instance=meal_schedule)
    return render(request, 'meals/mealschedule/edit.html', {'meal_schedule_form': meal_schedule_form, 'client': client})


@login_required
def create_exception_date(request):
    schedule_id = request.GET.get('schedule')
    schedule = get_object_or_404(MealsSchedule, pk=schedule_id)
    initial = {'schedule': schedule}
    new_exception_date = None
    if request.method == 'POST':
        exception_date_form = ExceptionDateForm(request.POST)
        if exception_date_form.is_valid():
            new_exception_date = exception_date_form.save()
            for delivery in schedule.client.meals_deliveries.all():
                if delivery.date == new_exception_date.date:
                    delivery.delete()
            return redirect(schedule.client.get_absolute_url() + '#meal-deliveries')
    else:
        exception_date_form = ExceptionDateForm(initial=initial)
    return render(request, 'meals/exceptiondate/edit.html', {'new_exception_date': new_exception_date, 'exception_date_form': exception_date_form, 'schedule': schedule})


@login_required
def delete_exception_date(request, pk):
    exception_date = get_object_or_404(ExceptionDate, pk=pk)
    client = exception_date.schedule.client
    exception_date.delete()
    return redirect(client.get_absolute_url() + '#meal-deliveries')


@login_required
def create_missed_delivery_date(request):
    schedule_id = request.GET.get('schedule')
    schedule = get_object_or_404(MealsSchedule, pk=schedule_id)
    initial = {'schedule': schedule}
    new_missed_delivery_date = None
    if request.method == 'POST':
        missed_delivery_date_form = MissedDeliveryDateForm(request.POST)
        if missed_delivery_date_form.is_valid():
            new_missed_delivery_date = missed_delivery_date_form.save()
            for delivery in schedule.client.meals_deliveries.all():
                if delivery.date == new_missed_delivery_date.date:
                    delivery.delete()
            return redirect(schedule.client.get_absolute_url() + '#meal-deliveries')
    else:
        missed_delivery_date_form = MissedDeliveryDateForm(initial=initial)
    return render(request, 'meals/misseddeliverydate/edit.html', {'new_missed_delivery_date': new_missed_delivery_date, 'missed_delivery_date_form': missed_delivery_date_form, 'schedule': schedule})


@login_required
def delete_missed_delivery_date(request, pk):
    missed_delivery_date = get_object_or_404(MissedDeliveryDate, pk=pk)
    client = missed_delivery_date.schedule.client
    missed_delivery_date.delete()
    return redirect(client.get_absolute_url() + '#meal-deliveries')


@login_required
def generate_meal_deliveries(request, datestring):
    date = datetime.datetime.strptime(datestring, '%Y-%m-%d').date()
    schedules = MealsSchedule.objects.filter(status='active').filter(start_date__lte=date).filter(end_date__gte=date)

    day_of_week = date.weekday()
    if day_of_week == 0:
        schedules = schedules.filter(monday_delivery=True)
    elif day_of_week == 2:
        schedules = schedules.filter(wednesday_delivery=True)
    elif day_of_week == 4:
        schedules = schedules.filter(friday_delivery=True)
    else:
        return redirect('/meals/mealdelivery?date=' + datestring)

    for schedule in schedules:
        if schedule.client.meals_deliveries.filter(date=date) or schedule.exception_dates.filter(date=date):
            continue
        delivery = MealsDelivery(
            client=schedule.client,
            date=date,
            number_of_adults=schedule.number_of_adults,
            number_of_children=schedule.number_of_children,
            dietary_requirements=', '.join(schedule.get_dietary_requirements()),
            delivery_notes=schedule.delivery_notes
        )
        delivery.save()

    return redirect('/meals/mealdelivery?date=' + datestring)
