from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from .models import Order
import random
import string

# Create your views here.

def index(request):
    return HttpResponse("Hello setaone！这是我的第一个Django页面～")


def html_index(request):
    return render(request, 'index.html', {'title': '订单首页'})



# 生成随机订单编号（辅助函数）
def generate_order_num():
    # 格式：时间戳+6位随机字符串
    timestamp = str(int(timezone.now().timestamp()))
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"ORD{timestamp}{random_str}"

# ====================== API接口 ======================
# 1. 创建订单API（POST请求）
class OrderCreateView(View):
    def post(self, request):
        # 获取前端传参（示例：product_name/price/status）
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        status = request.POST.get('status', 'pending')  # 默认待支付

        # 参数校验
        if not product_name or not price:
            return JsonResponse({
                'code': 400,
                'msg': '商品名称和价格不能为空',
                'data': None
            })

        # 创建订单
        try:
            order = Order.objects.create(
                order_num=generate_order_num(),
                product_name=product_name,
                price=price,
                status=status
            )
            return JsonResponse({
                'code': 200,
                'msg': '订单创建成功',
                'data': {
                    'order_id': order.id,
                    'order_num': order.order_num,
                    'product_name': order.product_name
                }
            })
        except Exception as e:
            return JsonResponse({
                'code': 500,
                'msg': f'创建失败：{str(e)}',
                'data': None
            })

# 2. 订单列表API（GET请求）
class OrderListView(View):
    def get(self, request):
        # 可选：按状态筛选（如?status=paid）
        status = request.GET.get('status')
        orders = Order.objects.all().order_by('-create_time')  # 按创建时间倒序

        # 状态筛选
        if status:
            orders = orders.filter(status=status)

        # 构造返回数据
        order_list = []
        for order in orders:
            order_list.append({
                'order_id': order.id,
                'order_num': order.order_num,
                'product_name': order.product_name,
                'price': str(order.price),  # Decimal转字符串避免JSON序列化问题
                'status': order.status,
                'status_text': dict(Order.ORDER_STATUS)[order.status],  # 状态中文
                'create_time': order.create_time.strftime('%Y-%m-%d %H:%M:%S')
            })

        return JsonResponse({
            'code': 200,
            'msg': '查询成功',
            'data': {
                'total': len(order_list),
                'orders': order_list
            }
        })

# 3. 订单详情查看API（GET请求，传订单ID）
class OrderDetailView(View):
    def get(self, request, order_id):
        # 查找订单（不存在则返回404）
        order = get_object_or_404(Order, id=order_id)

        # 构造详情数据
        detail = {
            'order_id': order.id,
            'order_num': order.order_num,
            'product_name': order.product_name,
            'price': str(order.price),
            'status': order.status,
            'status_text': dict(Order.ORDER_STATUS)[order.status],
            'create_time': order.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'update_time': order.update_time.strftime('%Y-%m-%d %H:%M:%S')
        }

        return JsonResponse({
            'code': 200,
            'msg': '查询成功',
            'data': detail
        })

# 4. 订单删除API（DELETE请求，传订单ID）
class OrderDeleteView(View):
    def delete(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        try:
            order.delete()
            return JsonResponse({
                'code': 200,
                'msg': '订单删除成功',
                'data': None
            })
        except Exception as e:
            return JsonResponse({
                'code': 500,
                'msg': f'删除失败：{str(e)}',
                'data': None
            })