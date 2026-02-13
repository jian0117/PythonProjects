from django.urls import path
from . import views
from .views import OrderCreateView, OrderListView, OrderDetailView, OrderDeleteView

urlpatterns = [
    # 访问http://127.0.0.1:8000/setaone/ 触发index函数
    path('', views.index, name='index'),

    # 访问http://127.0.0.1:8000/setaone/html/ 触发html_index函数
    path('html/', views.html_index, name='html_index'),

    # 创建订单：POST /api/order/create/
    path('api/order/create/', OrderCreateView.as_view(), name='order_create'),
    # 订单列表：GET /api/order/list/
    path('api/order/list/', OrderListView.as_view(), name='order_list'),
    # 订单详情：GET /api/order/detail/1/（1为订单ID）
    path('api/order/detail/<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),
    # 订单删除：DELETE /api/order/delete/1/（1为订单ID）
    path('api/order/delete/<int:order_id>/', OrderDeleteView.as_view(), name='order_delete'),

]
