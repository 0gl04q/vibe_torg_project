from django.http import JsonResponse

from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, CreateAPIView

from apps.orders.models import Order, Buyer
from apps.ordersAPI.serializers import OrderSerializer, BuyerSerializer


class BuyerCreateAPIView(CreateAPIView):
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer


class OrderListAPIView(ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        tg_id = self.kwargs['tg_id']
        return Order.objects.filter(buyer_id=tg_id).exclude(status__in=(Order.Status.CANCELLED, Order.Status.COMPLETED))


class OrderDetailAPIView(RetrieveUpdateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        tg_id = self.kwargs['tg_id']

        try:
            return Order.objects.filter(buyer_id=tg_id)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=404)

    def get_object(self):
        pk = self.kwargs['pk']

        try:
            return Order.objects.get(pk__icontains=pk)
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=404)


class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
