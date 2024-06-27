from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DeleteView, ListView, UpdateView

from .forms import SiteForm
from .models import Site, Contact


class SiteView(LoginRequiredMixin, ListView):
    template_name = 'portfolio/dashboard.html'
    model = Site
    ordering = ['-created_at']
    context_object_name = 'sites'
    paginate_by = 1

    def get_queryset(self):
        search = self.request.GET.get('search', '')

        search_query = Q()

        search_query |= Q(name__icontains=search) if search else Q()
        search_query |= Q(url__icontains=search) if search else Q()

        search_query &= Q(user=self.request.user)

        return Site.objects.filter(search_query).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search')
        return context


class SiteDeleteView(LoginRequiredMixin, DeleteView):
    model = Site
    template_name = 'portfolio/site_confirm_delete_view.html'

    def post(self, request, *args, **kwargs):
        site = self.get_object()

        if site.user != request.user:
            messages.error(request, "You are not authorized to delete this site")
            return redirect('portfolio:dashboard')

        messages.success(request, "Site deleted successfully")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('portfolio:dashboard')


class SiteCreateView(LoginRequiredMixin, View):
    def get(self, request):
        forms = SiteForm()
        return render(request, "portfolio/new_site.html", {"form": forms})

    def post(self, request):
        form = SiteForm(request.POST)
        # add user to the form
        form.instance.user = request.user

        if not form.is_valid():
            return render(request, "portfolio/new_site.html", {"form": form})

        form.save()

        messages.success(request, "Site created successfully")
        return redirect('portfolio:dashboard')


class SiteUpdateView(LoginRequiredMixin, UpdateView):
    model = Site
    template_name = 'portfolio/new_site.html'
    form_class = SiteForm

    def post(self, request, *args, **kwargs):
        site = self.get_object()

        if site.user != request.user:
            messages.error(request, "You are not authorized to update this site")
            return redirect('portfolio:dashboard')

        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('portfolio:dashboard')


class ContactView(LoginRequiredMixin, ListView):
    template_name = 'portfolio/contacts.html'
    model = Contact
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        search = self.request.GET.get('search', '')

        search_query = Q()

        search_query |= Q(name__icontains=search) if search else Q()
        search_query |= Q(email__icontains=search) if search else Q()
        search_query |= Q(site__name__icontains=search) if search else Q()

        search_query &= Q(site__user=self.request.user)

        return Contact.objects.filter(search_query)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_name'] = self.request.GET.get('name')
        context['search_email'] = self.request.GET.get('email')
        context['search_site'] = self.request.GET.get('site')

        return context
