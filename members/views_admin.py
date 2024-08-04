from django_filters.views import FilterView

from .filters import MemberFilter


class MemberList(FilterView):
    filterset_class = MemberFilter
    paginate_by = 50
