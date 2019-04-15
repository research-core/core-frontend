# from .dashboard import DashboardWidget
from .profile import UserProfileFormWidget
from .search import SearchWidget
from .external_links import WikiLink
from .external_links import RequisitionsLink
from .external_links import QlikViewLink
from .external_links import NexBittLink
from .external_links import iLabLink
from .external_links import FundingOpportunitiesLink

__all__ = (
    # 'DashboardWidget',
    UserProfileFormWidget,
    SearchWidget,
    WikiLink,
    RequisitionsLink,
    QlikViewLink,
    NexBittLink,
    iLabLink,
    FundingOpportunitiesLink,
)
