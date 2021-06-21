from django.shortcuts import redirect, render
from django.core.serializers import serialize
from django.http import HttpResponse
from django.contrib.auth import authenticate,logout,login as auth_login
from django.contrib import messages
from .models import category,transaction_info,money_info,schedule_tr
from django.contrib.auth.models import User
from django.utils import timezone
import json,getpass,datetime


def backupData(request):
    filepath='C:/Users/'+getpass.getuser()+'/Downloads/backup.json'
    querydata =  transaction_info.objects.filter(user_id=request.user.id)
    data = serialize("json",querydata,fields=("user_id","amount","note","category_id","added_on","time"))
    data = str(json.loads(data))
    data = data.replace("'", '"')
    with open(filepath ,'w') as f:
        f.write((data))
    messages.error(request,'Backup Completed')
    return redirect('/expense/setting/')

def restoreData(request):
    
    filepath='C:/Users/'+getpass.getuser()+'/Downloads/backup.json'
    with open(filepath ,'r') as f:
        json_data = f.read()
    json_data = json.loads(json_data)
    user_id=request.user
    checkdata = transaction_info.objects.filter(user_id=request.user.id)
    counter=0
    flag=0
    msg=0
    for i,j in zip(json_data,checkdata):
        print(j.added_on)
        print(i['fields']['added_on'])
        data_time=str(j.time)[:8]
        json_time=str(i['fields']['time'])[:8]
        
        if(j.added_on==i['fields']['added_on'] or data_time==json_time):  
            counter+=1
            print('abc')
        else:
            msg=1
            cat_id= category.objects.get(category_id=i['fields']['category_id'])
            expense = transaction_info(user_id=user_id,amount=i['fields']['amount'],note=i['fields']['note'],category_id=cat_id,added_on=i['fields']['added_on'],time=i['fields']['time'],)
            expense.save()
        if(counter>1 and flag==0):
            messages.error(request,'Some Data Already Exist')
            flag=1
    if(msg==1):
        messages.error(request,'Data Restored')
    return redirect('/expense/setting/')
    
def login(request):
    
    if request.method=="POST":
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = authenticate(username=username,password=password)

        if user is not None:
            auth_login(request, user)
           
            return redirect('/expense/dashboard/')
        else:
            messages.error(request,'Please Enter Correct Credentials')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
      
    
def register(request):
    if request.method=="POST":
        username = request.POST.get('username','')
        fname = request.POST.get('fname','')
        lname = request.POST.get('lname','')
        email = request.POST.get('email','')
        password = request.POST.get('password','')
    
        check_if_user_exists = User.objects.filter(username=username,password=password).exists()
        if check_if_user_exists:
            messages.error(request,'User Already Exist')
        else:
            myuser = User.objects.create_user(username,email,password)
            myuser.first_name =  fname
            myuser.last_name =  lname
            myuser.save()
            return redirect('/expense/login/')
    else :
        return render(request, 'register.html')

def handleLogout(request):
    logout(request)
    return redirect('/expense/login/')
    

