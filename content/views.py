from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


class TermsView(TemplateView):
    template_name = 'terms.html'
