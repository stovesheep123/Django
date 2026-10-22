from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Customer

@login_required
def customer_search(request):
    query = request.GET.get('q', '')
    if query:
        customers = Customer.objects.filter(
            Q(customer_code__icontains=query) |
            Q(customer_name__icontains=query) |
            Q(customer_telno__icontains=query) |
            Q(customer_address__icontains=query)
        )
    else:
        customers = Customer.objects.all()
        
    context = {
        'customers': customers,
        'query': query,
    }
    return render(request, 'psys/customer_search.html', context)

@login_required
def customer_list(request):
    customer_list_all = Customer.objects.all().order_by('customer_code')
    paginator = Paginator(customer_list_all, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'psys/customer_list.html', context)

@login_required
def customer_create(request):
    error_message = None
    if request.method == 'POST':
        code = request.POST.get('customer_code')
        name = request.POST.get('customer_name')
        telno = request.POST.get('customer_telno')
        postalcode = request.POST.get('customer_postalcode')
        address = request.POST.get('customer_address')
        discount_rate = request.POST.get('discount_rate', 0)
        
        if Customer.objects.filter(pk=code).exists():
            error_message = f"ERROR: 得意先コード '{code}' はすでに存在します。"
        else:
            Customer.objects.create(
                customer_code=code,
                customer_name=name,
                customer_telno=telno,
                customer_postalcode=postalcode,
                customer_address=address,
                discount_rate=discount_rate,
                delete_flag=0
            )
            return redirect('customer_list')
            
    return render(request, 'psys/customer_form.html', {'error_message': error_message})

@login_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.customer_name = request.POST.get('customer_name')
        customer.customer_telno = request.POST.get('customer_telno')
        customer.customer_postalcode = request.POST.get('customer_postalcode')
        customer.customer_address = request.POST.get('customer_address')
        customer.discount_rate = request.POST.get('discount_rate', 0)
        customer.save()
        return redirect('customer_list')
        
    return render(request, 'psys/customer_edit.html', {'customer': customer})

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
        
    return render(request, 'psys/customer_confirm_delete.html', {'customer': customer})