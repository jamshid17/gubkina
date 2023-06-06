from django.shortcuts import render, HttpResponse
from .forms import MainInfoForm
from django.contrib import messages
from django.conf import settings
from PIL import Image
from PyPDF2 import PdfMerger
import time, jinja2, os
from pyhtml2pdf import converter
from .models import MainInfoModel, email_addresses
from django.core.mail import send_mail, EmailMessage
from gubkina.config import CONFIG




base_certificate_path = os.path.join("files", "gr_certificates")
base_passport_path = os.path.join("files", "passports")
base_three_to_four_path = os.path.join("files", "three_to_four")
# Create your views here


def convert_pdfs(instance):
    certificate_path = str(instance.copy_graduation_certificate)
    passport_path = str(instance.copy_passport)
    three_to_four_path = str(instance.image_three_to_four)
    print(certificate_path, " certificate_path")
    print(passport_path, " passport_path")
    print(three_to_four_path, " three_to_four_path")

    merger = PdfMerger()

    if certificate_path.endswith(".pdf"):
        final_certificate_path = certificate_path
    else:
        image = Image.open(certificate_path)
        converted_file = image.convert('RGB')
        now = time.time()
        final_certificate_path = os.path.join(settings.BASE_DIR, "files",
                                              "samples", f"{now}.pdf")
        converted_file.save(final_certificate_path)
    merger.append(final_certificate_path)

    if passport_path.endswith(".pdf"):
        final_passport_path = passport_path
    else:
        image = Image.open(passport_path)
        converted_file = image.convert('RGB')
        now = time.time()
        final_passport_path = os.path.join(settings.BASE_DIR, "files",
                                           "samples", f"{now}.pdf")
        converted_file.save(final_passport_path)
    merger.append(final_passport_path)

    if three_to_four_path.endswith(".pdf"):
        final_three_to_four_path = three_to_four_path
    else:
        image = Image.open(three_to_four_path)
        converted_file = image.convert('RGB')
        now = time.time()
        final_three_to_four_path = os.path.join(settings.BASE_DIR, "files",
                                                "samples", f"{now}.pdf")
        converted_file.save(final_three_to_four_path)
    merger.append(final_three_to_four_path)
    print(final_certificate_path,)
    print(final_passport_path,)
    print(final_three_to_four_path,)
    merged_file_path = "files/merged_pages.pdf"
    merger.write(merged_file_path)

    return merged_file_path


def create_pdf_form(context, merged_file_path):
    template_loader = jinja2.FileSystemLoader("./")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("files/template.html")
    output_text = template.render(context)
    with open('files/new.html', 'w') as f:
        f.write(output_text)

    now = time.time()
    rendered_file_path = f'files/{now}.pdf'
    old_html_file_path = os.path.abspath('files/new.html')
    converter.convert(f'file:///{old_html_file_path}', rendered_file_path)
    # merging finally

    merger = PdfMerger()
    merger.append(rendered_file_path)
    merger.append(merged_file_path)
    now = time.time()
    final_merged_file_path = f"files/merged_files/{now}.pdf"
    merger.write(final_merged_file_path)

    # removing
    old_rendered_file_path = os.path.abspath(rendered_file_path)
    os.remove(old_rendered_file_path)
    old_merged_file_path = os.path.abspath(merged_file_path)
    os.remove(old_merged_file_path)
    os.remove(old_html_file_path)

    return final_merged_file_path


def get_final_major_choice_name(cleaned_data):
    final_major_choice_name = ''
    if cleaned_data['major_choice'] == MainInfoModel.MajorChoices.TECHNIC:
        final_major_choice_name += cleaned_data['technic_major_choice_first_name']
        if cleaned_data['technic_major_choice_second'] != MainInfoModel.MainTechnicMinorChoices.NONE:
            final_major_choice_name += ',  ' + cleaned_data['technic_major_choice_second_name']
        if cleaned_data['technic_major_choice_third'] != MainInfoModel.MainTechnicMinorChoices.NONE:
            final_major_choice_name += ',  ' + cleaned_data['technic_major_choice_third_name']       
    else:
        final_major_choice_name += cleaned_data['economic_major_choice_first_name']
        if cleaned_data['economic_major_choice_second'] != MainInfoModel.MainTechnicMinorChoices.NONE:
            final_major_choice_name += ',  ' + cleaned_data['economic_major_choice_second_name']
    return final_major_choice_name


