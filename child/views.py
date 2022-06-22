from django.shortcuts import render, get_object_or_404, redirect
from .models import Child, Client
from django.contrib.auth.decorators import login_required
from .forms import ChildForm
from .filters import ChildFilter
import datetime


@login_required
def child_list(request):
    child_filter = ChildFilter(request.GET, queryset=Child.objects.all())
    return render(request, 'child/child/list.html', {'child_filter': child_filter})


@login_required
def child_detail(request, pk):
    child = get_object_or_404(Child, pk=pk)
    disabilities = []
    if child.has_no_disability:
        disabilities.append('No disability')
    if child.has_physical_impairment:
        disabilities.append('Physical impairment')
    if child.has_sensory_impairment:
        disabilities.append('Sensory impairment')
    if child.has_learning_disability:
        disabilities.append('Learning disability')
    if child.has_mental_health_condition:
        disabilities.append('Mental health condition')
    if child.has_any_other_disability:
        disabilities.append('Other disability')

    return render(request, 'child/child/detail.html',
        {
            'child': child,
            'disabilities': ', '.join(disabilities),
        }
    )


@login_required
def create_child(request):
    client_id = request.GET.get('client')
    client = get_object_or_404(Client, pk=client_id)
    initial = {'client': client_id}
    new_child = None
    if request.method == 'POST':
        child_form = ChildForm(request.POST)
        if child_form.is_valid():
            new_child = child_form.save()
            return redirect(new_child.get_absolute_url())
    else:
        child_form = ChildForm(initial=initial)
    return render(request, 'child/child/edit.html', {'new_child': new_child, 'child_form': child_form, 'client': client})


@login_required
def edit_child(request, pk):
    child = get_object_or_404(Child, pk=pk)
    if request.method == 'POST':
        child_form = ChildForm(request.POST, instance=child)
        if child_form.is_valid():
            child = child_form.save()
            return redirect(child.get_absolute_url())
    else:
        child_form = ChildForm(instance=child)
    return render(request, 'child/child/edit.html', {'child_form': child_form, 'child': child})
