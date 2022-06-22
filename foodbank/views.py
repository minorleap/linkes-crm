from django.shortcuts import render, get_object_or_404, redirect
from .models import FoodbankReferral
from client.models import Client
from django.contrib.auth.decorators import login_required
from .forms import FoodbankReferralForm
from .filters import FoodbankReferralFilter
import datetime


@login_required
def foodbank_referral_today(request):
    return redirect('/foodbank/referral?date=' + str(datetime.date.today()))


@login_required
def foodbank_referral_list(request):
    foodbank_referral_filter = FoodbankReferralFilter(request.GET, queryset=FoodbankReferral.objects.all())
    date = datetime.datetime.strptime(request.GET.get('date'), '%Y-%m-%d').date()
    return render(request, 'foodbank/referral/list.html', {'foodbank_referral_filter': foodbank_referral_filter, 'date': date})


@login_required
def create_foodbank_referral(request):
    client_id = request.GET.get('client')
    client = get_object_or_404(Client, pk=client_id)
    initial = {'client': client}
    new_foodbank_referral = None
    if request.method == 'POST':
        foodbank_referral_form = FoodbankReferralForm(request.POST)
        if foodbank_referral_form.is_valid():
            new_foodbank_referral = foodbank_referral_form.save()
            return redirect(client.get_absolute_url() + '#foodbank')
    else:
        foodbank_referral_form = FoodbankReferralForm(initial=initial)
    return render(request, 'foodbank/referral/edit.html', {'new_foodbank_referral': new_foodbank_referral, 'foodbank_referral_form': foodbank_referral_form, 'client': client})


@login_required
def edit_foodbank_referral(request, pk):
    foodbank_referral = get_object_or_404(FoodbankReferral, pk=pk)
    client = foodbank_referral.client
    if request.method == 'POST':
        foodbank_referral_form = FoodbankReferralForm(request.POST, instance=foodbank_referral)
        if foodbank_referral_form.is_valid():
            foodbank_referral = foodbank_referral_form.save()
            if request.GET.get('referrer') == 'client':
                return redirect(client.get_absolute_url() + '#foodbank')
            else:
                date = request.GET.get('date')
                return redirect('/foodbank/referral?date=' + str(date))
    else:
        foodbank_referral_form = FoodbankReferralForm(instance=foodbank_referral)
    return render(request, 'foodbank/referral/edit.html', {'foodbank_referral_form': foodbank_referral_form, 'foodbank_referral': foodbank_referral, 'client': client})


@login_required
def delete_foodbank_referral(request, pk):
    foodbank_referral = get_object_or_404(FoodbankReferral, pk=pk)
    referrer = request.GET.get('referrer')
    date = request.GET.get('date')
    client = foodbank_referral.client
    foodbank_referral.delete()
    if referrer == 'client':
        return redirect(client.get_absolute_url() + '#foodbank')
    else:
        return redirect('/foodbank?date=' + date)
