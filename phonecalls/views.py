from django.shortcuts import render, get_object_or_404, redirect
from .models import Phonecall, PhonecallSchedule, ExceptionDate, MissedCallDate, PhonecallNotes
from client.models import Client
from django.contrib.auth.decorators import login_required
from .forms import PhonecallScheduleForm, PhonecallForm, ExceptionDateForm, MissedCallDateForm, PhonecallNotesForm
from .filters import PhonecallFilter
import datetime
from django.http import HttpResponse
import csv


@login_required
def phonecall_today(request):
    return redirect('/phonecalls/phonecall?date=' + str(datetime.date.today()))


@login_required
def export_phonecalls(request, datestring):
    pass


@login_required
def phonecall_list(request):
    phonecalls_filter = PhonecallFilter(request.GET, queryset=Phonecall.objects.all())
    date = datetime.datetime.strptime(request.GET.get('date'), '%Y-%m-%d').date()
    weekday = date.weekday()
    client_ids = list(phonecalls_filter.qs.values_list('client__pk', flat=True))
    exception_date_ids = list(ExceptionDate.objects.filter(date=date).values_list('pk', flat=True))
    schedules = PhonecallSchedule.objects.filter(status='active').filter(start_date__lte=date).filter(end_date__gte=date).exclude(client__pk__in=client_ids).exclude(exception_dates__pk__in=exception_date_ids).order_by('-time_of_day')
    schedule_ids = [schedule.pk for schedule in schedules if not schedule.includes_date(date)]
    schedules = schedules.exclude(pk__in=schedule_ids)
    total_count = len(schedules) + len(phonecalls_filter.qs)
    return render(request, 'phonecalls/phonecall/list.html', {'phonecalls_filter': phonecalls_filter, 'schedules': schedules, 'date': date, 'total_count': total_count})


@login_required
def create_phonecall(request):
    client_id = request.GET.get('client')
    type = request.GET.get('type')
    client = get_object_or_404(Client, pk=client_id)
    initial = {'client': client_id, 'type': type}
    new_phonecall = None
    if request.method == 'POST':
        phonecall_form = PhonecallForm(request.POST)
        if phonecall_form.is_valid():
            new_phonecall = phonecall_form.save()
            return redirect(client.get_absolute_url() + '#phonecalls')
    else:
        phonecall_form = PhonecallForm(initial=initial)
    return render(request, 'phonecalls/phonecall/edit.html', {'new_phonecall': new_phonecall, 'phonecall_form': phonecall_form, 'client': client})


@login_required
def edit_phonecall(request, pk):
    phonecall = get_object_or_404(PhonecallSchedule, pk=pk)
    client = phonecall.client
    if request.method == 'POST':
        phonecall_form = PhonecallForm(request.POST, instance=phonecall)
        if phonecall_form.is_valid():
            phonecall = phonecall_form.save()
            if request.GET.get('referrer') == 'client':
                return redirect(client.get_absolute_url() + '#phonecalls')
            else:
                date = request.GET.get('date')
                return redirect('/phonecalls/phonecall?date=' + str(date))
    else:
        phonecall_form = PhonecallForm(instance=phonecall)
    return render(request, 'phonecalls/phonecall/edit.html', {'phonecall_form': phonecall_form, 'client': client})


@login_required
def delete_phonecall(request, pk):
    phonecall = get_object_or_404(Phonecall, pk=pk)
    client = phonecall.client
    phonecall.delete()
    if request.GET.get('referrer') == 'client':
        return redirect(client.get_absolute_url() + '#phonecalls')
    else:
        date = request.GET.get('date')
        return redirect('/phonecalls/phonecall?date=' + date)


@login_required
def create_phonecall_schedule(request):
    client_id = request.GET.get('client')
    client = get_object_or_404(Client, pk=client_id)
    initial = {'client': client_id}
    new_phonecall_schedule = None
    if request.method == 'POST':
        phonecall_schedule_form = PhonecallScheduleForm(request.POST)
        if phonecall_schedule_form.is_valid():
            new_phonecall_schedule = phonecall_schedule_form.save()
            return redirect(client.get_absolute_url() + '#phonecalls')
    else:
        phonecall_schedule_form = PhonecallScheduleForm(initial=initial)
    return render(request, 'phonecalls/phonecallschedule/edit.html', {'new_phonecall_schedule': new_phonecall_schedule, 'phonecall_schedule_form': phonecall_schedule_form, 'client': client})


