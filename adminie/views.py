from random import randrange

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import *

from adminie.forms import *
from property.models import *


def generate_id(alpha):
    FROM = '0123456789'
    LENGTH = 7
    user_id = ""
    for i in range(LENGTH):
        user_id += FROM[randrange(0, len(FROM))]
    return f'{alpha}{user_id}'


class NewProperty(LoginRequiredMixin, CreateView):
    form_class = PropertyForm
    template_name = 'property/new.html'
    success_url = reverse_lazy('adminie:properties')

    def form_valid(self, form):
        valid = super(NewProperty, self).form_valid(form)

        form.instance.added_by = self.request.user

        form.instance.property_id = generate_id('PTY')
        form.instance.status = 'NEW'
        form.instance.bought = False

        if form.instance.property_type == 'Sale':

            form.instance.price = form.instance.price_sqft * form.instance.sqft


        form.save()

        return valid


class ProjectDetail(LoginRequiredMixin, DetailView):
    model = Property
    pk_url_kwarg = 'id'
    queryset = Property.objects.all()
    template_name = 'adminie/pro-details.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        try:
            context['receipt'] = Receipt.objects.get(propertie__id=self.kwargs.get('id'))
        except Receipt.DoesNotExist:
            pass
        return context


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'adminie/dashboard.html'


class Properties(LoginRequiredMixin, ListView):
    template_name = 'adminie/properties.html'
    queryset = Property.objects.all()


class NewPayment(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('adminie:prop-detail', kwargs={'id': self.kwargs.get('id')})

    def post(self, request, *args, **kwargs):
        pay_type = kwargs.get('type')
        propertie = Property.objects.get(id=self.kwargs.get('id'))
        phone = request.POST.get('phone')
        card_type = request.POST.get('card_type')
        card_number = request.POST.get('card_number')
        carrier = request.POST.get('carrier')
        amount = request.POST.get('amount')
        cvv = request.POST.get('cvv')
        client_id = kwargs.get('client')
        expiry_date = request.POST.get('expiry_date')

        client = Client.objects.get(id=client_id)
        payment = None
        if pay_type == 'Momo':
            payment = Payment.objects.create(
                pay_id=generate_id('MM'),
                propertie=propertie,
                phone_number=phone,
                carrier=carrier,
                amount=propertie.price,
                created_by=self.request.user,
                payment_type=pay_type,
                client=client
            )
            
            payment.save()
        elif pay_type == 'Card':
            payment = Payment.objects.create(
                pay_id=generate_id('VM'),
                propertie=propertie,
                client=client,
                cvv=cvv,
                visa_master=card_number,
                card_type=card_type,
                expiry_date=expiry_date,
                amount=propertie.price,
                created_by=self.request.user,
                payment_type=pay_type
            )
            
            payment.save()
            
        if propertie.property_type == 'Sale':
            propertie.status = 'SOLD'
            propertie.bought = True
        elif propertie.property_type == 'Rent':
            propertie.status = 'RENTED'

        receipt = Receipt.objects.create(
            receipt_id=generate_id('INV'),
            client=client,
            payment=payment,
            propertie=propertie
        )

        receipt.save()
        
        client.status = 'PAID'

        propertie.save()
        client.save()
        
        return super(NewPayment, self).post(self, request, *args, **kwargs)
        
        
class ReceiptDetail(LoginRequiredMixin, DetailView):
    model = Receipt
    queryset = Receipt.objects.all()
    pk_url_kwarg = 'id'
    template_name = 'adminie/receipt.html'


class AgreementPage(LoginRequiredMixin, DetailView):
    model = Receipt
    queryset = Receipt.objects.all()
    pk_url_kwarg = 'id'
    template_name = 'adminie/sign.html'

    def get_context_data(self, **kwargs):
        context = super(AgreementPage, self).get_context_data(**kwargs)
        context['today'] = timezone.now()
        return context


class Admins(LoginRequiredMixin, ListView):
    model = User
    queryset = User.objects.all()
    template_name = 'adminie/admins.html'


class NewAdmin(LoginRequiredMixin, CreateView):
    form_class = UserForm
    template_name = 'adminie/new.html'
    success_url = reverse_lazy('adminie:admins')

    def form_valid(self, form):
        valid = super(NewAdmin, self).form_valid(form)

        form.instance.set_password(form.instance.password)

        form.save()

        return valid
