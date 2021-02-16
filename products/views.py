from django.shortcuts import render, redirect, get_object_or_404
from .models import product
from django.contrib.auth.decorators import login_required
from .models import product
from django.utils import timezone
# Create your views here.
def home(request):
    prod_obj = product.objects
    return render(request , 'products/home.html', {'products':prod_obj});

@login_required(login_url = '/accounts/signup')
def create(request):
    if request.method=='POST':
        if request.POST['title'] and request.POST['url'] and request.FILES['image'] and request.POST['body'] and request.FILES['icon']:
            product_obj = product()
            product_obj.title = request.POST['title'];

            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product_obj.url = request.POST['url'];
            else:
                product_obj.url = 'http://'+request.POST['url'];

            product_obj.body = request.POST['body'];
            product_obj.icon = request.FILES['icon'];
            product_obj.image = request.FILES['image'];
            product_obj.pub_date = timezone.datetime.now();
            product_obj.hunter = request.user;
            product_obj.save();
            return redirect('/products/'+str(product_obj.id));
        else:
            return render(request , 'products/create.html', {'error': "Fill required data"});
    else:
        return render(request , 'products/create.html');

def detail(request, product_id):
    detail_product  = get_object_or_404(product, pk = product_id);
    return render(request, 'products/detail.html', {'product':detail_product});

@login_required(login_url = '/accounts/signup')
def upvote(request, product_id):
    if request.method=='POST':
        product_obj = get_object_or_404(product, pk = product_id);
        product_obj.votes_total +=1;
        product_obj.save()
        return redirect('/products/'+str(product_obj.id));