def home_form_view(request):
    context = {}
    if request.method == "GET":
        form = MainInfoForm()
        context['form'] = form
    elif request.method == "POST":
        form = MainInfoForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            cleaned_data = form.cleaned_data
            cleaned_data['gender'] = instance.get_gender_display()
            cleaned_data['graduation_place'] = instance.get_graduation_place_display()
            if cleaned_data["major_choice"] == MainInfoModel.MajorChoices.TECHNIC:
                cleaned_data['technic_major_choice_first_name'] = instance.get_technic_major_choice_first_display()
                cleaned_data['technic_major_choice_second_name'] = instance.get_technic_major_choice_second_display()
                cleaned_data['technic_major_choice_third_name'] = instance.get_technic_major_choice_third_display()
                cleaned_data["economic_major_choice_first"] == MainInfoModel.MainEconomicMinorChoices.NONE
                cleaned_data["economic_major_choice_second"] == MainInfoModel.MainEconomicMinorChoices.NONE
            else:

                cleaned_data['economic_major_choice_first_name'] = instance.get_economic_major_choice_first_display()
                cleaned_data['economic_major_choice_second_name'] = instance.get_economic_major_choice_second_display()
                cleaned_data["technic_major_choice_first"] = MainInfoModel.MainTechnicMinorChoices.NONE
                cleaned_data["technic_major_choice_second"] = MainInfoModel.MainTechnicMinorChoices.NONE
                cleaned_data["technic_major_choice_third"] = MainInfoModel.MainTechnicMinorChoices.NONE
            cleaned_data['final_major_choice_name'] = get_final_major_choice_name(cleaned_data)
            # some pdf action is here
            instance = form.save()
            if cleaned_data['home_phone_number']:
                cleaned_data['home_phone_number'] = cleaned_data['home_phone_number'].as_e164
            cleaned_data['own_phone_number'] = cleaned_data['own_phone_number'].as_e164
            # initial_merged_file_path = convert_pdfs(instance=instance)
            # final_merged_file_path = create_pdf_form(cleaned_data, initial_merged_file_path)
            # print(final_merged_file_path, " fin")
            #emails
            receiver_email_addresses = []
            if cleaned_data["major_choice"] == MainInfoModel.MajorChoices.TECHNIC:  
                technic_major_choice_first_email = email_addresses[cleaned_data["technic_major_choice_first"]]
                receiver_email_addresses.append(technic_major_choice_first_email)
            else:  
                economic_major_choice_first_email = email_addresses[cleaned_data["economic_major_choice_first"]]
                receiver_email_addresses.append(economic_major_choice_first_email)
            initial_merged_file_path = convert_pdfs(instance=instance)
            final_merged_file_path = create_pdf_form(cleaned_data, initial_merged_file_path)

            email = EmailMessage(
                subject="Subject",
                body="",
                from_email=CONFIG.email_host_user,
                to=receiver_email_addresses,
            )
            email.attach_file(final_merged_file_path)
            email.send()
            context['form'] = MainInfoForm()
            messages.success(request, 'Ваше заявление отправлено и обрабатывается технической группой приемной комиссии. Ожидайте смс-уведомление с регистрационным номером в течении 24 часов.')
        else:
            errors_dict = form.errors.as_data()
            first_error_message = errors_dict[list(errors_dict.keys())[0]][0].message
            messages.warning(request, first_error_message)
        context['form'] = form

    return render(request, 'main/main.html', context=context)
