from django.shortcuts import render
from .forms import MainInfoForm, TestForm
# Create your views here.

def home_form_view(request):
    context = {}
    if request.method == "GET":
        form = MainInfoForm()
        context['form'] = form
    elif request.method == "POST":
        form = MainInfoForm(request.POST, request.FILES)
        if form.is_valid():
            #some pdf action is here
            form.save()
            #some messaging
        else:
            #error messaging
            print(form.instance.__dict__)
            print(form.errors, " errors")
            context['form'] = form

    return render(request, 'main/main.html', context=context)   
    

def another_test_view(request):
    context = {}
    if request.method == "GET":
        form = TestForm()
        context['form'] = form
    elif request.method == "POST":
        form = TestForm(data=request.POST)
        print("posted here")
        
    return render(request, 'main/another.html', context=context)   
    