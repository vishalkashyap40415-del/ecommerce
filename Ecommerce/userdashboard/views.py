from django.shortcuts import redirect, render
from django.contrib import messages
from .models import signup


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

    return render(request, 'Dashboard.html', {'name': user.username, 'email': user.email, 'user_data': user})


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

    return render(request, 'myorders.html', {'user_data': user})


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
