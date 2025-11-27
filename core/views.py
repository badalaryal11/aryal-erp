from django.views.generic import TemplateView
from django.shortcuts import render

def home(request):
    return render(request, 'core/home.html')

class ContactView(TemplateView):
    template_name = 'core/contact.html'
