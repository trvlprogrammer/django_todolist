from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid:
            user = form.save()
            login(request,user)
            return redirect("todos:index")    
    form = SignUpForm()
    return render (request=request, template_name="accounts/register_form.html", context={"form" : form})