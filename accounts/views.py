from ast import Not
from django.shortcuts import render, redirect
from .models import Customer, Order, Product
from .forms import OrderForm, UserRegistraionForm
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import group_required
from django.contrib.auth.models import Group

# Create your views here.

def register_page(request):

    if request.user.is_authenticated:
        return redirect('/')
    
    else:
        form = UserRegistraionForm()

        if request.method == 'POST':
            form = UserRegistraionForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                my_group = Group.objects.get(name='customer') 
                user.groups.add(my_group)
                Customer.objects.create(user=user,)
                messages.success(request, "Profile created succcesfully !")
                return redirect('login')

        context = {'form': form}

        return render(request, 'accounts/register.html', context)

def login_page(request):

    if request.user.is_authenticated:
        return redirect('/')
    
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Credentials is incorrect !')
        
        return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout_page(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@group_required('customer')
def user_page(request):

    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    total_pending = orders.filter(status='Pending').count()
    total_delivered = orders.filter(status='Delivered').count()
    total_out_for_delivery = orders.filter(status='Out for delivery').count()

    context = {'orders': orders, 'total_orders': total_orders,'total_pending': total_pending, 'total_delivered': total_delivered, 'total_out_for_delivery': total_out_for_delivery}

    return render(request, 'accounts/user.html', context=context)

@login_required(login_url='login')
@group_required('admin')
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all().order_by('-date_created')

    total_orders = orders.count()
    total_pending = Order.objects.filter(status='Pending').count()
    total_delivered = Order.objects.filter(status='Delivered').count()
    total_out_for_delivery = Order.objects.filter(status='Out for delivery').count()

    context = {'customers': customers, 'orders': orders, 'total_orders': total_orders,'total_pending': total_pending, 'total_delivered': total_delivered, 'total_out_for_delivery': total_out_for_delivery}

    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@group_required('admin')
def products(request):

    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products': products})

@login_required(login_url='login')
@group_required('admin', 'customer')
def customer(request, pk):

    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()  # parent relationship reverse in case of foregin key and many to many

    order_filter = OrderFilter(request.GET, queryset=orders)

    orders = order_filter.qs

    total_orders = orders.count()

    context = {'orders': orders, 'customer': customer, 'total_orders': total_orders, 'order_filter': order_filter}

    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
@group_required('admin')
def create_order(request):

    form = OrderForm()

    if request.method == 'POST':

        form = OrderForm(request.POST)

        if form.is_valid():
            form.save() 
            return redirect('/')

    context = {'form': form}

    return render(request, 'accounts/create_order.html', context) 

@login_required(login_url='login')
@group_required('admin')
def update_order(request, pk):

    order = Order.objects.get(id=pk)

    form = OrderForm(instance=order) # Not like normal, we have to write instance

    if request.method == 'POST':

        form = OrderForm(request.POST, instance=order)
        
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form, 'pk': pk}

    return render(request, 'accounts/update_order.html', context) 

@login_required(login_url='login')
@group_required('admin')
def delete_order(request, pk):

    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        flag = request.POST
        if flag['flag']=='Yes':
            order.delete()
        return redirect('/')

    context = {'pk': pk, 'order': order}

    return render(request, 'accounts/delete_order.html', context) 