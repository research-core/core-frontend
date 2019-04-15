from django.contrib.staticfiles.templatetags.staticfiles import static

from confapp import conf
from pyforms_web.web.middleware import PyFormsMiddleware
from pyforms_web.widgets.django import ModelAdminWidget
from pyforms_web.widgets.django import ModelFormWidget
from pyforms.basewidget import segment
from pyforms.controls import ControlImg
from pyforms.controls import ControlSimpleLabel
from pyforms.controls import ControlEmptyWidget

from common.models import InstitutionAffiliation
from humanresources.models import Person
from humanresources.models import PrivateInfo
from humanresources.models import AcademicCareer
from research.models import GroupMember

from ..humanresources_apps.apps.people.profile_privateinfo import ProfilePrivateInfoFormWidget


class InstitutionAffiliationInline(ModelAdminWidget):
    MODEL = InstitutionAffiliation
    LIST_DISPLAY = ['institution', 'date_joined', 'date_left']
    FIELDSETS = [
        ('institution', 'date_joined', 'date_left')
    ]


class ResearchGroupsInline(ModelAdminWidget):
    MODEL = GroupMember

    LIST_DISPLAY = ['group', 'position', 'date_joined', 'date_left']

    def has_add_permissions(self):
        return False

    def has_view_permissions(self, obj):
        return False

    def has_update_permissions(self, obj):
        return False

    def has_remove_permissions(self, obj):
        return False


class AcademicCareerInline(ModelAdminWidget):
    MODEL = AcademicCareer

    LIST_DISPLAY = ['institution', 'degree', 'field_of_study', 'graduation_year']

    FIELDSETS = [
        ('institution', 'degree', 'field_of_study', 'graduation_year')
    ]


class UserProfileFormWidget(ModelFormWidget):

    UID = 'profile'
    TITLE = 'My Profile'

    MODEL = Person

    LAYOUT_POSITION = conf.ORQUESTRA_HOME

    ORQUESTRA_MENU = 'user'
    ORQUESTRA_MENU_ICON = 'user'
    ORQUESTRA_MENU_ORDER = 1

    HAS_CANCEL_BTN_ON_EDIT = False

    READ_ONLY = (
        'full_name',
        'person_gender',
        'person_img',
        'person_cardnum',
        'person_phoneext',
        'position',
    )

    FIELDSETS = [
        segment(
            ('_summary', '_img',),
        ),
        'h3:PERSONAL INFORMATION',
        {
            '1:General': [
                ('person_gender', 'person_birthday'),
                ('person_personalemail', 'person_mobile'),
                'person_cv',
                'person_emergencycontact',
            ],
            '2:Public': [
                # 'info:The information provided in the fields below will be shared publicly.',
                ('person_first', 'person_last', 'degree'),
                'person_bio',
            ],
            '3:Private': [
                '_privateinfo',
            ],
            '4:Institutional': [
                ('person_cardnum', 'person_phoneext'),
                'ResearchGroupsInline',
            ],
            '5:Affiliation':[
                'InstitutionAffiliationInline',
            ],
            '6:Education': [
                'AcademicCareerInline',
            ],
        },
    ]

    INLINES = [
        InstitutionAffiliationInline,
        ResearchGroupsInline,
        AcademicCareerInline,
    ]

    def __init__(self, *args, **kwargs):
        user = PyFormsMiddleware.user()
        person = Person.objects.get(djangouser=user)
        super().__init__(pk=person.pk, *args, **kwargs)

        membership = GroupMember.objects.filter(person=person).first()
        membership_html = (
            f'<h3><a>{membership.group}</a> - {membership.position}</h3>'
            if membership is not None
            else ''
        )
        s = (
            f'<h1>{person.full_name}</h1>'
            '<address>'
            f'{membership_html}'
            '\n'
            f'<a href="mailto:{person.person_email}" target="_blank">'
            f'<i class="envelope icon"></i>{person.person_email}</a>'
            '</address>'
        )
        self._summary = ControlSimpleLabel(
            default=s,
            label_visible=False,
            field_css='fourteen wide',
        )

        privateinfo, _ = PrivateInfo.objects.get_or_create(person=person)
        self._privateinfo = ControlEmptyWidget(
            parent=self,
            name='_privateinfo',
            default=ProfilePrivateInfoFormWidget(
                pk=privateinfo.pk,
                has_cancel_btn=False,
            ),
        )
        
        try:
            img_url = self.model_object.thumbnail_url(geometry_string='300x300')
        except AttributeError:
            img_url = static('square-image.png')
        self._img = ControlImg('Image', default=img_url, label_visible=False,
                               field_css='three wide')

    def save_form_event(self, obj):
        self._privateinfo.value.save_form_event(self._privateinfo.value.model_object)
        super().save_form_event(obj)

    def has_remove_permissions(self):
        return False
