from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.views import generic
from django.http import HttpResponseRedirect 
from .models import Product, Basket, Favorite
from .forms import BasketForm

# Create your views here.

class Products(generic.ListView):
    queryset = Product.objects.all()
    template_name = "products/products.html"

def view_product(request, slug):

    queryset = Product.objects.all()
    product = get_object_or_404(queryset, slug=slug)
    basket = product.product.all()
    
    if request.method == 'POST':
        basket_form = BasketForm(data=request.POST)
        if basket_form.is_valid():
            order = basket_form.save(commit=False)
            order.user = request.user
            order.product = product
            order.amount = product.price
            order.save()
            messages.success(request, 'Product added to basket')
        else:
            messages.error(request, 'Error adding product to basket')

    basket_form = BasketForm()
    return render(
        request,
        'products/view_product.html',
        {'product': product,
        'basket': basket,
        'basket_from': basket_form,},
        )

def home(request):
    return render(request, 'products/index.html',)

def basket(request):

    items = Basket.objects.filter(user=request.user)
    total = sum(item.amount*item.quantity for item in items)

    return render(request, 'products/basket.html', {'items': items, 'total': total})


def remove_item(request, basket_id):

    basket_item = get_object_or_404(Basket, id=basket_id, user=request.user)
    basket_item.delete()
    messages.add_message(request, messages.SUCCESS, 'Item removed!')

    return HttpResponseRedirect(reverse('basket'))

def after_payment(request):

    return render(
        request,
        'products/after_payment.html',
    )

def add_to_favorites(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)

    if created:
        messages.success(request, f'{product.title} has been added to your favorites.')
    else:
        messages.info(request, f'{product.title} is already in your favorites.')
    
    return redirect('products')

def favorites(request):

    favorites = Favorite.objects.filter(user=request.user)

    return render(
        request,
        'products/favorites.html',
        {'favorites': favorites,},
        )

def remove_favorite(request, favorite_id):

    favorite = get_object_or_404(Favorite, id=favorite_id, user=request.user)
    favorite.delete()
    messages.add_message(request, messages.SUCCESS, 'Favorite removed!')

    return HttpResponseRedirect(reverse('favorites'))