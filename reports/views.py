from django.shortcuts import render, get_object_or_404, redirect
from client.models import Client, Referral, Casenote
from phonecalls.models import Phonecall
from foodhub.models import FoodhubCollection
from foodbank.models import FoodbankReferral
from foodshopping.models import ShoppingDelivery
from halalshopping.models import ShoppingCollection
from meals.models import MealsDelivery
from group.models import GroupSession
from childrensgroup.models import GroupSession as ChildrensGroupSession
from foodservice.models import GroupSession as FoodserviceGroupSession
from staff.models import Timesheet
from django.contrib.auth.decorators import login_required
import datetime


@login_required
def report_list(request):
    return render(request, 'report/report/list.html')


@login_required
def client_report(request):
    start = request.GET.get('start_date') or "2021-01-01"
    end = request.GET.get('end_date') or "2021-12-31"
    start_date = datetime.datetime.strptime(start, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end, '%Y-%m-%d').date()
    casenotes = Casenote.objects.filter(date__gte=start_date).filter(date__lte=end_date)
    casenote_clients = set([casenote.client for casenote in casenotes])
    phonecalls = Phonecall.objects.filter(date__gte=start_date).filter(date__lte=end_date)
    phonecall_clients = set([call.client for call in phonecalls])
    foodbank_referrals = FoodbankReferral.objects.filter(date__gte=start_date).filter(date__lte=end_date)
    foodbank_clients = set([referral.client for referral in foodbank_referrals])
    foodhub_collections = FoodhubCollection.objects.filter(date__gte=start_date).filter(date__lte=end_date)
    foodhub_clients = set([collection.client for collection in foodhub_collections])
    shopping_deliveries = ShoppingDelivery.objects.filter(date__gte=start_date).filter(date__lte=end_date)
    shopping_clients = set([delivery.client for delivery in shopping_deliveries])
    halal_collections = ShoppingCollection.objects.filter(date__gte=start_date).filter(date__lte=end_date)
    halal_clients = set([collection.client for collection in halal_collections])
    meal_deliveries = MealsDelivery.objects.filter(date__gte=start_date).filter(date__lte=end_date)
    meal_clients = set([delivery.client for delivery in meal_deliveries])
    group_sessions = GroupSession.objects.filter(date__gte=start_date).filter(date__lte=end_date)
    group_attendance = sum([len(session.attenders.all()) for session in group_sessions])
    group_clients = set([attender for session in group_sessions for attender in session.attenders.all()])
    childrens_group_sessions = ChildrensGroupSession.objects.filter(date__gte=start_date).filter(date__lte=end_date)
    childrens_group_attendance = sum([len(session.attenders.all()) for session in childrens_group_sessions])
    childrens_group_clients = set([attender for session in childrens_group_sessions for attender in session.attenders.all()])
    food_service_sessions = FoodserviceGroupSession.objects.filter(date__gte=start_date).filter(date__lte=end_date)
    food_service_attendance = sum([len(session.attenders.all()) for session in food_service_sessions])
    food_service_clients = set([attender for session in food_service_sessions for attender in session.attenders.all()])
    service_clients = phonecall_clients.union(foodbank_clients, foodhub_clients, shopping_clients, halal_clients, meal_clients)
    all_clients = service_clients.union(group_clients, food_service_clients)
    all_service_uses = sum([len(service) for service in [phonecalls, foodbank_referrals, foodhub_collections, shopping_deliveries, halal_collections, meal_deliveries]])

    group_types = {session.group.group_type.name: {'attendances': 0, 'clients': [], 'sessions': 0} for session in group_sessions}
    for session in group_sessions:
        attenders = session.attenders.all()
        group_type = session.group.group_type.name
        group_types[group_type]['clients'] += attenders
        group_types[group_type]['sessions'] += 1
        group_types[group_type]['attendances'] += len(attenders)
    for group_type in group_types:
        num_clients = len(set(group_types[group_type]['clients']))
        group_types[group_type]['clients'] = num_clients

    childrens_group_types = {session.group.group_type.name: {'attendances': 0, 'clients': [], 'sessions': 0} for session in childrens_group_sessions}
    for session in childrens_group_sessions:
        attenders = session.attenders.all()
        group_type = session.group.group_type.name
        childrens_group_types[group_type]['clients'] += attenders
        childrens_group_types[group_type]['sessions'] += 1
        childrens_group_types[group_type]['attendances'] += len(attenders)
    for group_type in childrens_group_types:
        num_clients = len(set(childrens_group_types[group_type]['clients']))
        childrens_group_types[group_type]['clients'] = num_clients

    food_services = {session.group.group_type.name: {'attendances': 0, 'clients': [], 'sessions': 0} for session in food_service_sessions}
    for session in food_service_sessions:
        attenders = session.attenders.all()
        group_type = session.group.group_type.name
        food_services[group_type]['clients'] += attenders
        food_services[group_type]['sessions'] += 1
        food_services[group_type]['attendances'] += len(attenders)
    for group_type in food_services:
        num_clients = len(set(food_services[group_type]['clients']))
        food_services[group_type]['clients'] = num_clients

    return render(request, 'report/report/client.html', {
        'start': start,
        'end': end,
        'start_date': start_date,
        'end_date': end_date,
        'casenotes': len(casenotes),
        'casenote_clients': len(casenote_clients),
        'phonecalls': len(phonecalls),
        'phonecall_clients': len(phonecall_clients),
        'foodbank_referrals': len(foodbank_referrals),
        'foodbank_clients': len(foodbank_clients),
        'foodhub_collections': len(foodhub_collections),
        'foodhub_clients': len(foodhub_clients),
        'shopping_deliveries': len(shopping_deliveries),
        'shopping_clients': len(shopping_clients),
        'halal_collections': len(halal_collections),
        'halal_clients': len(halal_clients),
        'meal_deliveries': len(meal_deliveries),
        'meal_clients': len(meal_clients),
        'group_sessions': len(group_sessions),
        'group_attendance': group_attendance,
        'group_clients': len(group_clients),
        'childrens_group_sessions': len(childrens_group_sessions),
        'childrens_group_attendance': childrens_group_attendance,
        'childrens_group_clients': len(childrens_group_clients),
        'food_service_sessions': len(food_service_sessions),
        'food_service_attendance': food_service_attendance,
        'food_service_clients': len(food_service_clients),
        'service_clients': len(service_clients),
        'all_clients': len(all_clients),
        'all_service_uses': all_service_uses,
        'group_types': group_types,
        'childrens_group_types': childrens_group_types,
        'food_services': food_services
    })


@login_required
def timesheet_report(request):
    start = request.GET.get('start_date') or "2021-01-01"
    end = request.GET.get('end_date') or "2021-12-31"
    start_date = datetime.datetime.strptime(start, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end, '%Y-%m-%d').date()
    timesheets = Timesheet.objects.filter(week_commencing__gte=start_date).filter(week_commencing__lte=end_date)
    staff = {staff_member: None for staff_member in set([timesheet.staff for timesheet in timesheets])}
    for staff_member in staff:
        staff[staff_member] = sum([timesheet.total_hours() for timesheet in timesheets if timesheet.staff == staff_member])
    roles = {role: None for role in set([timesheet.get_role_display() for timesheet in timesheets])}
    for role in roles:
        roles[role] = sum([timesheet.total_hours() for timesheet in timesheets if timesheet.get_role_display() == role])
    return render(request, 'report/report/timesheet.html', {
        'start': start,
        'end': end,
        'start_date': start_date,
        'end_date': end_date,
        'timesheets': timesheets,
        'staff': staff,
        'roles': roles
    })
