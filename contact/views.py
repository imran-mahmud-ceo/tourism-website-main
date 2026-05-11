from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage, OfficeLocation
from django import forms


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.ip_address = request.META.get('REMOTE_ADDR')
            msg.save()
            messages.success(request, 'Thank you! Your message has been received. We will get back to you shortly.')
            return redirect('contact:contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    offices = OfficeLocation.objects.filter(is_active=True)
    return render(request, 'contact/contact.html', {'form': form, 'offices': offices})