def dashboard(request):
    last_week_labels = []
    last_week_data = []
    monthly_labels = []
    monthly_data = []
    yearly_labels = []
    yearly_data = []
    dict_week ={}
    dict_month={}
    dict_year={}
    data = transaction_info.objects.order_by('added_on','time').reverse()
    todays_date=datetime.date.today().day
    curr_month=datetime.date.today().month
    curr_year=datetime.date.today().year

    for i in range(todays_date,todays_date-7,-1):
        dict_week[i]=0
    
    for i in range(12):
        dict_month[i+1]=0

    for i in range(curr_year,curr_year-5,-1):
        dict_year[i]=0

    
    for i in data:        
        data_date = i.added_on.day
        data_month = i.added_on.month
        data_year = i.added_on.year

        # for week
        for j in range (todays_date,todays_date-7,-1):
            if (data_date == j and data_month==curr_month):
                dict_week[j]=i.amount
        
        # for month
        for k in range(12):
            if (data_month==k+1 and data_year==curr_year):
                dict_month[k+1]=dict_month[k+1]+i.amount
        
        # for year
        for l in range(curr_year,curr_year-5,-1):
            if (data_year==l):
                dict_year[l]=dict_year[l]+i.amount

    #for week
    # converted dict into list
    temp_week = []
    dictdata_week = []
    for key, val in dict_week.items():
        temp_week = [key,val]
        dictdata_week.append(temp_week)
    # store data into list
    for i in dictdata_week:
        last_week_labels.append(i[0])
        last_week_data.append(i[1])

    last_week_data.reverse()
    last_week_labels.reverse()
    # for month
    # converted dict into list
    temp_month = []
    dictdata_month = []
    for key, val in dict_month.items():
        temp_month = [key,val]
        dictdata_month.append(temp_month)
        
    # store data into list
    for i in dictdata_month:
        monthly_labels.append(i[0])
        monthly_data.append(i[1])

    # for year
    # converted dict into list
    temp_year = []
    dictdata_year = []
    for key, val in dict_year.items():
        temp_year = [key,val]
        dictdata_year.append(temp_year)
        
    # store data into list
    for i in dictdata_year:
        yearly_labels.append(i[0])
        yearly_data.append(i[1])

    yearly_labels.reverse()
    yearly_data.reverse()

    data = money_info.objects.filter(user_id=request.user.id)
    for i in data:
        budget = str(i.budget)
        currency = str(i.currency)
    checkdata = transaction_info.objects.filter(user_id=request.user.id)
    if (len(checkdata))==0:
        no_of_expenses = 0
        tr_data=''
        total_expense=0
        rem_budget = budget
        for i in data:
            currency = str(i.currency)
        messages.error(request,'Please add some expense first')
    else:
        tr_data = transaction_info.objects.order_by('added_on','time').reverse()
        no_of_expenses=len(tr_data)
        total_expense = 0
        for i in tr_data:
            total_expense=total_expense+i.amount
        rem_budget = int(budget) - int(total_expense)
        graph= {'last_week_labels':last_week_labels,'last_week_data':last_week_data,'monthly_labels':monthly_labels,'monthly_data':monthly_data,'yearly_labels':yearly_labels,'yearly_data':yearly_data}
    param = {'graph':graph,'budget':budget,'expenses': tr_data,'no_of_expenses':no_of_expenses,'total_expense':total_expense,'rem_budget':rem_budget,'currency':currency}
    return render(request, 'dashboard.html',param)

def manageExpense(request):
    filter = request.GET.get('filter')
    data = money_info.objects.filter(user_id=request.user.id)
    checkdata = transaction_info.objects.filter(user_id=request.user.id)
    categories = category.objects.all()
    for i in data:
        budget = str(i.budget)
        currency = str(i.currency)
    if (len(checkdata))==0:
        no_of_expenses = 0
        tr_data=''
        total_expense=0
        rem_budget = budget
        for i in data:
            currency = str(i.currency)
        messages.error(request,'Please add some expense first')
    else:
        if(filter == 'date'):
            datafilter =' By date'
            date = timezone.now().date()
            tr_data = transaction_info.objects.filter(added_on= date)
            no_of_expenses=len(tr_data)
            total_expense =0
            for i in tr_data:
                total_expense=total_expense+i.amount
            rem_budget = int(budget) - int(total_expense)
        elif(filter == 'month'):
            datafilter =' By month'
            month = timezone.now().month
            tr_data = transaction_info.objects.filter(added_on__month__gte= month)
            no_of_expenses=len(tr_data)
            total_expense =0
            for i in tr_data:
                total_expense=total_expense+i.amount
            rem_budget = int(budget) - int(total_expense)
        elif(filter == 'category'):
            datafilter =' By category'
            if request.method=="POST":
                selectedcategory = request.POST.get('selectedcategory','')
                print(selectedcategory)
                cat_id=category.objects.get(name=selectedcategory)
                tr_data = transaction_info.objects.filter(category_id=cat_id.category_id)
                if (len(tr_data))==0:
                    no_of_expenses = 0
                    total_expense=0
                    rem_budget = budget
                    messages.error(request,'Expense not found')
                else:
                    print(tr_data)
                    no_of_expenses=len(tr_data)
                    total_expense =0
                    for i in tr_data:
                        total_expense=total_expense+i.amount
                    rem_budget = int(budget) - int(total_expense)
            else:
                return redirect('/expense/manageExpense/')
        elif(filter == 'expense'):
            datafilter =' By Expense'
            date = timezone.now().date()
            tr_data = transaction_info.objects.order_by('amount').reverse()
            no_of_expenses=len(tr_data)
            total_expense =0
            for i in tr_data:
                total_expense=total_expense+i.amount
            rem_budget = int(budget) - int(total_expense)
        elif(filter == 'datarange'):
            from datetime import datetime
            if request.method=="POST":
                start_date = request.POST.get('start_date','')
                end_date = request.POST.get('end_date','')
                st_date=datetime.strptime(start_date,'%Y-%m-%d' ).strftime("%d-%b-%Y")
                en_date=datetime.strptime(end_date,'%Y-%m-%d' ).strftime("%d-%b-%Y")
                
                datafilter =' '+st_date+ ' to '+en_date
                tr_data = transaction_info.objects.filter(added_on__range=[start_date,end_date])
                if (len(tr_data))==0:
                    no_of_expenses = 0
                    total_expense=0
                    rem_budget = budget
                    messages.error(request,'Expense not found')
                else:
                    no_of_expenses=len(tr_data)
                    total_expense =0
                    for i in tr_data:
                        total_expense=total_expense+i.amount
                    rem_budget = int(budget) - int(total_expense)
            else:
                return redirect('/expense/manageExpense/')
        else:
            datafilter =' Default'
            tr_data = transaction_info.objects.order_by('added_on','time').reverse()

            json_tr_data=serialize("json",tr_data,fields=("user_id","amount","note","category_id","added_on","time"))
            no_of_expenses=len(tr_data)
            total_expense = 0
            for i in tr_data:
                total_expense=total_expense+i.amount
            rem_budget = int(budget) - int(total_expense)

    param = {'datafilter':datafilter,'json_tr_data':json_tr_data,'categories':categories,'expenses': tr_data,'no_of_expenses':no_of_expenses,'total_expense':total_expense,'rem_budget':rem_budget,'currency':currency}
    return render(request, 'manage_expense.html',param)
    
