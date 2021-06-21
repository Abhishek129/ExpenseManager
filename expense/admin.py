from django.contrib import admin
from .models import category,transaction_info,money_info,schedule_tr

admin.site.register(category)
admin.site.register(transaction_info)
admin.site.register(money_info)
admin.site.register(schedule_tr)
