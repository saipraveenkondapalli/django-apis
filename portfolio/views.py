from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DeleteView

from .forms import SiteForm
from .models import Site


class SiteView(LoginRequiredMixin, View):
    def get(self, request):
        sites = Site.objects.filter(user=request.user)
        return render(request, "portfolio/dashboard.html", {"sites": sites})


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
