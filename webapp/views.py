from django.core.paginator import Paginator
from django.shortcuts import render

from webapp.models import Car


def index(request):
    cars = Car.objects.all()[:3]
    main_car = Car.objects.filter(is_main=True).first()
    context = {"cars": cars,
               "main_car": main_car}
    return render(request, 'webapp/index.html', context=context)


def about(request):
    return render(request, 'webapp/about.html')


def cars(request):
    cars = Car.objects.all()
    paginator = Paginator(cars, 3)
    page_number = request.GET.get('page')
    page_objs = paginator.get_page(page_number)

    context = {"page_objs": page_objs}
    return render(request, 'webapp/cars.html', context=context)


def services(request):
    return render(request, 'webapp/services.html')


def contact(request):
    return render(request, 'webapp/contact.html')
