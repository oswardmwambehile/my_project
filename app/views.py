from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Count
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from.models import Product,Customer,Order,Payment
from .form import CustomerForm, ChangePasswordForm
from.models import Customer,Cart
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse

from django.http import HttpResponseRedirect
from django.db.models import Sum


from .form import ChangePasswordForm

import re

from django.core.paginator import Paginator


def index(request):
    if request.user.is_authenticated:
      # Get all the products
       product_list = Product.objects.all()
    
       # Paginate products (12 products per page)
       paginator = Paginator(product_list, 12)  # Show 12 products per page
       page_number = request.GET.get('page')  # Get current page number from query params
       products = paginator.get_page(page_number)  # Get products for that page
    
       # Render the template with paginated products
       return render(request, 'home.html', {'products': products})
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')

def home(request):
   
      return  render (request,'index.html')
    

def category(request,pk):
    if request.user.is_authenticated:
      product= Product.objects.filter(category=pk)
      title= Product.objects.filter(category=pk).values('title')
      return render(request, 'category.html',{'product':product,'title':title})
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')


def product_detail(request, pk):
    if request.user.is_authenticated:
       product=Product.objects.get(id=pk)
       return render(request, 'product_detail.html', {'product':product})
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')


def about(request):
    if request.user.is_authenticated:
        return render(request,'about.html')
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')

def contact(request):
    if request.user.is_authenticated:
       return render(request,'contact.html')
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        
        # Validation for username, email, and password
        if len(username) < 3:
            messages.error(request, 'Username must be at least 3 characters long.')
            return redirect('register')
        
        if not re.match(r"^[a-zA-Z0-9_]*$", username):
            messages.error(request, 'Username can only contain letters, numbers, and underscores.')
            return redirect('register')

        if len(password) < 5:
            messages.error(request, 'Password must be at least 5 characters long.')
            return redirect('register')
        
        if not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
            messages.error(request, 'Password must contain both letters and numbers.')
            return redirect('register')
        
        if password != password1:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
        
        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return redirect('register')
        
        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('register')
        
        # Create the user if all validations pass
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'You have successfully registered.')
        return redirect('login')
    
    return render(request, 'register.html')


def login_user(request):

    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'login successfully')
            return redirect('profile')
        else:
            messages.error(request,'Wrong username or password combination')
            return redirect('login')
    else:
        return  render(request,'login.html')
    




def profile(request):
    if request.user.is_authenticated:
    # Instantiate the form with POST data if it exists, else None
        form = CustomerForm(request.POST or None)

        # Check if the form is being submitted via POST
        if request.method == 'POST':
            # Check if the form is valid
            if form.is_valid():
                # Create a new instance of the Customer model without committing it to the DB yet
                customer = form.save(commit=False)
                
                # Assign the current logged-in user to the 'user' field
                customer.user = request.user
                
                # Save the customer record to the database
                customer.save()
                
                # Show a success message
                messages.success(request, 'Record added successfully')
                
                # Redirect to the profile page after saving
                return redirect('address')  # Adjust redirect URL if needed
            else:
                # Print the form errors to the console for debugging
                print(form.errors)  # Helps to debug form validation issues

        # Render the form again if it's not a POST request or if validation failed
        return render(request, 'profile.html', {'form': form})
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')
 



def address(request):
    if request.user.is_authenticated:
        add=Customer.objects.filter(user=request.user)
        return render(request, 'address.html',{'add':add})
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')
 



def update_record(request,pk):
    if request.user.is_authenticated:
        curent=Customer.objects.get(id=pk)
        form = CustomerForm(request.POST or None,instance=curent)
        if form.is_valid():
            form.save()
            messages.success(request, 'record updated successfully')
            return redirect('address')
        return render(request, 'update.html', {'form': form})
    else:
        messages.error(request, 'You must login to the system')
        return redirect('login')






def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ChangePasswordForm(user=request.user, data=request.POST)
            
            if form.is_valid():
                # Save the new password
                form.save()
                update_session_auth_hash(request, form.user)  # Important to keep the user logged in
                messages.success(request, 'Your password has been updated successfully!')
                return redirect('profile')  # Redirect to the profile page or another appropriate page
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = ChangePasswordForm(user=request.user)
        
        return render(request, 'change_password.html', {'form': form})
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')



