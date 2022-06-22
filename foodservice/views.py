from django.shortcuts import render, get_object_or_404, redirect
from .models import GroupType, Group, GroupSession, GroupBooking
from client.models import Client
from django.contrib.auth.decorators import login_required
from .forms import GroupTypeForm, GroupForm, GroupSessionForm, GroupBookingForm, BulkGroupSessionForm
from .filters import GroupFilter, GroupSessionFilter
import datetime
from django.http import HttpResponse
import csv


@login_required
def group_type_list(request):
    group_types = GroupType.objects.all()
    groups = Group.objects.all()
    return render(request, 'foodservice/grouptype/list.html', {'group_types': group_types, 'groups': groups})


@login_required
def group_type_detail(request, pk):
    group_type = get_object_or_404(GroupType, pk=pk)
    return render(request, 'foodservice/grouptype/detail.html', {'group_type': group_type})


@login_required
def edit_group_type(request, pk):
    group_type = get_object_or_404(GroupType, pk=pk)
    if request.method == 'POST':
        group_type_form = GroupTypeForm(request.POST, instance=group_type)
        if group_type_form.is_valid():
            group_type = group_type_form.save()
            return redirect(group_type.get_absolute_url())
    else:
        group_type_form = GroupTypeForm(instance=group_type)
    return render(request, 'foodservice/grouptype/edit.html', {'group_type_form': group_type_form, 'group_type': group_type})



@login_required
def create_group_type(request):
    new_group_type = None
    if request.method == 'POST':
        group_type_form = GroupTypeForm(request.POST)
        if group_type_form.is_valid():
            new_group_type = group_type_form.save()
            return redirect(new_group_type.get_absolute_url())
    else:
        group_type_form = GroupTypeForm()
    return render(request, 'foodservice/grouptype/edit.html', {'new_group_type': new_group_type, 'group_type_form': group_type_form})


@login_required
def group_detail(request, pk):
    group = get_object_or_404(Group, pk=pk)
    sessions = group.sessions.all()
    bookings = group.bookings.all()
    bookers = [booking.client for booking in bookings]
    return render(request, 'foodservice/group/detail.html',
        {
            'group': group,
            'sessions': sessions,
            'bookings': bookings,
        }
    )


@login_required
def create_group(request):
    group_type_id = request.GET.get('grouptype')
    group_type = get_object_or_404(GroupType, pk=group_type_id)
    initial = {'group_type': group_type}
    new_group = None
    if request.method == 'POST':
        group_form = GroupForm(request.POST)
        if group_form.is_valid():
            new_group = group_form.save()
            return redirect(new_group.get_absolute_url())
    else:
        group_form = GroupForm(initial=initial)
    return render(request, 'foodservice/group/edit.html', {'new_group': new_group, 'group_form': group_form, 'group_type': group_type, 'action': 'create'})


@login_required
def edit_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    group_type = group.group_type
    if request.method == 'POST':
        group_form = GroupForm(request.POST, instance=group)
        if group_form.is_valid():
            group = group_form.save()
            return redirect(group.get_absolute_url())
    else:
        group_form = GroupForm(instance=group)
    return render(request, 'foodservice/group/edit.html', {'group_form': group_form, 'group_type': group_type, 'group': group, 'action': 'edit'})


@login_required
def delete_group(request, pk):
    group = get_object_or_404(Group, pk=pk)
    group_type = group.group_type
    if not group.bookings.all():
        group.delete()
    return redirect(group_type.get_absolute_url())


@login_required
def group_session_list(request):
    group_sessions_filter = GroupSessionFilter(request.GET, queryset=GroupSession.objects.all())
    return render(request, 'foodservice/groupsession/list.html', {'group_sessions_filter': group_sessions_filter})


@login_required
def group_session_detail(request, pk):
    group_session = get_object_or_404(GroupSession, pk=pk)
    attenders = group_session.attenders.all()
    active_bookers = [booking.client for booking in group_session.group.bookings.filter(active=True)]
    inactive_bookers = [booking.client for booking in group_session.group.bookings.filter(active=False)]
    return render(request, 'foodservice/groupsession/detail.html',
        {
            'group_session': group_session,
            'attenders': attenders,
            'active_bookers': active_bookers,
            'inactive_bookers': inactive_bookers
        }
    )


@login_required
def create_group_session(request):
    group_id = request.GET.get('group')
    group = get_object_or_404(Group, pk=group_id)
    initial = {'group': group}
    new_group_session = None
    if request.method == 'POST':
        group_session_form = GroupSessionForm(request.POST)
        if group_session_form.is_valid():
            new_group_session = group_session_form.save()
            return redirect(group.get_absolute_url() + '#group-sessions')
    else:
        group_session_form = GroupSessionForm(initial=initial)
    return render(request, 'foodservice/groupsession/edit.html', {'new_group_session': new_group_session, 'group_session_form': group_session_form, 'group': group})


