from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone


# 订单模型
class Order(models.Model):
    # 订单状态枚举（可选：待支付/已支付/已取消/已完成）
    ORDER_STATUS = (
        ('pending', '待支付'),
        ('paid', '已支付'),
        ('cancelled', '已取消'),
        ('completed', '已完成'),
    )

    # 订单核心字段
    order_num = models.CharField('订单编号', max_length=32, unique=True)  # 唯一订单号
    product_name = models.CharField('商品名称', max_length=128)  # 商品名称
    price = models.DecimalField('商品价格', max_digits=10, decimal_places=2)  # 价格
    status = models.CharField('订单状态', max_length=16, choices=ORDER_STATUS, default='pending')
    create_time = models.DateTimeField('创建时间', default=timezone.now)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'order'  # 数据库表名
        verbose_name = '订单'
        verbose_name_plural = '订单'

    def __str__(self):
        return self.order_num  # 后台显示订单编号