from django.urls import path

from apps.ordersAPI import views

urlpatterns = [
    path("buyer/create/", views.BuyerCreateAPIView.as_view(), name="buyer_create"),
    path("order/<int:tg_id>/<str:pk>/", views.OrderDetailAPIView.as_view(), name="order_detail"),
    path("order/<int:tg_id>/", views.OrderListAPIView.as_view(), name="order_list"),
    path("order/create/", views.OrderCreateAPIView.as_view(), name="order_create")
]
