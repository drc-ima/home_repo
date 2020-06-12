from django.contrib.auth.views import LoginView
from django.urls import path

from adminie.views import *

app_name = 'adminie'

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('properties/', Properties.as_view(), name='properties'),
    path('prop/new/', NewProperty.as_view(), name='prop-new'),
    path('xyz/', Admins.as_view(), name='admins'),
    path('xyz/new/', NewAdmin.as_view(), name='new-admin'),
    path('prop/detail/<id>/', ProjectDetail.as_view(), name='prop-detail'),
    path('payment/<id>/<type>/<client>/', NewPayment.as_view(), name='payment'),
    path('receipt/<id>/', ReceiptDetail.as_view(), name='receipt'),
    path('sign/<id>/', AgreementPage.as_view(), name='sign'),
]