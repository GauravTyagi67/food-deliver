from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View
from .models import MenuItem,Category,OrderModel
from django.core.mail import send_mail
import json

# Create your views here.
class Index(View):
    def get(self,request,*args,**Kwargs):
        return render(request,"customer/index.html")

class About(View):
    def get(self,request,*args,**kwargs):
        return render(request,"customer/about.html")

class Order(View):
    def get(self,request,*args,**kwargs):
        #get every item from each category
        appetizers=MenuItem.objects.filter(category__name__contains='Appetizer')
        dessert=MenuItem.objects.filter(category__name__contains='Dessert')
        drinks=MenuItem.objects.filter(category__name__contains='Drink')

        #pass into context
        context={
            'appetizers':appetizers,
            'dessert':dessert,
            'drinks':drinks
        }

        #render the templates
        return render(request,"customer/order.html",context)

    def post(self, request, *args, **kwargs):
        name=request.POST.get('name')
        email=request.POST.get('email')
        street=request.POST.get('street')
        city=request.POST.get('city')
        state=request.POST.get('state')
        pincode=request.POST.get('pincode')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            state=state,
            pincode=pincode
        )
        order.items.add(*item_ids)

        #Send Email Validations
        body=('Thankyou for your orders successfully!Your foods is being made and will be delivered soon.\n'
            f'Your total:{price}\n'
            'Thankyou again for your orders'
        )

        send_mail(
            'Thankyou for your orders successfully',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )

        context = {
            'items': order_items['items'],
            'price': price
        }

        return redirect('order-confirmation',pk=order.pk)
        #return render(request, 'customer/order_confirmation.html', context)

class OrderConfirmation(View):
    def get(self,request,pk,*args,**kwargs):
        order=OrderModel.objects.get(pk=pk)

        context={
            'pk':order.pk,
            'items':order.items,
            'price':order.price,
        }

        return render(request, 'customer/order_confirmation.html', context)

    def post(self,request,pk,*args,**kwargs):
        data=json.loads(request.body)
        if data['isPaid']:
            order=OrderModel.objects.get(pk=pk)
            order.is_paid=True
            order.save()

        return redirect('payment-confirmation')

class OrderPayConfirmation(View):
    def get(self,request,*args,**kwargs):
        return render(request,"customer/order_pay_confirmation.html")