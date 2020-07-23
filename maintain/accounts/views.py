# from django.contrib.auth.forms import CreateUserForm
# Create your views here.
from django.contrib import messages
from django.contrib.auth.models import Group,User
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect
from .filters import *
from .forms import CreateUserForm,OrderForm
from .decorators import *

@unauthenticated_user
def RegisterPage(request):
    form=CreateUserForm()
    if request.method=="POST":
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get("username")
            group=Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(user=user)
            messages.success(request,"Account was created for "+username)
            return redirect("login")
    context={'form':form}
    return render(request,"accounts/Register.html",context)

@unauthenticated_user
# @allowed_users(allowed_roles=['customer'])
def LoginPage(request):

    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,"Username or password is incorrect")
    context={}
    return render(request,"accounts/Login.html",context)

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(redirect_field_name='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders=request.user.customer.order_set.all()
    total_orders=orders.count()
    delivered=orders.filter(status='Delivered').count()
    pending=orders.filter(status='Pending').count()
    context={'orders':orders,'total':total_orders,'delivered':delivered,'pending':pending}
    return render(request,"accounts/user.html",context)


@login_required(redirect_field_name='login')
@admin_only
def home(request):
    customer=Customer.objects.all()
    order=Order.objects.all()
    n_orders=len(order)
    n_pending=Order.objects.filter(status='Pending')
    pending=len(n_pending)
    n_delivered = Order.objects.filter(status='Delivered')
    delivered=len(n_delivered)
    return render(request,"accounts/dashboard.html",{'customers':customer,'order':order,'total':n_orders,'pending':pending,'delivered':delivered})


@login_required(redirect_field_name='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products=Product.objects.all()
    return render(request,"accounts/products.html",{'products':products})

@login_required(redirect_field_name='login')
@allowed_users(allowed_roles=['admin'])
def customers(request,pk_test):
    customer=Customer.objects.get(id=pk_test)
    orders=customer.order_set.all()
    n=customer.order_set.all().count()
    myFilter=OrderFilter(request.GET,queryset=orders)
    orders=myFilter.qs
    return render(request,"accounts/customer.html",{'filter':myFilter,'customer':customer,
                  'orders':orders,'total':n})
#
@login_required(redirect_field_name='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'))
    customer=Customer.objects.get(id=pk)
    formset=OrderFormSet(instance=customer)
    if request.method=="POST":
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect("/")
    return render(request,'accounts/order_form.html',{'formset':formset})

@login_required(redirect_field_name='login')
@allowed_users(allowed_roles=['admin'])
def update(request,pk):
    order=Order.objects.get(id=pk)
    form=OrderForm(instance=order)
    if request.method=="POST":
        form=OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect("/")
    context={'form':form}
    return render(request,"accounts/order_form.html",context)

@login_required(redirect_field_name='login')
@allowed_users(allowed_roles=['admin'])
def delete(request,pk):
    order = Order.objects.get(id=pk)
    if request.method=="POST":
        order.delete()
        return redirect("/")
    return render(request,"accounts/delete.html",{'item':order})


def setting(request):
    return render(request,"accounts/setting.html")