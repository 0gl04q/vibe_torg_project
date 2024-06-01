from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from apps.orders.models import Order
from apps.orders.forms import OrderForm
from apps.service.tg_api import send_message


class OrderListView(ListView):
    queryset = Order.objects.select_related('buyer')
    template_name = 'list_order.html'
    context_object_name = 'orders'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Заказы'
        return context


def update_order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    old_status = order.status
    old_price = order.price

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()

            if old_status == Order.Status.PENDING or order.price != old_price:
                send_message(order.buyer.tg_id,
                             text=f'Проверьте заказы, произошло обновление заказа {str(order.id)[:8]}...')

            return render(request, 'detail_order.html', {'order': order})
    else:
        form = OrderForm(instance=order)
    return render(request, 'update_form_order.html', {'order': order, 'form': form})


def detail_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'detail_order.html', {'order': order})


def cancel_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.status = Order.Status.CANCELLED
    order.save()

    return render(request, 'detail_order.html', {'order': order})
