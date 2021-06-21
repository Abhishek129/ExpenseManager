from os import makedirs
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    iconname = models.CharField(max_length=100,default='')
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class transaction_info(models.Model):
    tr_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.IntegerField()
    note = models.CharField(max_length=500)
    category_id = models.ForeignKey(category,on_delete=models.CASCADE)
    added_on = models.DateField()
    time = models.TimeField(auto_now=True)

    def __str__(self):
        return str(self.category_id) +'....'+ str(self.user_id)
        
class schedule_tr(models.Model):
    sc_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.IntegerField()
    note = models.CharField(max_length=500)
    category_id = models.ForeignKey(category,on_delete=models.CASCADE)
    added_on = models.DateField()
    time = models.TimeField(auto_now_add=True)
    repeat = models.CharField(max_length=20)

    def __str__(self):
        return str(self.category_id) +'....'+ str(self.user_id)

class money_info(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    currency = models.CharField(max_length=50)
    budget = models.IntegerField()

    def __str__(self):
        return str(self.user_id)

