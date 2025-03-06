from django.shortcuts import render

from django.http import Http404
from django.shortcuts import render
from .models import Owner

def owner_detail(request, owner_id):
    try:
        owner = Owner.objects.get(pk=owner_id)  # Поиск владельца по первичному ключу (id)
    except Owner.DoesNotExist:
        raise Http404("Owner does not exist")  # Вызываем ошибку 404, если объект не найден
    return render(request, 'owner.html', {'owner': owner})  # Передаем объект owner в шаблон