def editExpense(request):
    id = request.GET.get('id')
    type = request.GET.get('type')
    userid = request.user.id
    if id and type:
        if type=='edit':
            data_tr = transaction_info.objects.filter(tr_id=id)
            data_money = money_info.objects.filter(user_id=request.user.id)
            categories = category.objects.all()
            for i in data_tr:
                date = str(i.added_on)
            for i in data_money:
                currency = str(i.currency)
            param = {'data':data_tr,'categories':categories,'date':date,'currency':currency}
            return render(request, 'edit_expense.html',param)
        if type =='save':
            if request.method=="POST":
                update = transaction_info.objects.get(tr_id=id)
                expenses = request.POST.get('expense','')
                cat = request.POST.get('category','')
                note = request.POST.get('note','')
                added_on = request.POST.get('added_on','')
                cat_id= category.objects.get(name=cat)
                update.amount = expenses
                update.category_id = cat_id 
                update.note = note
                update.added_on = added_on
                update.save()
                return redirect('/expense/manageExpense/')
            else:
                return HttpResponse('ERROR')
        if type =='clearall':
            transaction_info.objects.filter(user_id=userid).delete()
            return redirect('/expense/setting/')
        if type =='clear':
            transaction_info.objects.filter(tr_id=id).delete()
            return redirect('/expense/manageExpense/')
        else:
            return redirect('/expense/manageExpense/')
    else:
        return redirect('/expense/manageExpense/')

def addExpense(request):
    categories = category.objects.all()
    data = money_info.objects.filter(user_id=request.user.id)
    for i in data:
        currency = str(i.currency)
    param = {'categories':categories,'currency':currency}
    if request.method=="POST":
        expenses = request.POST.get('expense','')
        print(expenses)
        if (int(expenses) > 0):
            user_id=request.user
            cat = request.POST.get('category','')
            note = request.POST.get('note','')
            added_on = request.POST.get('added_on','')
            cat_id= category.objects.get(name=cat)
            expense = transaction_info(user_id=user_id,amount=expenses,note=note,category_id=cat_id,added_on=added_on)
            expense.save()
            return redirect('/expense/manageExpense/')
        else:
            messages.error(request,'Expense should not be 0')
            return render(request, 'add_expense.html',param)
    else:
        return render(request, 'add_expense.html',param)

