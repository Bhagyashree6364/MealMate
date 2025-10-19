from django.shortcuts import render, redirect
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Restaurant
from .models import Restaurant, MenuItem
from django.shortcuts import render, redirect, get_object_or_404
from .models import Restaurant, MenuItem, Order
from django.contrib.auth.decorators import login_required

@login_required
def place_order(request, rest_id):
    restaurant = get_object_or_404(Restaurant, id=rest_id)
    menu_items = MenuItem.objects.filter(restaurant=restaurant)
    if request.method == 'POST':
        selected = []
        total = 0
        for item in menu_items:
            if str(item.id) in request.POST:
                selected.append(item)
                total += item.price
        address = request.POST.get('delivery_address')
        number = request.POST.get('number')
        # Store in session for payment
        request.session['order_items'] = [item.id for item in selected]
        request.session['order_total'] = float(total)
        request.session['order_rest_id'] = restaurant.id
        request.session['order_address'] = address
        request.session['order_number'] = number
        return redirect('payment', rest_id=restaurant.id)
    else:
        return render(request, 'delivery/place_order.html', {'menu_items': menu_items, 'restaurant': restaurant})
import razorpay
from django.conf import settings

@login_required
def payment(request, rest_id):
    restaurant = get_object_or_404(Restaurant, id=rest_id)
    items_ids = request.session.get('order_items', [])
    total = request.session.get('order_total', 0)
    address = request.session.get('order_address', '')
    number = request.session.get('order_number', '')
    menu_items = MenuItem.objects.filter(id__in=items_ids)
    amount_paise = int(float(total) * 100)

    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    razorpay_order = client.order.create({'amount': amount_paise, 'currency': 'INR', 'payment_capture': 1})

    context = {
        'restaurant': restaurant,
        'items': menu_items,
        'total': total,
        'razorpay_order_id': razorpay_order['id'],
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount_paise,
        'currency': 'INR',
        'callback_url': '/paymenthandler/',
        # Pass address and number for reference (not used by Razorpay, but available for order review)
        'address': address,
        'number': number,
    }
    return render(request, 'delivery/payment.html', context)

@login_required
def paymenthandler(request):
    # ...verify payment logic...
    rest_id = request.session.get('order_rest_id')
    restaurant = get_object_or_404(Restaurant, id=rest_id)
    items_ids = request.session.get('order_items', [])
    total = request.session.get('order_total', 0)
    address = request.session.get('order_address', '')
    number = request.session.get('order_number', '')

    # Save the order to DB with address and number
    order = Order.objects.create(
        user=request.user,
        restaurant=restaurant,
        number=number,
        delivery_address=address,
        total_amount=total,
        # add other fields as needed
        is_paid=True # After successful payment only!
    )
    order.menu_items.set(MenuItem.objects.filter(id__in=items_ids))
    order.save()
    # Clear session/order info
    for key in ['order_items', 'order_total', 'order_rest_id', 'order_address', 'order_number']:
        if key in request.session:
            del request.session[key]
    return render(request, 'delivery/payment_success.html', {'order': order})

def view_cart(request):
    # Temporary cart view placeholder
    return render(request, 'delivery/cart.html')

def signup_view(request):
    if request.method == 'POST':
        # signup logic here, e.g., create user
        pass
    return render(request, 'delivery/signup.html')

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to homepage on successful login
        else:
            return render(request, 'delivery/login.html', {'error': "Invalid credentials"})
    else:
        return render(request, 'delivery/login.html')


from .models import Restaurant

def index(request):
    restaurants = Restaurant.objects.all()
    return render(request, "delivery/index.html", {'restaurants': restaurants})

def restaurant_menu(request, rest_id):
    restaurant = get_object_or_404(Restaurant, id=rest_id)
    menu_items = MenuItem.objects.filter(restaurant=restaurant)
    return render(request, "delivery/menu.html", {
        "restaurant": restaurant,
        "menu": menu_items,
    })
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserProfileForm

@login_required
def profile_view(request):
    profile = get_or_create_userprofile(request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'delivery/profile.html', {'form': form})
from .models import UserProfile

def get_or_create_userprofile(user):
    try:
        return user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
        return profile
