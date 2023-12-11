import paypalrestsdk
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CustomUserCreationForm, CategoryForm, ProductForm, ReviewForm, OrderHistoryForm
from .models import Category, Product, Review, Cart, OrderHistory
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from paypal.standard.forms import PayPalPaymentsForm

# Create your views here.
def is_admin(user):
    return user.is_superuser

def index(request):
    return render(request, 'main/index.html')

def registro(request):
		form = CustomUserCreationForm()
		if request.method == 'POST':
			form = CustomUserCreationForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Felicidades cuenta creada ' + user)

				return redirect('login')
			

		context = {'form':form}
		return render(request, 'registration/registro.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

@user_passes_test(is_admin)
def create_category(request):
   
    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect('main:category_list')
        elif 'save' in request.POST:
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('main:category_list')

    else:
        form = CategoryForm()
    
    return render(request, 'main/create_category.html', {'form': form})

@user_passes_test(is_admin)
def edit_category(request, category_id):
   
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        if 'delete' in request.POST:
            category.delete()
            return redirect('main:category_list')
        elif 'cancel' in request.POST:
            return redirect('main:category_list')
        elif 'save' in request.POST:
            form = CategoryForm(request.POST)
            if form.is_valid():
                #form.update()
                form.save()
                return redirect('main:category_list')
    else:
      
        form = CategoryForm(instance=category)
    
    return render(request, 'main/edit_category.html', {'form': form, 'category': category})

@user_passes_test(is_admin)
def delete_category(request, category_id):
  
    category = get_object_or_404(Category, pk=category_id)
    
    if request.method == 'POST':
        category.delete()
        return redirect('main:category_list') 
    return render(request, 'main/delete_category.html', {'category': category})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'main/category_list.html', {'categories': categories})

@user_passes_test(is_admin)
def create_product(request):
    if request.method == 'POST':
        if 'cancel' in request.POST:
            return redirect('main:product_list')
        elif 'save' in request.POST:
            form = ProductForm(request.POST, request.FILES )
            if form.is_valid():
                form.save()
                return redirect('main:product_list')
    else:
        form = ProductForm()
    categories = Category.objects.all()  
    return render(request, 'main/create_product.html', {'form': form, 'categories': categories})

# Vista para editar un producto existente
@user_passes_test(is_admin)
def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        if 'delete' in request.POST:
            # Lógica para eliminar el producto
            product.delete()
            return redirect('main:product_list')
        elif 'cancel' in request.POST:
            # Redirige a la lista de productos en caso de cancelación
            return redirect('main:product_list')
        elif 'save' in request.POST:
            # Lógica para guardar el producto
            form = ProductForm(request.POST,request.FILES, instance=product)
            if form.is_valid():
                form.save()
                return redirect('main:product_list')
    else:
        form = ProductForm(instance=product)
        
    categories = Category.objects.all() 
    return render(request, 'main/edit_product.html', {'form': form, 'product': product, 'categories': categories})

# Vista para eliminar un producto
@user_passes_test(is_admin)
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        product.delete()
        return redirect('main:product_list')  
    
    return render(request, 'main/delete_product.html', {'product': product})

# Vista para ver la lista de productos
def product_list(request):
    categories = Category.objects.all()

    selected_category_id = None
    selected_category_name = "Todos" 

    if request.method == 'GET':
        selected_category_id = request.GET.get('category')
        
        if selected_category_id:
            selected_category = Category.objects.get(id=selected_category_id)
            selected_category_name = selected_category.name

    if selected_category_id:
        products = Product.objects.filter(category_id=selected_category_id)
    else:
        products = Product.objects.all()

    return render(request, 'main/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category_id': selected_category_id,
        'selected_category_name': selected_category_name  
    })
    

# Vista para ver los detalles de los productos 
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product=product)
    return render(request, 'main/product_detail.html', {
        'product': product,
        'reviews': reviews,
    })

# Vista para agregar una review
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            rating = form.cleaned_data['rating']
          
            review = Review.objects.create(product=product, user=request.user, comment=comment, rating=rating)
            review.save()
            messages.info(request, 'Felicitaciones')
			           
            return redirect('main:product_detail', product_id=product_id)
    else:
        form = ReviewForm()

    return render(request, 'main/add_review.html', {'product': product, 'form': form})

#carrito de compras
def carrito_de_compras(request):
    try:
        cart = Cart.objects.get(user=request.user)
        products = cart.products.all()
    except Cart.DoesNotExist:
        products = []
        cart = None

    return render(request, 'main/carrito_de_compras.html', {'products': products, 'cart': cart})

#añadir producto al carrito
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)
        cart.save()

    if product in cart.products.all():
        messages.info(request, 'Producto ya está en el carrito')
    else:
        cart.products.add(product)
        cart.total += product.price
        cart.save()
        messages.info(request, 'Producto agregado al carrito')

    return redirect('main:carrito_de_compras')

#eliminar producto del carrito
def remove_from_cart(request, id):
    product = get_object_or_404(Product, id=id)
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = None

    if cart:
        if product in cart.products.all():
            cart.products.remove(product)
            cart.total -= product.price
            cart.save()
            messages.info(request, 'Producto removido del carrito')
        else:
            messages.info(request, 'Producto no está en el carrito')
    else:
        messages.info(request, 'No hay carrito para este usuario')

    return redirect('main:carrito_de_compras')

#busqueda personalizada de productos
def search(request, ):
    query = request.GET.get('q', '')
    productos = Product.objects.filter(name__icontains=query)
    if not productos.exists():
        messages.info(request, 'Producto no existe')
        return redirect('/')

    return render(request, 'main/search_results.html', {'productos': productos})
    #funciona solo que en el form de product detail redirecciona a add_riview y sale error


#API de Paypal
paypalrestsdk.configure({
    "mode": "sandbox",  # Change to "live" for production
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET,
})

def create_payment(request):
    cart = Cart.objects.get(user=request.user)
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal",
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('main:execute_payment')),
            "cancel_url": request.build_absolute_uri(reverse('main:payment_failed')),
        },
        "transactions": [
            {
                "amount": {
                    "total": str(cart.total),  # Total amount in USD
                    "currency": "USD",
                },
                "description": "Payment for Product/Service",
            }
        ],
    })

    if payment.create():
        for link in payment.links:
            if link.method == "REDIRECT":
                return redirect(link.href)
       # return redirect(payment.links[1].href)  # Redirect to PayPal for payment
    else:
        return render(request, 'main/payment_failed.html', {'error_message': payment.error})
    
def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return render(request, 'main/payment_success.html')
    else:
        return render(request, 'main/payment_failed.html')
    

def payment_failed(request):
    return render(request, 'main/payment_failed.html')

def ordenarPedido(request):
    if request.method == 'POST':
        form = OrderHistoryForm(request.POST)
        if form.is_valid():
            order_history = form.save(commit=False)
            order_history.user = request.user
            order_history.save()
            return redirect('main:order_history')  
    else:
        form = OrderHistoryForm()

    order_histories = OrderHistory.objects.filter(user=request.user)
    
    return render(request, 'main/order_history.html', {'form': form, 'order_histories': order_histories})


def Ejemplo(request):
    return render(request, 'main/ejemplo.html')