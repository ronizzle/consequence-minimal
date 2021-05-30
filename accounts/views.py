from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
# Create your views here.


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    context = {
        'orders': orders,
        'customers': customers,
        'total_customers': total_customers,
    }
    return render(request, 'accounts/dashboard.html', context)


def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    return render(request, 'accounts/customer.html', {'customer': customer})


def create_customer(request):

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    form = CustomerForm()

    context = {'form': form}
    return render(request, 'accounts/customer_form.html', context)


def update_customer(request, pk):

    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')

    form = CustomerForm(instance=customer)

    context = {'form': form}
    return render(request, 'accounts/customer_form.html', context)


def delete_customer(request, pk):

    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('/')

    context = {'customer': customer}
    return render(request, 'accounts/delete.html', context)

