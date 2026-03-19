from django.contrib import messages
from django.shortcuts import redirect, render

from userdashboard.models import signup

from .models import admin_user, product


def _get_logged_in_admin(request):
    admin_id = request.session.get('admin_id')
    admin_email = request.session.get('admin_email')

    if not admin_id or not admin_email:
        return None

    try:
        return admin_user.objects.get(id=admin_id, email=admin_email)
    except admin_user.DoesNotExist:
        request.session.pop('admin_id', None)
        request.session.pop('admin_email', None)
        request.session.pop('admin_name', None)
        return None


def admin_login(request):
    if _get_logged_in_admin(request) is not None:
        return redirect('admin_dashboard')
    return render(request, 'admin_login.html')


def check_user(request):
    if request.method == 'GET':
        return redirect('admin_login')

    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '').strip()

    if not email or not password:
        messages.error(request, 'Email and password are required.')
        return redirect('admin_login')

    try:
        admin_usr = admin_user.objects.get(email=email, password=password)
    except admin_user.DoesNotExist:
        messages.error(request, 'Invalid email or password.')
        return redirect('admin_login')

    request.session['admin_id'] = admin_usr.id
    request.session['admin_email'] = admin_usr.email
    request.session['admin_name'] = admin_usr.name
    return redirect('admin_dashboard')


def admin_dash(request):
    current_admin = _get_logged_in_admin(request)
    if current_admin is None:
        messages.error(request, 'Please login first.')
        return redirect('admin_login')

    users = signup.objects.order_by('-id')
    products = product.objects.order_by('-id')
    context = {
        'admin_name': current_admin.name,
        'total_users': users.count(),
        'total_products': products.count(),
        'recent_users': users[:5],
        'recent_products': products[:5],
    }
    return render(request, 'admin_dashboard.html', context)


def add_product(request):
    current_admin = _get_logged_in_admin(request)
    if current_admin is None:
        messages.error(request, 'Please login first.')
        return redirect('admin_login')

    if request.method == 'POST':
        pname = request.POST.get('pname', '')
        pprice = request.POST.get('pprice', '')
        pdescription = request.POST.get('pdescription', '')
        ptype = request.POST.get('ptype', '')
        pphoto = request.FILES.get('pphoto')

        if not pname or not pprice or not pdescription or not ptype or not pphoto:
            messages.error(request, 'All product fields are required.')
            return redirect('add_product')

        product.objects.create(
            pname=pname,
            pprice=pprice,
            pdescription=pdescription,
            ptype=ptype,
            pphoto=pphoto,
        )
        request.session['product_success_message'] = f'[{pname}] product added successfully'
        return redirect('add_product')

    products = product.objects.order_by('-id')
    success_message = request.session.pop('product_success_message', None)
    context = {
        'admin_name': current_admin.name,
        'products': products,
        'success': success_message,
    }
    return render(request, 'add_product.html', context)


def manage_product(request):
    current_admin = _get_logged_in_admin(request)
    if current_admin is None:
        messages.error(request, 'Please login first.')
        return redirect('admin_login')

    products = product.objects.order_by('-id')
    context = {
        'admin_name': current_admin.name,
        'products': products,
    }
    return render(request, 'manage_product.html', context)


def admin_logout(request):
    request.session.pop('admin_id', None)
    request.session.pop('admin_email', None)
    request.session.pop('admin_name', None)
    messages.success(request, 'Admin logged out successfully.')
    return redirect('admin_login')


def admin_profile(request):
    current_admin = _get_logged_in_admin(request)
    if current_admin is None:
        messages.error(request, 'Please login first.')
        return redirect('admin_login')

    return render(request, 'admin_profile.html', {'admin_data': current_admin})


def admin_orders(request):
    current_admin = _get_logged_in_admin(request)
    if current_admin is None:
        messages.error(request, 'Please login first.')
        return redirect('admin_login')

    return render(request, 'admin_orders.html', {'admin_data': current_admin})


def admin_users(request):
    current_admin = _get_logged_in_admin(request)
    if current_admin is None:
        messages.error(request, 'Please login first.')
        return redirect('admin_login')

    return render(request, 'admin_users.html', {'admin_data': current_admin})

