from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.handleLogout, name='handleLogout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('editUser/', views.editUser, name='editUser'),
    path('manageExpense/', views.manageExpense, name='manageExpense'),
    path('addExpense/', views.addExpense, name='addExpense'),
    path('editExpense/', views.editExpense, name='editExpense'),
    path('addBudget/', views.addBudget, name='addBudget'),
    path('addCategory/', views.addCategory, name='addCategory'),
    path('addCurrency/', views.addCurrency, name='addCurrency'),
    path('scheduleExpense/', views.scheduleExpense, name='scheduleExpense'),
    path('editScheduleExpense/', views.editScheduleExpense, name='editScheduleExpense'),
    path('restoreData/', views.restoreData, name="restoreData"),
    path('backupData/', views.backupData, name="backupData"),
    path('setting/', views.setting, name='setting'),
]
