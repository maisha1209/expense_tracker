"""
URL configuration for expense_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path 
from . import views



#urlpatterns = [
   
 #   path("admin/", admin.site.urls),
 #   path('login/', views.login_view, name='login'),
 #   path('signup/', views.signup_view, name='signup'),
 #   path('', views.login_view, name='dashboard'),  # New dashboard page view
 #   path('create_link_token/', views.create_link_token, name='create_link_token'),
 #   path('get_access_token/', views.get_access_token, name='get-access-token'),
 #   path('auth', views.get_auth, name="get-auth"),
  #  path('transactions/get/', views.get_transactions, name='get-transactions'),
   
    
  
    
#]


app_name = 'expense_tracker'
urlpatterns = [ 
    #path('', views.index, name='index'),
    path('', views.base, name='base'),
    path('index', views.index, name='index'),
    path('budget/<int:budget_id>/', views.budget, name='budget'),
    path('budget/<int:budget_id>/category/<int:category_id>/edit', views.category_edit, name='category-edit'),
    path('budget/<int:budget_id>/category/<int:category_id>/update', views.category_update, name='category-update'),
    path('budget/new', views.budget_new, name='budget-new'),
    path('budget/delete', views.budget_delete, name='budget-delete'),
    path('<int:budget_id>/category/new', views.category_new, name='category-new'),
    path('budget/<int:budget_id>/category/<int:category_id>/delete', views.bca_delete, name='bca-delete'),
    path('budget/<int:budget_id>/bca/new', views.bca_new, name='bca-new'),
    path('link_account', views.link_account, name='link-account'),
    path('transactions', views.transactions, name='transactions'),
    path('transactions/get', views.get_transactions, name='get-transactions'),
    path('trans_category_update', views.trans_category_update, name='trans-category-update'),
    path('create_link_token', views.create_link_token, name='create_link_token'),
    path('get_access_token', views.get_access_token, name='get-access-token'),
    path('auth', views.get_auth, name="get-auth"),
    path('signup', views.signup, name="signup"),
    path('create_user', views.create_user, name='create-user'),
    path('log_in', views.log_in, name='log_in'),
    path('log_in_form', views.log_in_form, name='log-in-form'),
    path('log_out', views.log_out, name='log-out'),
    path('refresh_accounts', views.refresh_accounts, name='refresh-accounts'),
    
    path('savings/goals/create/', views.create_savings_goal, name='create_savings_goal'),
    path('savings/goals/', views.view_savings_goals, name='view_savings_goals'),
    path('savings/goals/update/<int:goal_id>/', views.update_savings_goal, name='update_savings_goal'),
 
]