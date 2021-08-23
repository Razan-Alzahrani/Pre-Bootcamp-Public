from django.urls import path 
from . import views
urlpatterns = [
    path('' , views.index),
    path('sp_register' , views.sp_register),
    path('login_page', views.login_page),
    path('login', views.login),
    path('freelancer' , views.freelancer),
    path('login_customer', views.login_customer),
    path('edit_account/<int:id>', views.edit_account),
    path('updated_account/<int:id>', views.updated_account),
    path('costumer_register' , views.costumer_register),
    path('customer' , views.customer),
    path('add_proj' , views.add_proj),
    path('create_proj' , views.create_proj),
    path('accept_req' , views.accept_req),
    path('create_req' , views.create_req),
    path('delete/<int:id>' , views.delete),
    path('logout' , views.logout),
    path('view/<int:id>', views.view),
    path('approved/<int:id>', views.approved)

]