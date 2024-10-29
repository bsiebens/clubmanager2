# class OrderFilter(django_filters.FilterSet):
#     lineitem__member__user__first_name = django_filters.CharFilter(lookup_expr="icontains", label=_("First Name"), distinct=True)
#     lineitem__member__user__last_name = django_filters.CharFilter(lookup_expr="icontains", label=_("Last Name"), distinct=True)
#
#     class Meta:
#         model = Order
#         fields = ["lineitem__member__user__first_name", "lineitem__member__user__last_name", "season", "status", "lineitem__material"]
#
#     def filter_queryset(self, queryset):
#         return super().filter_queryset(queryset).distinct()