def scheduleExpense(request):
    categories = category.objects.all()
    data = money_info.objects.filter(user_id=request.user.id)
    for i in data:
        currency = str(i.currency)
    checkdata = schedule_tr.objects.filter(user_id=request.user.id)
    if (len(checkdata))==0:
        tr_data=''
        messages.error(request,'Please Schedule expense first')
    else:
        tr_data = schedule_tr.objects.order_by('added_on','time').reverse()
    param = {'expenses':tr_data,'categories':categories,'currency':currency}
    type = request.GET.get('type')
    if type :
        if type=='add_schedule':
            if request.method=="POST":
                expenses = request.POST.get('expense','')
                user_id=request.user
                cat = request.POST.get('category','')
                note = request.POST.get('note','')
                added_on = request.POST.get('added_on','')
                repeat = request.POST.get('repeat','')
                cat_id= category.objects.get(name=cat)
                data = schedule_tr(user_id=user_id,amount=expenses,note=note,category_id=cat_id,added_on=added_on,repeat=repeat)
                data.save()
                return redirect('/expense/scheduleExpense/')
            else:
                return render(request, 'schedule_expense.html',param)
            
        else:
            return render(request, 'schedule_expense.html',param)
    else:
        return render(request, 'schedule_expense.html',param)

def editScheduleExpense(request):
    id = request.GET.get('id')
    type = request.GET.get('type')
    if id and type:
        if type=='edit':
            data_sc_tr = schedule_tr.objects.filter(sc_id= id)
            data_money = money_info.objects.filter(user_id=request.user.id)
            for i in data_sc_tr:
                date = str(i.added_on)
            for i in data_money:
                currency = str(i.currency)
            param = {'data':data_sc_tr,'date':date,'currency':currency}
            return render(request, 'edit_schedule_expense.html',param)
        if type=='save':
            if request.method=="POST":
                update = schedule_tr.objects.get(sc_id=id)
                expenses = request.POST.get('expense','')
                cat = request.POST.get('category','')
                note = request.POST.get('note','')
                added_on = request.POST.get('added_on','')
                repeat = request.POST.get('repeat','')
                cat_id= category.objects.get(name=cat)
                update.amount = expenses
                update.category_id = cat_id 
                update.note = note
                update.added_on = added_on
                update.repeat = repeat
                update.save()
                return redirect('/expense/scheduleExpense/')
            else:
                return HttpResponse('ERROR')
        if type =='clear':
            schedule_tr.objects.filter(sc_id=id).delete()
            return redirect('/expense/scheduleExpense/')

        else:
            return redirect('/expense/scheduleExpense/')
    else:
        return redirect('/expense/scheduleExpense/')
                
def addBudget(request):
    
    if request.method=="POST":
        budget = request.POST.get('budget','')
        user_id=request.user
        check_if_user_exists = User.objects.filter(username=user_id).exists()
        if check_if_user_exists:
            data = money_info.objects.get(user_id=user_id)
            data.budget = budget
            print('User Already Exist')
        else:
            data = money_info(user_id=user_id,budget=budget)
        data.save()
        return redirect('/expense/dashboard/')
    else:    
        return redirect('/expense/manageExpense/')

def addCategory(request):
    if request.method=="POST":
        name = request.POST.get('category','')
        user_id=request.user
        iconname= 'fa fa-ellipsis-h'
        data = category(user_id=user_id,name=name,iconname=iconname)
        data.save()
        return redirect('/expense/setting/')
    else:
        return redirect('/expense/setting/')

def setting(request):
    user_id=request.user.id
    data = money_info.objects.filter(user_id=user_id)
    data_user = User.objects.filter(id=user_id)
    for i in data:
        budget = str(i.budget)
        currency = str(i.currency)
    param = {'data':data_user,'budget':budget,'currency':currency,'user_id':user_id}
    return render(request, 'setting.html',param)

def addCurrency(request):
    if request.method=="POST":
        user_id=request.user
        updatedata = money_info.objects.get(user_id=user_id)
        currency = request.POST.get('selectedcurrency','')
        updatedata.currency = currency
        updatedata.save()
        return redirect('/expense/setting/')
    else:
        return redirect('/expense/setting/')

def editUser(request):
    id = request.GET.get('id')
    type = request.GET.get('type')
    if id and type:
        if type=='edit':
            data = User.objects.filter(id= id)
            param = {'data':data}
            return render(request, 'edit_user.html',param)
        if type =='save':
            print("Save")
            if request.method=="POST":
                update = User.objects.get(id=id)
                username = request.POST.get('username','')
                fname = request.POST.get('fname','')
                lname = request.POST.get('lname','')
                email = request.POST.get('email','')
                update.username = username
                update.first_name = fname 
                update.last_name = lname
                update.email = email
                update.save()
                return redirect('/expense/setting/')
            else:
                return HttpResponse('ERROR')

