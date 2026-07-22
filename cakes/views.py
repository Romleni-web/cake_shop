from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Cake, GalleryImage, Review
from cart.forms import CartAddProductForm
from .forms import ReviewForm, ContactForm
from django.contrib import messages
from django.core.mail import send_mail

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Cake.objects.filter(available=True)

    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'cakes/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Cake, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    reviews = product.reviews.filter(active=True)
    new_review = None

    if request.method == 'POST':
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.cake = product
            new_review.save()
            messages.success(request, 'Your review has been added.')
            return redirect(product.get_absolute_url())
    else:
        review_form = ReviewForm()

    return render(request, 'cakes/product/detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
        'reviews': reviews,
        'review_form': review_form
    })

def gallery(request):
    images = GalleryImage.objects.all()
    return render(request, 'cakes/gallery.html', {'images': images})

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send Email
            cd = form.cleaned_data
            subject = f"New Contact Message: {cd['subject']}"
            message = f"From: {cd['name']} <{cd['email']}>\n\nMessage:\n{cd['message']}"
            send_mail(subject, message, cd['email'], ['admin@melanincakehouse.com'])

            messages.success(request, 'Thank you for your message. We will get back to you soon.')
            return redirect('cakes:contact')
    else:
        form = ContactForm()
    return render(request, 'cakes/contact.html', {'form': form})
