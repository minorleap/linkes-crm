from django.shortcuts import render, get_object_or_404, redirect
from .models import Staff, Role, Timesheet
from django.contrib.auth.decorators import login_required
from .forms import StaffForm, RoleForm, TimesheetFormSet
from .filters import StaffFilter, TimesheetsFilter
import datetime
#from django.forms import modelformset_factory


@login_required
def staff_list(request):
    staff_filter = StaffFilter(request.GET, queryset=Staff.objects.all())
    return render(request, 'staff/staff/list.html', {'staff_filter': staff_filter})


@login_required
def staff_detail(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    roles = staff.roles.all()
    return render(request, 'staff/staff/detail.html', {'staff': staff, 'roles': roles})


@login_required
def create_staff(request):
    first_name = request.GET.get('firstname')
    last_name = request.GET.get('lastname')
    postcode = request.GET.get('postcode')
    initial = {'first_name': first_name, 'last_name': last_name, 'postcode': postcode}
    new_staff = None
    if request.method == 'POST':
        staff_form = StaffForm(request.POST)
        if staff_form.is_valid():
            new_staff = staff_form.save()
            return redirect(new_staff.get_absolute_url())
    else:
        staff_form = StaffForm(initial=initial)
    return render(request, 'staff/staff/edit.html', {'new_staff': new_staff, 'staff_form': staff_form})


@login_required
def edit_staff(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        staff_form = StaffForm(request.POST, instance=staff)
        if staff_form.is_valid():
            staff = staff_form.save()
            return redirect(staff.get_absolute_url())
    else:
        staff_form = StaffForm(instance=staff)
    return render(request, 'staff/staff/edit.html', {'staff_form': staff_form, 'staff': staff})


@login_required
def create_role(request):
    staff_id = request.GET.get('staff')
    staff = get_object_or_404(Staff, pk=staff_id)
    initial = {'staff': staff}
    new_role = None
    if request.method == 'POST':
        role_form = RoleForm(request.POST)
        if role_form.is_valid():
            new_role = role_form.save()
            return redirect(staff.get_absolute_url())
    else:
        role_form = RoleForm(initial=initial)
    return render(request, 'staff/role/edit.html', {'new_role': new_role, 'role_form': role_form, 'staff': staff})


@login_required
def delete_role(request, pk):
    role = get_object_or_404(Role, pk=pk)
    staff = role.staff
    role.delete()
    return redirect(staff.get_absolute_url())


@login_required
def timesheet_list(request):
    timesheets_filter = TimesheetsFilter(request.GET, queryset=Timesheet.objects.all())

    # if week_commencing param isn't set, go to current week
    if not request.GET.get('week_commencing'):
        return redirect('/staff/timesheet?week_commencing=' + str(datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())))

    week_commencing = datetime.datetime.strptime(request.GET.get('week_commencing'), '%Y-%m-%d').date()

    # if week_commencing date is not a monday, go to the previous monday
    if week_commencing.weekday() != 0:
        week_commencing -= datetime.timedelta(days=week_commencing.weekday())
        return redirect('/staff/timesheet?week_commencing=' + str(week_commencing))

    previous_week = week_commencing - datetime.timedelta(days=7)
    next_week = week_commencing + datetime.timedelta(days=7)
    
    if request.method == 'POST':
        formset = TimesheetFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                # set week_commencing based on the url param
                instance.week_commencing = week_commencing
                if instance.monday_hours == None:
                    instance.monday_hours = 0
                if instance.tuesday_hours == None:
                    instance.tuesday_hours = 0
                if instance.wednesday_hours == None:
                    instance.wednesday_hours = 0
                if instance.thursday_hours == None:
                    instance.thursday_hours = 0
                if instance.friday_hours == None:
                    instance.friday_hours = 0
                if instance.saturday_hours == None:
                    instance.saturday_hours = 0
                instance.save()
        else:
            print(formset.errors)

    formset = TimesheetFormSet(queryset=timesheets_filter.qs)
    return render(request, 'staff/timesheet/list.html', {'timesheets_filter': timesheets_filter, 'formset': formset, 'previous_week': previous_week, 'next_week': next_week})
