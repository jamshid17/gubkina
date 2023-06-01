from django.shortcuts import render
from .forms import MainInfoForm
from django.contrib import messages
from django.conf import settings
import os 
from PIL import Image


base_certificate_path = os.path.join(settings.BASE_DIR, "files", "gr_certificates")
base_passport_path = os.path.join(settings.BASE_DIR, "files", "passports")
base_three_to_four_path = os.path.join(settings.BASE_DIR, "files", "three_to_four")

# Create your views here.
def convert_pdfs(instance):
    certificate_path = os.path.join(base_certificate_path, f"{instance.copy_graduation_certificate}")
    passport_path = os.path.join(base_passport_path, f"{instance.copy_passport}")
    three_to_four_path = os.path.join(base_three_to_four_path, f"{instance.image_three_to_four}")

    #  = Image.open(certificate_path)
    # im_1 = image_1.convert('RGB')
    # im_1.save(r'path where the pdf will be stored\new file name.pdf') 

def home_form_view(request):
    context = {}
    if request.method == "GET":
        form = MainInfoForm()
        context['form'] = form
    elif request.method == "POST":
        form = MainInfoForm(request.POST, request.FILES)
        if form.is_valid():
            #some pdf action is here

            instance = form.save()

            messages.success(request, 'Muvaffaqiyatli yaratildi!')
        else:
            errors_dict = form.errors.as_data()
            first_error_message = errors_dict[list(errors_dict.keys())[0]][0].message
            messages.warning(request, first_error_message)
        context['form'] = form

    return render(request, 'main/main.html', context=context)   
    