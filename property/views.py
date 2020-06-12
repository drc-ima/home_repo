# from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import *

from adminie.views import generate_id
from property.models import *


class PropertyCardList(ListView):
    model = Property
    template_name = 'property/index.html'
    queryset = Property.objects.all()

    def get_queryset(self):
        list_type = self.request.GET.get('type')
        property_type = self.request.GET.get('prop_type')
        location = self.request.GET.get('location')

        if list_type or property_type or location:
            lookup = Q(home_type__icontains=list_type) | Q(property_type=property_type) | Q(located__icontains=location)
            return Property.objects.filter(lookup)
        else:
            return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PropertyCardList, self).get_context_data(**kwargs)
        context['properties'] = self.queryset
        return context


class PropertyList(ListView):
    model = Property
    template_name = 'property/view-list.html'
    queryset = Property.objects.all()

    def get_queryset(self):
        list_type = self.request.GET.get('type')
        property_type = self.request.GET.get('prop_type')
        location = self.request.GET.get('location')

        if list_type or property_type or location:
            lookup = Q(home_type__icontains=list_type) | Q(property_type=property_type) | Q(located__icontains=location)
            return Property.objects.filter(lookup)
        else:
            return self.queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PropertyList, self).get_context_data(**kwargs)
        context['properties'] = self.queryset
        return context


class PropertyDetail(DetailView):
    model = Property
    pk_url_kwarg = 'id'
    queryset = Property.objects.all()
    template_name = 'property/details.html'

    def get_context_data(self, **kwargs):
        context = super(PropertyDetail, self).get_context_data(**kwargs)
        context['properties'] = Property.objects.all().all()
        return context


class ClientRequest(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('property:detail', kwargs={'id': self.kwargs.get('id')})

    def post(self, request, *args, **kwargs):
        propertie = Property.objects.get(id=self.kwargs.get('id'))
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        client = Client.objects.create(
            client_id=generate_id('CL'),
            name=name,
            propertie=propertie,
            email=email,
            phone=phone,
            status='REQUESTED'
        )

        propertie.status = 'REQUESTED'
        propertie.client_requests.add(client)

        propertie.save()
        client.save()

        return super(ClientRequest, self).post(self, request, *args, **kwargs)

