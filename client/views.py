from django.shortcuts import render, get_object_or_404, redirect
from .models import Client, Referral, Casenote
from django.contrib.auth.decorators import login_required
from .forms import ClientForm, ReferralForm, CasenoteForm
from .filters import ClientFilter
import datetime


@login_required
def client_list(request):
    clients_filter = ClientFilter(request.GET, queryset=Client.objects.all())
    return render(request, 'client/client/list.html', {'clients_filter': clients_filter})


@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    referrals = client.referrals.all()
    casenotes = client.casenotes.all()

    adhoc_meals_deliveries = client.meals_deliveries.filter(type='ad-hoc').filter(date__gte=datetime.date.today())
    meal_exception_dates = None
    meal_missed_delivery_dates = None
    if hasattr(client, 'meals_schedule'):
        meal_exception_dates = client.meals_schedule.exception_dates.filter(date__gte=datetime.date.today())
        meal_missed_delivery_dates = client.meals_schedule.missed_delivery_dates.all()

    adhoc_shopping_deliveries = client.shopping_deliveries.filter(type='ad-hoc').filter(date__gte=datetime.date.today())
    food_shopping_exception_dates = None
    food_shopping_missed_delivery_dates = None
    if hasattr(client, 'food_shopping_schedule'):
        food_shopping_exception_dates = client.food_shopping_schedule.exception_dates.filter(date__gte=datetime.date.today())
        food_shopping_missed_delivery_dates = client.food_shopping_schedule.missed_delivery_dates.all()

    adhoc_shopping_collections = client.shopping_collections.filter(type='ad-hoc').filter(date__gte=datetime.date.today())
    halal_shopping_exception_dates = None
    halal_shopping_missed_collection_dates = None
    if hasattr(client, 'halal_shopping_schedule'):
        halal_shopping_exception_dates = client.halal_shopping_schedule.exception_dates.filter(date__gte=datetime.date.today())
        halal_shopping_missed_collection_dates = client.halal_shopping_schedule.missed_collection_dates.all()

    adhoc_phonecalls = client.phonecalls.filter(type='ad-hoc').filter(date__gte=datetime.date.today())
    phonecall_exception_dates = None
    phonecall_missed_call_dates = None
    phonecall_notes = None
    if hasattr(client, 'phonecall_schedule'):
        phonecall_exception_dates = client.phonecall_schedule.exception_dates.filter(date__gte=datetime.date.today())
        phonecall_missed_call_dates = client.phonecall_schedule.missed_call_dates.all()
        phonecall_notes = client.phonecall_schedule.phonecall_notes.all()

    return render(request, 'client/client/detail.html',
        {
            'client': client,
            'referrals': referrals,
            'casenotes': casenotes,
            'adhoc_meals_deliveries': adhoc_meals_deliveries,
            'meal_exception_dates': meal_exception_dates,
            'meal_missed_delivery_dates': meal_missed_delivery_dates,
            'adhoc_shopping_deliveries': adhoc_shopping_deliveries,
            'food_shopping_exception_dates': food_shopping_exception_dates,
            'food_shopping_missed_delivery_dates': food_shopping_missed_delivery_dates,
            'adhoc_shopping_collections': adhoc_shopping_collections,
            'halal_shopping_exception_dates': halal_shopping_exception_dates,
            'halal_shopping_missed_collection_dates': halal_shopping_missed_collection_dates,
            'adhoc_phonecalls': adhoc_phonecalls,
            'phonecall_exception_dates': phonecall_exception_dates,
            'phonecall_missed_call_dates': phonecall_missed_call_dates,
            'phonecall_notes': phonecall_notes,
        }
    )


@login_required
def create_client(request):
    first_name = request.GET.get('firstname')
    last_name = request.GET.get('lastname')
    postcode = request.GET.get('postcode')
    initial = {'first_name': first_name, 'last_name': last_name, 'postcode': postcode}
    new_client = None
    if request.method == 'POST':
        client_form = ClientForm(request.POST)
        if client_form.is_valid():
            new_client = client_form.save()
            return redirect(new_client.get_absolute_url())
    else:
        client_form = ClientForm(initial=initial)
    return render(request, 'client/client/edit.html', {'new_client': new_client, 'client_form': client_form})


@login_required
def edit_client(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client_form = ClientForm(request.POST, instance=client)
        if client_form.is_valid():
            client = client_form.save()
            return redirect(client.get_absolute_url())
    else:
        client_form = ClientForm(instance=client)
    return render(request, 'client/client/edit.html', {'client_form': client_form, 'client': client})


@login_required
def create_referral(request):
    client_id = request.GET.get('client')
    client = get_object_or_404(Client, pk=client_id)
    initial = {'client': client}
    new_referral = None
    if request.method == 'POST':
        referral_form = ReferralForm(request.POST)
        if referral_form.is_valid():
            new_referral = referral_form.save()
            return redirect(client.get_absolute_url())
    else:
        referral_form = ReferralForm(initial=initial)
    return render(request, 'client/referral/edit.html', {'new_referral': new_referral, 'referral_form': referral_form, 'client': client})


@login_required
def delete_referral(request, pk):
    referral = get_object_or_404(Referral, pk=pk)
    client = referral.client
    referral.delete()
    return redirect(client.get_absolute_url())


@login_required
def create_casenote(request):
    client_id = request.GET.get('client')
    client = get_object_or_404(Client, pk=client_id)
    initial = {'client': client}
    new_casenote = None
    if request.method == 'POST':
        casenote_form = CasenoteForm(request.POST)
        if casenote_form.is_valid():
            new_casenote = casenote_form.save()
            return redirect(client.get_absolute_url() + "#casenotes")
    else:
        casenote_form = CasenoteForm(initial=initial)
    return render(request, 'client/casenote/edit.html', {'new_casenote': new_casenote, 'casenote_form': casenote_form, 'client': client})


@login_required
def edit_casenote(request, pk):
    casenote = get_object_or_404(Casenote, pk=pk)
    client = casenote.client
    if request.method == 'POST':
        casenote_form = CasenoteForm(request.POST, instance=casenote)
        if casenote_form.is_valid():
            casenote = casenote_form.save()
            return redirect(client.get_absolute_url() + "#casenotes")
    else:
        casenote_form = CasenoteForm(instance=casenote)
    return render(request, 'client/casenote/edit.html', {'casenote_form': casenote_form, 'client': client, 'casenote': casenote})


@login_required
def delete_casenote(request, pk):
    casenote = get_object_or_404(Casenote, pk=pk)
    client = casenote.client
    casenote.delete()
    return redirect(client.get_absolute_url() + "#casenotes")
