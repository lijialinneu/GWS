from django.shortcuts import render

from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from account.models import User
from django.views.decorators.csrf import csrf_exempt

class UserForm(forms.Form):
    email = forms.EmailField(label='email')
    password = forms.CharField(label='password',widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })


@csrf_exempt
def sign_in(request):
    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():
            email = uf.cleaned_data['email']
            password = uf.cleaned_data['password']
            user = User.objects.filter(email=email, password=password)
            if user: 
                tip = "登录成功"
                return render_to_response('sign_in.html', {'uf':uf, 'tip':tip})
            else:
                tip = "邮箱或密码不对"
                return render_to_response('sign_in.html', {'uf':uf, 'tip':tip})
    else:
        uf = UserForm()
    return render_to_response('sign_in.html', {'uf':uf})


@csrf_exempt
def sign_up(request):
    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():
            email = uf.cleaned_data['email']
            password = uf.cleaned_data['password']

            user = User.objects.get(email=email)
            if user:
                tip = "这个邮箱已经被注册了"
                return render_to_response('sign_up.html', {'uf':uf, 'tip':tip})
            else:
                user = User()
                user.email = email
                user.password = password           
                user.save()
                tip = "注册成功，去登录试试看"
                return render_to_response('sign_up.html',{'uf':uf, 'tip':tip})
    else:
        uf = UserForm()
    return render_to_response('sign_up.html',{'uf':uf})
