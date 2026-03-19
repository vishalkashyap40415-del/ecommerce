from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import signup
from admindashboard.models import order, product


# Create your views here.
def HOME_Main_Page(request):
    return render(request, 'main.html')


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '').strip()

    if not email or not password:
        messages.error(request, 'Email and password are required')
        return render(request, 'login.html')

    try:
        user = signup.objects.get(email=email, password=password)
        request.session['user_id'] = user.id
        request.session['username'] = user.username
        request.session['email'] = user.email
        return redirect('Dashboard')
    except signup.DoesNotExist:
        messages.error(request, 'Invalid email or password')
        return render(request, 'login.html')


def newuser(request):
    if request.method == 'GET':
        return render(request, 'newuser.html')

    username = request.POST.get('username', '').strip()
    email = request.POST.get('email', '').strip()
    password = request.POST.get('password', '').strip()
    confirm_password = request.POST.get('confirm_password', '').strip()
    mobile_number = request.POST.get('mobile', '').strip()
    profile_image = request.FILES.get('img')
    address = request.POST.get('address', '').strip()

    if not username or not email or not password or not confirm_password or not mobile_number or not profile_image or not address:
        messages.error(request, 'All fields are required')
        return render(request, 'newuser.html')

    if password != confirm_password:
        messages.error(request, 'Password and confirm password must match')
        return render(request, 'newuser.html')

    if signup.objects.filter(email=email).exists():
        messages.error(request, 'Email already exists')
        return render(request, 'newuser.html')

    if signup.objects.filter(username=username).exists():
        messages.error(request, 'Username already exists')
        return render(request, 'newuser.html')

    signup.objects.create(
        username=username,
        email=email,
        password=password,
        mobile_number=mobile_number,
        profile_image=profile_image,
        address=address,
    )
    messages.success(request, 'User created successfully. Please log in.')
    return redirect('login')


def _get_logged_in_user(request):
    user_id = request.session.get('user_id')
    email = request.session.get('email')
    if not user_id or not email:
        return None

    try:
        return signup.objects.get(id=user_id, email=email)
    except signup.DoesNotExist:
        request.session.flush()
        return None


def Dashboard(request):
    user = _get_logged_in_user(request)
    if user is None:
        messages.error(request, 'Please login first')
        return redirect('login')

    products = product.objects.all()
    return render(request, 'Dashboard.html', {'name': user.username, 'email': user.email, 'user_data': user, 'products': products})


def Profile(request):
    user = _get_logged_in_user(request)
    if user is None:
        messages.error(request, 'Please login first')
        return redirect('login')

    return render(request, 'profile.html', {'user_data': user})


def MyOrders(request):
    user = _get_logged_in_user(request)
    if user is None:
        messages.error(request, 'Please login first')
        return redirect('login')

    # Fetch orders for the logged-in user
    user_orders = order.objects.filter(email=user.email)
    return render(request, 'myorders.html', {'user_data': user, 'myorder': user_orders})


def signup_page(request):
    return redirect('newuser')


def logout_view(request):
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


def ChangePassword(request):
    user = _get_logged_in_user(request)
    if user is None:
        messages.error(request, 'Please login first')
        return redirect('login')

    if request.method == 'GET':
        return render(request, 'changepassword.html', {'email': user.email})

    old_password = request.POST.get('old_password', '').strip()
    new_password = request.POST.get('new_password', '').strip()
    confirm_password = request.POST.get('confirm_password', '').strip()

    if not old_password or not new_password or not confirm_password:
        messages.error(request, 'All password fields are required')
        return render(request, 'changepassword.html', {'email': user.email})

    if user.password != old_password:
        messages.error(request, 'Old password is incorrect')
        return render(request, 'changepassword.html', {'email': user.email})

    if new_password != confirm_password:
        messages.error(request, 'New password and confirm password must match')
        return render(request, 'changepassword.html', {'email': user.email})

    user.password = new_password
    user.save()
    request.session.flush()
    messages.success(request, 'Password changed successfully. Please login again.')
    return redirect('login')


def buynow(request):
    if "username" in request.session and "email" in request.session:
        product_id = request.POST.get('pid')
        useremail=request.session['email']
        username=request.session['username']
        pqnty = request.POST.get('pqnty')
        data = get_object_or_404(product, id=product_id)
        total_price = int(data.pprice) * int(pqnty)
        try:
            order.objects.create(user=username, email=useremail,
                                product=data, ptype=data.ptype, pprice=data.pprice,
                                p_photo=data.pphoto, pdescription=data.pdescription,
                                quantity=pqnty, total_price=total_price, pname=data.pname)
        except Exception as e:
            messages.error(request, f'Error placing order: {str(e)}')
            return redirect('products')  # assuming a products page
        return redirect('my_order_list')



def my_order_list(request):
    if "username" in request.session and "email" in request.session:
        useremail=request.session['email']
        data = order.objects.filter(email=useremail)
        return render(request,"myorders.html",{'myorder':data})
    else:
        messages.error(request, 'Please login first')
        return redirect('login.html')



def Products(request):
    user = _get_logged_in_user(request)
    if user is None:
        messages.error(request, 'Please login first')
        return redirect('login')

    from admindashboard.models import product
    products = product.objects.all()
    return render(request, 'Products.html', {'products': products, 'user_data': user})


def product_orders(request):
    user = _get_logged_in_user(request)
    if user is None:
        messages.error(request, 'Please login first')
        return redirect('login')

    product_id = request.GET.get('product_id') or request.POST.get('product_id')
    
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        address = request.POST.get('address')
        name = request.POST.get('name')
        email = request.POST.get('email')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        
        if product_id and quantity and address and name and email and city and pincode:
            prod = product.objects.get(id=product_id)
            total_price = int(prod.pprice) * int(quantity)
            # Save order to database
            order.objects.create(
                user=name, 
                email=email,
                product=prod,
                ptype=prod.ptype,
                pprice=prod.pprice,
                p_photo=prod.pphoto,
                pdescription=prod.pdescription,
                quantity=quantity,
                total_price=total_price,
                pname=prod.pname
            )
            messages.success(request, f'Order placed successfully for {prod.pname}!')
            return redirect('MyOrders')
        else:
            messages.error(request, 'All fields are required')
            data = product.objects.get(id=product_id)
            return render(request, 'product_order.html', {'product': data, 'user_data': user})
    else:
        # GET request - show the order form
        if product_id:
            data = product.objects.get(id=product_id)
            return render(request, 'product_order.html', {'product': data, 'user_data': user})
        else:
            return redirect('Products')


def cancel_order(request, order_id):
    user = _get_logged_in_user(request)
    if user is None:
        messages.error(request, 'Please login first')
        return redirect('login')

    try:
        order_obj = order.objects.get(id=order_id, email=user.email)
        if order_obj.order_shipped_status == 'Pending':
            order_obj.order_shipped_status = 'Cancelled'
            order_obj.save()
            messages.success(request, f'Order for {order_obj.pname} has been cancelled successfully.')
        else:
            messages.error(request, 'This order cannot be cancelled as it is already processed.')
    except order.DoesNotExist:
        messages.error(request, 'Order not found.')

    return redirect('MyOrders')
