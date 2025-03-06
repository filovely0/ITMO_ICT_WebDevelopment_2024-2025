from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Owner
from .models import Car
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .forms import OwnerForm
from .forms import CarForm
from django.views import View



def owner_detail(request, owner_id):
    try:
        owner = Owner.objects.get(pk=owner_id)
    except Owner.DoesNotExist:
        raise Http404("Owner does not exist")
    return render(request, 'owner.html', {'owner': owner})

# вывод списка владельцев функционально
def owner_list(request):
    owners = Owner.objects.all()
    return render(request, 'owners/owner_list.html', {'owners': owners})

# вывод списка автомобилей классами

class CarListView(ListView):
    model = Car
    template_name = 'cars/car_list.html'
    context_object_name = 'cars'

# класс вывода авто по айди
class CarDetailView(DetailView):
    model = Car
    template_name = 'cars/car_detail.html'
    context_object_name = 'car'

# класс обновления авто

class CarUpdateView(UpdateView):
    model = Car
    fields = ['license_plate', 'brand', 'model', 'color']
    template_name = 'cars/car_update.html'
    success_url = reverse_lazy('car_list')

# форма ввода владельцев функционально
def owner_create(request):
    if request.method == 'POST':
        form = OwnerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('owner_list')
    else:
        form = OwnerForm()
    return render(request, 'owners/owner_create.html', {'form': form})


# Создание нового автомобиля
class CarCreateView(View):
    def get(self, request):
        form = CarForm()
        return render(request, 'cars/car_form.html', {'form': form})

    def post(self, request):
        form = CarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('car_list')
        return render(request, 'cars/car_form.html', {'form': form})



# Удаление автомобиля
class CarDeleteView(View):
    def get(self, request, car_id):
        car = get_object_or_404(Car, id=car_id)
        return render(request, 'cars/car_confirm_delete.html', {'car': car})

    def post(self, request, car_id):
        car = get_object_or_404(Car, id=car_id)
        car.delete()
        return redirect('car_list')