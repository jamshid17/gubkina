from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import datetime
from django.core.validators import FileExtensionValidator


def year_choices():
    return [(r, r) for r in range(2000, datetime.date.today().year + 5)]


class MainInfoModel(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = 'Male', 'Мужчина'
        FEMALE = 'Female', 'Женщина'

    class GraduationPlaceChoices(models.TextChoices):
        SCHOOL = "School", "Школа"
        COLLEGE = "College", "Колледж"
        LYCEUM = "Lyceum", "Лицей"

    class MajorChoices(models.TextChoices):
        TECHNIC = 'Technic', 'Техническое направление'
        ECONOMIC = 'Economic', 'Экономическое направление'

    class MainTechnicMinorChoices(models.TextChoices):
        NONE = "None", "Выберите (приоритетный) профиль подготовки"
        GI = "GI", "Геофизические методы исследования скважин (ГИ) (специалитет)"
        GC = "GC", "Цифровой геоинжиниринг (ГЦ) (специалитет)"
        RB = "RB", "Бурение нефтяных и газовых скважин (РБ)"
        OS = "OS", "Эксплуатация и обслуживание объектов добычи нефти (РН)"
        DG = "DG", "Эксплуатация и обслуживание объектов добычи газа, газоконденсата и подземных хранилищ (РГ)"
        TS = "TS", "Сооружение и ремонт газонефтепроводов и газонефтехранилищ (ТС)"
        TP = "TP", "Эксплуатация и обслуживание объектов транспорта и хранения нефти, газа и продуктов переработки (ТП)"
        RT = "RT", "Технология бурения нефтяных и газовых скважин на суше и море (РТ) (специалитет)"
        RS = "RS", "Разработка и эксплуатация нефтяных и газовых месторождений (РС) (специалитет)"

    class SecondaryTechnicMinorChoices(models.TextChoices):
        NONE = "None", "Выберите дополнительный профиль подготовки"
        GI = "GI", "Геофизические методы исследования скважин (ГИ) (специалитет)"
        GC = "GC", "Цифровой геоинжиниринг (ГЦ) (специалитет)"
        RB = "RB", "Бурение нефтяных и газовых скважин (РБ)"
        OS = "OS", "Эксплуатация и обслуживание объектов добычи нефти (РН)"
        DG = "DG", "Эксплуатация и обслуживание объектов добычи газа, газоконденсата и подземных хранилищ (РГ)"
        TS = "TS", "Сооружение и ремонт газонефтепроводов и газонефтехранилищ (ТС)"
        TP = "TP", "Эксплуатация и обслуживание объектов транспорта и хранения нефти, газа и продуктов переработки (ТП)"
        RT = "RT", "Технология бурения нефтяных и газовых скважин на суше и море (РТ) (специалитет)"
        RS = "RS", "Разработка и эксплуатация нефтяных и газовых месторождений (РС) (специалитет)"

    class MainEconomicMinorChoices(models.TextChoices):
        NONE = "None" , "Выберите (приоритетный) профиль подготовки"
        EE = "EE", "Экономика и проекты устойчивого развития энергетики (ЭЭ)"
        EM = "EM", "Управление бизнесом в энергетике (ЭМ)"

    class SecondaryEconomicMinorChoices(models.TextChoices):
        NONE = "None" , "Выберите второй дополнительный профиль подготовки"
        EE = "EE", "Экономика и проекты устойчивого развития энергетики (ЭЭ)"
        EM = "EM", "Управление бизнесом в энергетике (ЭМ)"



    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)
    birth_date = models.DateField()
    nationality = models.CharField(max_length=50)
    birth_place = models.CharField(max_length=200)
    living_place = models.CharField(max_length=200)
    citizenship = models.CharField(max_length=200)
    identity_document_name = models.CharField(max_length=100)
    identity_document_ser = models.CharField(max_length=10)
    identity_document_id = models.CharField(max_length=100)
    identity_document_issued_info = models.CharField(max_length=400)
    home_phone_number = PhoneNumberField(null=True, blank=True)
    own_phone_number = PhoneNumberField()
    email = models.EmailField()
    # graduation fields
    graduation_place = models.CharField(
        max_length=20,
        choices=GraduationPlaceChoices.choices, 
        default=GraduationPlaceChoices.SCHOOL
    )
    graduation_certificate_ser = models.CharField(max_length=50)
    graduation_year = models.IntegerField(choices=year_choices())
    copy_passport = models.FileField(
        upload_to='files/passports',
        validators=[FileExtensionValidator(
            allowed_extensions=["pdf", "jpg", "jpeg", "png"]
        )])
    copy_graduation_certificate = models.FileField(
        upload_to='files/gr_certificates',
        validators=[FileExtensionValidator(
            allowed_extensions=["pdf", "jpg", "jpeg", "png"]
        )])
    image_three_to_four = models.FileField(
        upload_to='files/three_to_four',
        validators=[FileExtensionValidator(
            allowed_extensions=["pdf", "jpg", "jpeg", "png"]
        )])
    # majoring fields
    major_choice = models.CharField(
        max_length=200,
        choices=MajorChoices.choices,
        default=None
    )
    technic_major_choice_first = models.CharField(
        max_length=200,
        choices=MainTechnicMinorChoices.choices,
        default=MainTechnicMinorChoices.NONE,
    )
    technic_major_choice_second = models.CharField(
        max_length=200,
        choices=SecondaryTechnicMinorChoices.choices,
        default=SecondaryTechnicMinorChoices.NONE,
    )
    technic_major_choice_third = models.CharField(
        max_length=200,
        choices=SecondaryTechnicMinorChoices.choices,
        default=SecondaryTechnicMinorChoices.NONE,
    )
    economic_major_choice_first = models.CharField(
        max_length=200,
        choices=MainEconomicMinorChoices.choices,
        default=MainEconomicMinorChoices.choices,
    )

    economic_major_choice_second = models.CharField(
        max_length=200,
        choices=SecondaryEconomicMinorChoices.choices,
        default=SecondaryEconomicMinorChoices.choices,
    )
    # confirming
    first_confirm = models.BooleanField()
    second_confirm = models.BooleanField()


email_addresses = {
    "GI":"ilhomhafizov6@gmail.com",
    "GC":"ilhomhafizov6@gmail.com",
    # "GI":"gi@gubkin.uz",
    # "GC":"gc@gubkin.uz",
    # "RB":"rb@gubkin.uz",
    # "OS":"rn@gubkin.uz",
    # "DG":"rg@gubkin.uz",
    # "TS":"ts@gubkin.uz",
    # "TP":"tp@gubkin.uz",
    # "RT":"rt@gubkin.uz",
    # "RS":"rs@gubkin.uz",
    # "EE":"ee@gubkin.uz",
    # "EM":"em@gubkin.uz"
}
