from django.shortcuts import render
from django.http import HttpResponse
from .models import Product,Contact,Order,OrderUpdate
from math import ceil
import json
# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)
# Create your views here.
def index(request):
    #return HttpResponse("You are in Shop")
    #return  render(request,'shop/index.html')
    #products = Product.objects.all()
    #print(products)
    #n = len(products)
    #nSlides = n//4 + ceil((n/4)-(n//4))
    allProds = []
    catprods = Product.objects.values('category')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        print('prod in each iter:',prod)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    #params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    #return render(request, 'shop/index.html', params)
    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)

def about(request):
    return  render(request,'shop/about.html')
def contact(request):
    if request.method == "POST":
        print(request)
        name = request.POST.get('name','')
        #print(name)
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        #print(name,email,phone,desc)
        contact = Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
    return  render(request,'shop/contact.html')

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(order_id=orderId, email=email)
            print(order[0].items_json)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                print(update)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    #response = json.dumps(updates, default=str)
                    response = json.dumps({"updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')

def productView(request,myid):
    #fetch product using id
    product = Product.objects.filter(id=myid)
    #print(product)
    return  render(request,'shop/prodview.html',{'product': product[0]})

def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        address = request.POST.get('address1','') + '' + request.POST.get('address2','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        phone = request.POST.get('phone','')
        zip_code = request.POST.get('zip_code','')
        order = Order(items_json=items_json,name=name,email=email,phone=phone,city=city,state=state,address=address,zip_code=zip_code)
        order.save()
        update = OrderUpdate(order_id= order.order_id, update_desc = "Your order has been placed")
        update.save()
        thank = True
        print(thank)
        id = order.order_id
        print(id)
        return render(request,'shop/checkout.html',{'thank': thank, 'id': id})
    return  render(request,'shop/checkout.html')

def searchMatch(query,item):
    if query in item.product_name.lower() or query in item.product_discreption.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    print(query)
    allProds = []
    catprods = Product.objects.values('category')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query,item)]
        print('prod in each iter:',prod)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod)!= 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds,'msg':""}
    if len(allProds)== 0 or len(query)<3:
        params = {'msg':"Enter relevant search query"}
    return render(request, 'shop/search.html', params)
