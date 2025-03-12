from django .urls import path
from django.contrib.auth import views as auth_views
from .import views

urlpatterns =[
    path('' , views.home, name='home'),
    path('index' , views.index, name='index'),
    path('about' , views.about, name='about'),
    path('contact' , views.contact, name='contact'),
    path('category/<str:pk>', views.category, name='category'),
    path('product/<str:pk>', views.product_detail, name='product_detail'),
    path('register', views.register,name='register'),
    path('login', views.login_user,name='login'),
    path('profile', views.profile,name='profile'),
    path('address', views.address, name='address'),
    path('update/<str:pk>', views.update_record, name='update'),
    path('change-password/', views.change_password, name='change_password'), 
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),  # Ensure the trailing slash
    path('cart/', views.show_cart, name='show_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increment_quantity/<int:cart_item_id>/', views.increment_quantity, name='increment_quantity'),
    path('decrement_quantity/<int:cart_item_id>/', views.decrement_quantity, name='decrement_quantity'),
    path('checkout',views.checkout, name='checkout'),
    path('order-success/<int:payment_id>/', views.order_success, name='order_success'),
    path('order-progress/', views.order_progress, name='order_progress'),
   
    path('logout',views.logout_user, name='logout'),
    path('service',views.service, name='service')


]