from .views import *
from django.urls import path

urlpatterns = [
    path('freeOrdersList/<int:week>/', FreeListOfOrders.as_view(), name='freeOrdersList'),
    path('ordersList/', GetListOfOrders.as_view(), name='ordersList'),
    path('deleteOrder/<int:order_id>/', DeleteOrder.as_view(), name='deleteOrder'),
    path('addOrder/', AddOrder.as_view(), name='addOrder'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

    path('getAllOrders/', GetAllOrders.as_view(), name='getAllOrders'),
]