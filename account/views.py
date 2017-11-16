from django.shortcuts import render

from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from account.models import User


class UserForm(forms.Form):
    email = forms.EmailField(label='email')
    passworld = forms.CharField(label='password',widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })


# Create your views here.
def register(request):
    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():
            email = uf.cleaned_data['email']
            passworld = uf.cleaned_data['passworld']

            user = User()
            user.passworld = passworld
            user.email = email
            user.save()
            return render_to_response('success.html',{'username':username})
    else:
        uf = UserForm()
    return render_to_response('register.html',{'uf':uf})