@login_required
def create_bulk_group_sessions(request):
    group_id = request.GET.get('group')
    group = get_object_or_404(Group, pk=group_id)
    initial = {'group': group}
    if request.method == 'POST':
        bulk_group_session_form = BulkGroupSessionForm(request.POST)
        if bulk_group_session_form.is_valid():
            start_date = bulk_group_session_form.cleaned_data['start_date']
            end_date = bulk_group_session_form.cleaned_data['end_date']
            time = bulk_group_session_form.cleaned_data['time']
            monday = bulk_group_session_form.cleaned_data['monday']
            tuesday = bulk_group_session_form.cleaned_data['tuesday']
            wednesday = bulk_group_session_form.cleaned_data['wednesday']
            thursday = bulk_group_session_form.cleaned_data['thursday']
            friday = bulk_group_session_form.cleaned_data['friday']

            num_of_days = (end_date - start_date).days
            for i in range(num_of_days):
                the_date = start_date + datetime.timedelta(days=i)
                the_weekday = the_date.weekday()
                # Check that the group doesn't already have a session on that day?
                if (monday and the_weekday == 0) or (tuesday and the_weekday == 1) or (wednesday and the_weekday == 2) or (thursday and the_weekday == 3) or (friday and the_weekday == 4):
                    group_session = GroupSession(
                        group=group,
                        date=the_date,
                        time=time
                    )
                    group_session.save()
            return redirect(group.get_absolute_url() + '#group-sessions')
    else:
        bulk_group_session_form = BulkGroupSessionForm(initial=initial)
    return render(request, 'foodservice/groupsession/bulk-edit.html', {'bulk_group_session_form': bulk_group_session_form, 'group': group})


@login_required
def edit_group_session(request, pk):
    group_session = get_object_or_404(GroupSession, pk=pk)
    group = group_session.group
    if request.method == 'POST':
        group_session_form = GroupSessionForm(request.POST, instance=group_session)
        if group_session_form.is_valid():
            group_session = group_session_form.save()
            return redirect(group.get_absolute_url() + '#group-sessions')
    else:
        group_session_form = GroupSessionForm(instance=group_session)
    return render(request, 'foodservice/groupsession/edit.html', {'group_session_form': group_session_form, 'group_session': group_session, 'group': group})


@login_required
def delete_group_session(request, pk):
    group_session = get_object_or_404(GroupSession, pk=pk)
    group = group_session.group
    group_session.delete()
    return redirect(group.get_absolute_url() + '#group-sessions')


@login_required
def add_group_session_attender(request, pk):
    group_session = get_object_or_404(GroupSession, pk=pk)
    client_id = request.GET.get('client')
    client = get_object_or_404(Client, pk=client_id)
    group_session.attenders.add(client)
    return redirect(group_session.get_absolute_url())


@login_required
def remove_group_session_attender(request, pk):
    group_session = get_object_or_404(GroupSession, pk=pk)
    client_id = request.GET.get('client')
    client = get_object_or_404(Client, pk=client_id)
    group_session.attenders.remove(client)
    return redirect(group_session.get_absolute_url())


@login_required
def create_group_booking(request):
    client_id = request.GET.get('client')
    client = get_object_or_404(Client, pk=client_id)
    initial = {'client': client}
    new_group_booking = None
    if request.method == 'POST':
        group_booking_form = GroupBookingForm(request.POST)
        if group_booking_form.is_valid():
            new_group_booking = group_booking_form.save()
            return redirect(client.get_absolute_url() + '#food-services')
    else:
        group_booking_form = GroupBookingForm(initial=initial)
    return render(request, 'foodservice/groupbooking/edit.html', {'new_group_booking': new_group_booking, 'group_booking_form': group_booking_form, 'client': client, 'referrer': 'client'})


@login_required
def edit_group_booking(request, pk):
    group_booking = get_object_or_404(GroupBooking, pk=pk)
    group = group_booking.group
    client = group_booking.client
    referrer = request.GET.get('referrer')
    if request.method == 'POST':
        group_booking_form = GroupBookingForm(request.POST, instance=group_booking)
        if group_booking_form.is_valid():
            group_booking = group_booking_form.save()
            if referrer == 'client':
                return redirect(client.get_absolute_url() + '#groups')
            else:
                return redirect(group.get_absolute_url() + '#group-bookings')
    else:
        group_booking_form = GroupBookingForm(instance=group_booking)
    return render(request, 'foodservice/groupbooking/edit.html', {'group_booking_form': group_booking_form, 'group_booking': group_booking, 'group': group, 'client': client, 'referrer': referrer})


@login_required
def delete_group_booking(request, pk):
    referrer = request.GET.get('referrer')
    group_booking = get_object_or_404(GroupBooking, pk=pk)
    group_booking.delete()
    if referrer == 'client':
        return redirect(group_booking.client.get_absolute_url() + '#food-services')
    else:
        return redirect(group_booking.group.get_absolute_url() + '#group-bookings')


@login_required
def prune_group_bookings(request, pk):
    group = get_object_or_404(Group, pk=pk)
    active_bookings = group.bookings.filter(active=True)
    for booking in active_bookings:
        client = booking.client
        five_weeks_ago = datetime.date.today() - datetime.timedelta(days=35)
        client_attendance = client.attended_foodservice_sessions.filter(group=group).filter(date__gte=five_weeks_ago)
        if not client_attendance:
            booking.active = False
            booking.save()
    return redirect(group.get_absolute_url() + '#group-bookings')
