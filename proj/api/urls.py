from django.conf.urls import url
from django.urls import path

from .views import InventoriesView, OrdersView


# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('inventario/', InventoriesView.as_view()),
    path('orders/', OrdersView.as_view()),
]