@login_required
def edit_phonecall_schedule(request, pk):
    phonecall_schedule = get_object_or_404(PhonecallSchedule, pk=pk)
    client = phonecall_schedule.client
    if request.method == 'POST':
        phonecall_schedule_form = PhonecallScheduleForm(request.POST, instance=phonecall_schedule)
        if phonecall_schedule_form.is_valid():
            phonecall_schedule = phonecall_schedule_form.save()
            return redirect(client.get_absolute_url())
    else:
        phonecall_schedule_form = PhonecallScheduleForm(instance=phonecall_schedule)
    return render(request, 'phonecalls/phonecallschedule/edit.html', {'phonecall_schedule_form': phonecall_schedule_form, 'client': client})


@login_required
def create_exception_date(request):
    schedule_id = request.GET.get('schedule')
    schedule = get_object_or_404(PhonecallSchedule, pk=schedule_id)
    initial = {'schedule': schedule}
    new_exception_date = None
    if request.method == 'POST':
        exception_date_form = ExceptionDateForm(request.POST)
        if exception_date_form.is_valid():
            new_exception_date = exception_date_form.save()
            for phonecall in schedule.client.phonecalls.all():
                if phonecall.date == new_exception_date.date:
                    phonecall.delete()
            return redirect(schedule.client.get_absolute_url() + '#phonecalls')
    else:
        exception_date_form = ExceptionDateForm(initial=initial)
    return render(request, 'phonecalls/exceptiondate/edit.html', {'new_exception_date': new_exception_date, 'exception_date_form': exception_date_form, 'schedule': schedule})


@login_required
def delete_exception_date(request, pk):
    exception_date = get_object_or_404(ExceptionDate, pk=pk)
    client = exception_date.schedule.client
    exception_date.delete()
    return redirect(client.get_absolute_url() + '#phonecalls')


@login_required
def create_missed_call_date(request):
    schedule_id = request.GET.get('schedule')
    schedule = get_object_or_404(PhonecallSchedule, pk=schedule_id)
    initial = {'schedule': schedule}
    new_missed_call_date = None
    if request.method == 'POST':
        missed_call_date_form = MissedCallDateForm(request.POST)
        if missed_call_date_form.is_valid():
            new_missed_call_date = missed_call_date_form.save()
            for phonecall in schedule.client.phonecalls.all():
                if phonecall.date == new_missed_call_date.date:
                    phonecall.delete()
            return redirect(schedule.client.get_absolute_url() + '#phonecalls')
    else:
        missed_call_date_form = MissedCallDateForm(initial=initial)
    return render(request, 'phonecalls/missedcalldate/edit.html', {'new_missed_call_date': new_missed_call_date, 'missed_call_date_form': missed_call_date_form, 'schedule': schedule})


@login_required
def delete_missed_call_date(request, pk):
    missed_call_date = get_object_or_404(MissedCallDate, pk=pk)
    client = missed_call_date.schedule.client
    missed_call_date.delete()
    return redirect(client.get_absolute_url() + '#phonecalls')


@login_required
def create_phonecall_notes(request):
    schedule_id = request.GET.get('schedule')
    schedule = get_object_or_404(PhonecallSchedule, pk=schedule_id)
    initial = {'schedule': schedule}
    new_phonecall_notes = None
    if request.method == 'POST':
        phonecall_notes_form = PhonecallNotesForm(request.POST)
        if phonecall_notes_form.is_valid():
            new_phonecall_notes = phonecall_notes_form.save()
            return redirect(schedule.client.get_absolute_url() + '#phonecalls')
    else:
        phonecall_notes_form = PhonecallNotesForm(initial=initial)
    return render(request, 'phonecalls/phonecallnotes/edit.html', {'new_phonecall_notes': new_phonecall_notes, 'phonecall_notes_form': phonecall_notes_form, 'schedule': schedule})


@login_required
def delete_phonecall_notes(request, pk):
    phonecall_notes = get_object_or_404(PhonecallNotes, pk=pk)
    client = phonecall_notes.schedule.client
    phonecall_notes.delete()
    return redirect(client.get_absolute_url() + '#phonecalls')


@login_required
def generate_phonecalls(request, datestring):
    date = datetime.datetime.strptime(datestring, '%Y-%m-%d').date()
    schedules = PhonecallSchedule.objects.filter(status='active').filter(start_date__lte=date).filter(end_date__gte=date)

    for schedule in schedules:
        if schedule.client.phonecalls.filter(date=date) or schedule.exception_dates.filter(date=date):
            continue
        if not schedule.includes_date(date):
            continue
        phonecall = Phonecall(
            client=schedule.client,
            date=date,
            time_of_day=schedule.time_of_day,
        )
        phonecall.save()

    return redirect('/phonecalls/phonecall?date=' + datestring)
