from .models import transaction_info,schedule_tr

def scheduleExpense():
    data_sc=schedule_tr.objects.all()
    for i in data_sc:
        user_id = i.user_id
        sc_id=i.sc_id
        amount = i.amount
        note = i.note
        cat_id = i.category_id
        added_on =i.added_on
        insert = transaction_info(user_id=user_id,amount=amount,note=note,category_id=cat_id,added_on=added_on)
        insert.save()
        schedule_tr.objects.filter(sc_id=sc_id).delete()
