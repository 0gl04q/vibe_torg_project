from django.urls import path

from apps.orders import views

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order-list'),
    path('cancel_order/<uuid:order_id>/', views.cancel_order, name='cancel_order'),
    path('detail_order/<uuid:order_id>/', views.detail_order, name='detail_order'),
    path("update_order_details/<uuid:order_id>/", views.update_order_detail, name="update_order_details"),
]
