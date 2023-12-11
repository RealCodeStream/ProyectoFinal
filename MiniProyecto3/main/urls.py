from django.urls import path
from . import views


app_name = "main"

urlpatterns =[
    path('', views.index, name='home'),
    path('logout/',views.logout, name='logout'),
    path('registro/',views.registro, name='registro'),
    path('Categorias/',views.category_list, name='category_list'),
    path('categories/create/', views.create_category, name='create_category'),
    path('categories/<int:category_id>/edit/', views.edit_category, name='edit_category'),
    path('categories/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    
    # Rutas para productos
    path('products/', views.product_list, name='product_list'),
    path('products/create/', views.create_product, name='create_product'),
    path('products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    
    # Rutas para review
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/add_review/', views.add_review, name='add_review'),
    
     path('carrito-de-compras/', views.carrito_de_compras, name='carrito_de_compras'),
     path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
     path('remove_from_cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
     path('search/', views.search, name='search'),
    path('create_payment/', views.create_payment, name='create_payment'),
    path('execute_payment/', views.execute_payment, name='execute_payment'),
    path('payment_failed/', views.payment_failed, name='payment_failed'),
    path('order_history/', views.ordenarPedido, name='order_history'),
    path('Ejemplo/', views.Ejemplo, name='Ejemplo'),
]