def custom_password_reset(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                user = User.objects.filter(email=email).first()
                if user:
                    # Send the reset email
                    token = default_token_generator.make_token(user)
                    reset_url = f"{request.build_absolute_uri('/password_reset_confirm/')}?token={token}"
                    send_mail(
                        'Password Reset',
                        f'Click here to reset your password: {reset_url}',
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                    )
                    messages.success(request, "Password reset link has been sent to your email.")
                else:
                    messages.error(request, "No user found with that email address.")
                return HttpResponseRedirect('/password_reset_done/')
        else:
            form = PasswordResetForm()
        return render(request, 'password_reset.html', {'form': form})
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')

def add_to_cart(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Get the product_id from POST data
            product_id = request.POST.get('product_id')

            # Validate the product_id and handle errors
            try:
                product = Product.objects.get(id=product_id)

                # Check if the product is already in the user's cart
                cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

                if created:
                    # If the cart item was created, it means the product was not in the cart
                    cart_item.quantity = 1  # Set quantity to 1 for new products
                    cart_item.save()
                    messages.success(request, f'{product.title} has been added to your cart.')
                else:
                    # If the product already exists in the cart, increase the quantity by 1
                    cart_item.quantity += 1
                    cart_item.save()
                    messages.info(request, f'{product.title} quantity has been updated in your cart.')

            except Product.DoesNotExist:
                messages.error(request, 'Product not found.')

        # Redirect to the cart page
        return redirect('show_cart')  # Ensure 'show_cart' is the correct name of the cart page view
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')

from django.db.models import Sum

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart_items = Cart.objects.filter(user=user)

        # Calculate the total price of items in the cart
        total_cart_price = sum(item.total_cost for item in cart_items)

        # Calculate the total quantity of items in the cart
        total_quantity = cart_items.aggregate(total_count=Sum('quantity'))['total_count'] or 0

        # Pass the cart items, total price, and total quantity to the template
        return render(request, 'addcart.html', {
            'cart_items': cart_items,
            'total_cart_price': total_cart_price,
            'total_quantity': total_quantity,  # Pass the total quantity to the template
        })
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')



def remove_from_cart(request, cart_item_id):
    if request.user.is_authenticated:
        try:
            # Get the cart item based on the provided cart_item_id and the logged-in user
            cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
            
            # Remove the cart item
            cart_item.delete()

            messages.success(request, f'{cart_item.product.title} has been removed from your cart.')

        except Cart.DoesNotExist:
            messages.error(request, 'The product was not found in your cart.')

        # Redirect back to the cart page after removing the product
        return redirect('show_cart')  # Ensure 'show_cart' is the name of the cart page view
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')
 


from django.http import JsonResponse


# Increment the quantity of a product in the cart
def increment_quantity(request, cart_item_id):
    if request.user.is_authenticated:
        try:
            cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
            cart_item.quantity += 1
            cart_item.save()

            # Calculate the total number of items in the cart
            total_quantity = sum(item.quantity for item in Cart.objects.filter(user=request.user))

            # Return the updated quantity and total cost as well as the total cart quantity
            return JsonResponse({
                'success': True,
                'quantity': cart_item.quantity,
                'total_cost': cart_item.total_cost,
                'total_quantity': total_quantity
            })

        except Cart.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Cart item not found.'})
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')

# Decrement the quantity of a product in the cart
def decrement_quantity(request, cart_item_id):
    if request.user.is_authenticated:
        try:
            cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
            if cart_item.quantity > 1:  # Prevent quantity from going below 1
                cart_item.quantity -= 1
                cart_item.save()

                # Calculate the total number of items in the cart
                total_quantity = sum(item.quantity for item in Cart.objects.filter(user=request.user))

                # Return the updated quantity and total cost as well as the total cart quantity
                return JsonResponse({
                    'success': True,
                    'quantity': cart_item.quantity,
                    'total_cost': cart_item.total_cost,
                    'total_quantity': total_quantity
                })
            else:
                return JsonResponse({'success': False, 'message': 'Quantity cannot be less than 1.'})

        except Cart.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Cart item not found.'})
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')




def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        address = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)

        total_cart_price = sum(item.total_cost for item in cart_items)

        if request.method == 'POST':
            # Capture the selected shipping address and payment method
            shipping_address_id = request.POST.get('shipping_address')
            payment_method = request.POST.get('payment_method', 'cash_on_delivery')  # Default to cash on delivery if not selected

            # Validate if the shipping address was selected
            if not shipping_address_id:
                messages.error(request, 'Please select a shipping address.')
                return redirect('checkout')  # Redirect back to checkout page

            # Get the selected shipping address
            shipping_address = Customer.objects.get(id=shipping_address_id, user=user)

            # Create the payment record (e.g., cash_on_delivery or online_payment)
            payment = Payment.objects.create(
                user=user,
                amount=total_cart_price,
                payment_method=payment_method,  # Save the selected payment method
                paid=False  # Not paid yet
            )

            # Create orders for each item in the cart
            for item in cart_items:
                Order.objects.create(
                    user=user,
                    customer=shipping_address,
                    product=item.product,
                    quantity=item.quantity,
                    payment=payment,
                    status='pending'  # You can adjust this as per your workflow
                )

            # Clear the cart after creating the order
            cart_items.delete()

            # Redirect to order success page, passing the payment object
            messages.success(request, 'Your order has been placed successfully.')
            return redirect('order_success', payment_id=payment.id)  # Pass the payment_id to the order_success page
    

        return render(request, 'checkout.html', {
            'address': address,
            'cart_items': cart_items,
            'total_cart_price': total_cart_price,
        })
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')



def order_success(request, payment_id):
    if request.user.is_authenticated:
        # Retrieve the payment object based on the payment_id
        payment = get_object_or_404(Payment, id=payment_id)

        # Render the order success template, passing the payment object
        return render(request, 'order_success.html', {'payment': payment})
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')
     

def order_progress(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
        for order in orders:
            print(order.status)  # Check the status value of each order
        return render(request, 'order.html', {'orders': orders})
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')

    


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'you have log out............')
        return redirect('home')
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')

    



def service(request):
    if request.user.is_authenticated:
        return render(request, 'service.html')
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')



