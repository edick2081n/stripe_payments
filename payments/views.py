from django.shortcuts import render, redirect
from payments.models import Item, Order, OrderItems
from stripe.api_resources.checkout.session import Session
from django.http import JsonResponse




def show_item(request, id):
    a = Item.objects.get(id=id)
    return render(request, "item.html", {"item":a})

def buy_item(request, id):
    positions = OrderItems.objects.filter(order__id=id)
    items = []
    for position in positions:
        items.append({"price": position.item.stripe_id, "quantity":position.count})
    b = Session.create(
        api_key='sk_test_51Myxy7FlSvL4cyBCbS13rfgttcMk4u9xoFj7A1CvbIFdnwavqdRF84NgCFmaIjxnIxTgn9Kf6T5VqJbzL1xKZHtB00Wc9XsJHg',
        success_url="http://localhost:8000/success/", line_items=items, mode='subscription')

    return JsonResponse({"id":b.id})

def add_to_order(request, item_id):
    if request.user.is_authenticated:
        order = Order.objects.filter(is_paid=False, customer=request.user).first()
        if order is None:
            order = Order.objects.create(customer=request.user)
        item = Item.objects.get(id=item_id)
        order_item = OrderItems.objects.filter(order=order, item=item).first()
        if order_item is None:
            order.items.add(item)
        else:
            order_item.count+=1
            order_item.save()
        print(order.items.all())
       # total = OrderItems.objects.filter
        #return redirect(f"/item/{item.id}/")
        return render(request, "order.html", {"order": order})


def success(request):
    return render(request, "success.html")
