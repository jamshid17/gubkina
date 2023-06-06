from typing import Any, Dict
from django import forms
from django.forms import  (
    ClearableFileInput,
    FileField,
    TextInput, 
    EmailInput, 
    Select, 
    RadioSelect,
    DateInput,
)
from django.core.exceptions import ValidationError
from .models import MainInfoModel


class FileForm(forms.Form):
    copy_passport = FileField(widget=ClearableFileInput())
    copy_certificate = FileField(widget=ClearableFileInput())
    image_three_to_four = FileField(widget=ClearableFileInput())


class MainInfoForm(forms.ModelForm):

    class Meta:
        model = MainInfoModel
        fields = '__all__'

        widgets = {
            'first_name': TextInput(attrs={
                'id': 'name',
                'class': "same_input",
                "placeholder": "Имя",
                }),
            'last_name': TextInput(attrs={
                "id": "surname",
                'class': "same_input",
                "placeholder": "Фамилия",
                }),
            'middle_name': TextInput(attrs={
                "id": "f-name",
                'class': "same_input",
                "placeholder": "Отчество",
                }),
            'gender': Select(attrs={
                "id": "surname",
                'class': "same_input",
                "placeholder": "Фамилия",
                }),
            'birth_date': DateInput(
                attrs={
                    "id": "date",
                    'class': "same_input",
                    'type': 'date',
                }),
            'nationality': TextInput(attrs={
                "id": "nation",
                'class': "same_input",
                "placeholder": "Национальность",
                }),
            'birth_place': TextInput(attrs={
                "id": "place",
                'class': "same_input",
                "placeholder": "Место рождения",
                }),
            'living_place': TextInput(attrs={
                "id": "place",
                'class': "same_input",
                "placeholder": "Место проживания",
                }),
            'citizenship': TextInput(attrs={
                "id": "native",
                'class': "same_input",
                "placeholder": "Гражданство",
                }),
            'identity_document_name': TextInput(attrs={
                "id": "nat_doc",
                'class': "same_input",
                "placeholder": "Документ личности",
                }),
            'identity_document_ser': TextInput(attrs={
                "id": "seria",
                'class': "same_input",
                "placeholder": "Серия",
                "style": "max-width: 80px;"
                }),
            'identity_document_id': TextInput(attrs={
                "id": "num",
                'class': "same_input",
                "placeholder": "Номер паспорта",
                "style": "max-width: 240px;"
                }),
            'identity_document_issued_info': TextInput(attrs={
                "id": "num",
                'class': "same_input",
                }),
            'home_phone_number': TextInput(attrs={
                "id": "phone",
                'class': "same_input",
                "placeholder": "+998",
                "value": "+998"
                }),
            'own_phone_number': TextInput(attrs={
                "id": "tel",
                'class': "same_input",
                "placeholder": "+998",
                "value": "+998"
                }),
            'email': EmailInput(attrs={
                "id": "gmail",
                'class': "same_input",
                'placeholder': 'Эл.почта'
                }),
            'graduation_place': Select(attrs={
                "empty_label": "something",
                "id": "select_edu",
                "style": "max-width: 100%; height: 30px; font-size: 18px; "

                }),
            'graduation_certificate_ser': TextInput(attrs={
                "id": "diploma",
                'class': "same_input",
                }),
            'graduation_year': Select(attrs={
                "id": "year_grad",
                'class': "same_input",
                }),
            'copy_passport': ClearableFileInput(attrs={
                "id": "choose_file",
                "class": "custom-file-input"
                }),
            'copy_graduation_certificate': ClearableFileInput(attrs={
                "id": "choose_file",
                "class": "custom-file-input"
                }),
            'image_three_to_four': ClearableFileInput(attrs={
                "id": "choose_file",
                "class": "custom-file-input"
                }),
            'major_choice': RadioSelect(attrs={
                "style": "max-width: 100%;",
                "class": "faculty_type",
            }),
            'technic_major_choice_first': Select(attrs={
                "style": "max-width: 100%; height: 40px",
                }),
            'technic_major_choice_second': Select(attrs={
                "style": "max-width: 100%; height: 40px"
                }),
            'technic_major_choice_third': Select(attrs={
                "style": "max-width: 100%; height: 40px"
                }),
            'economic_major_choice_first': Select(attrs={
                "style": "max-width: 100%; height: 40px"
                }),
            'economic_major_choice_second': Select(attrs={
                "style": "max-width: 100%; height: 40px"
                }),
            'need_dormitory': Select(attrs={
                "style": "width: 60px; height: 30px; font-size: 18px; "
            })
        }

    def clean(self):
        if not self.cleaned_data['first_confirm'] or not self.cleaned_data['second_confirm']:
            raise ValidationError("Пожалуйста, подтвердите, что информация, представленная вам в заявлении, является правильной")
        if self.cleaned_data["major_choice"] == MainInfoModel.MajorChoices.TECHNIC:  
            if self.cleaned_data["technic_major_choice_first"] == MainInfoModel.MainTechnicMinorChoices.NONE:
                raise ValidationError(
                    message="Вы должны выбирать основное направление!"
                )
            if self.cleaned_data["technic_major_choice_second"] != MainInfoModel.MainTechnicMinorChoices.NONE or \
                self.cleaned_data["technic_major_choice_third"] != MainInfoModel.MainTechnicMinorChoices.NONE:
                if len(set([self.cleaned_data["technic_major_choice_first"], self.cleaned_data["technic_major_choice_second"], self.cleaned_data["technic_major_choice_third"]])) != 3:
                    raise ValidationError(
                        message="Выбранные Вами направления являются одинаковыми!"
                    )
        elif self.cleaned_data["major_choice"] == MainInfoModel.MajorChoices.ECONOMIC:            
            if self.cleaned_data["economic_major_choice_first"] == MainInfoModel.MainEconomicMinorChoices.NONE:
                raise ValidationError(
                    message="Вы должны выбирать основное направление!"
                )
            if self.cleaned_data["economic_major_choice_first"] == self.cleaned_data["economic_major_choice_second"]:
                raise ValidationError(
                    message="Выбранные Вами направления являются одинаковыми!"
                )
        return super().clean()