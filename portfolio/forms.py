from django.forms import ModelForm

from .models import Site


class SiteForm(ModelForm):
    class Meta:
        model = Site
        fields = ['name', 'url', 'contact_receiver_email']
        labels = {
            'name': 'Site Name',
            'url': 'Site URL',
        }

        help_texts = {
            'name': 'Enter the name of your site',
            'url': 'Enter the URL of your site',
        }
        # error_messages = {
        #     'name': {
        #         'required': 'Name is required',
        #     },
        #     'url': {
        #         'required': 'URL is required',
        #     }
        # }
