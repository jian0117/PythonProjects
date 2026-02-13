# -*- coding : utf-8 -*-
from django.db import models

class Expense(models.Model):
    EXPENSE_CHOICES = [
        ('FOOD', '吃喝'),
        ('OTHER', '其他'),
        ('RENT', '租房'),
    ]

    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    expense_type = models.CharField(max_length=5, choices=EXPENSE_CHOICES)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Assuming you are using Django's built-in User model
