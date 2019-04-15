from confapp import conf
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlQueryList
from pyforms.controls import ControlText
from pyforms.controls import ControlButton
from pyforms.controls import ControlAutoComplete
from humanresources.models import Person
from research.models import Group
from pyforms.basewidget import no_columns

class SearchWidget(BaseWidget):

    MODEL = Person

    UID = 'search'
    TITLE = 'Find people'

    LIST_DISPLAY = [
        'name',
        'person_email',
        'thumbnail_80x80',
    ]

    SEARCH_FIELDS = [
        'person_first__icontains',
        'person_last__icontains',
    ]

    LIST_FILTER = [
        'groupmember__group',
        'groupmember__position',
    ]

    # Orquestra Configuration
    # =========================================================================

    LAYOUT_POSITION = conf.ORQUESTRA_HOME

    ORQUESTRA_MENU = 'left'
    ORQUESTRA_MENU_ICON = 'search'
    ORQUESTRA_MENU_ORDER = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._search = ControlText('Search by name', on_enter_event=self.populate_list )
        self._groups = ControlAutoComplete("Filter by groups", queryset=Group.objects.all(), multiple=True, changed_event=self.populate_list)
        self._list   = ControlQueryList('People', list_display=self.LIST_DISPLAY)

        self.formset = [
            '_search',
            '_groups',
            '_list'
        ]

        self.populate_list()
        
    def populate_list(self):
        qs = Person.objects.active()
        has_filter = False
        
        if self._search.value:
            qs = qs.filter(full_name__icontains=self._search.value)
            has_filter = True
        
        if self._groups.value:
            qs = qs.filter_by_groups(self._groups.value)
            has_filter = True

        if has_filter:
            qs = qs.order_by('full_name')
        else:
            qs = qs.order_by('?')

        self._list.value = qs
