from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.query import QuerySet
from django.forms import Form
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.views.generic.list import ListView
from django_filters.views import FilterView
from .forms import EditorAddForm, NewsItemForm
from .models import NewsItem
from .filters import NewsItemFilter
from .rules import is_editor
from django.db.models import Count


class EditorListView(ListView):
    model = get_user_model()
    paginate_by = 200
    template_name = "news/editor_list.html"

    def get_queryset(self) -> QuerySet[Any]:
        group = Group.objects.get(name="editors")

        return super(EditorListView, self).get_queryset().filter(groups=group, is_active=True).order_by("last_name", "first_name")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(EditorListView, self).get_context_data(**kwargs)
        context["form"] = EditorAddForm()

        return context


class EditorAddView(SuccessMessageMixin, FormView):
    form_class = EditorAddForm
    success_url = reverse_lazy("clubmanager_admin:news:editors_index")
    success_message = _("Editor %(name)s was added succesfully")
    template_name = "news/editor_form.html"

    def form_valid(self, form: EditorAddForm) -> HttpResponse:
        form.save_member()

        return super(EditorAddView, self).form_valid(form)

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=cleaned_data["member"].user.get_full_name())


class EditorDeleteView(SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy("clubmanager_admin:news:editors_index")
    success_message = _("Editor was succesfully removed")
    model = get_user_model()
    template_name = "news/editor_confirm_delete.html"

    def form_valid(self, form: Form) -> HttpResponse:
        self.object = self.get_object()

        editors = Group.objects.get(name="editors")
        self.object.groups.remove(editors)

        return HttpResponseRedirect(self.get_success_url())


class NewsListView(FilterView):
    model = NewsItem
    paginate_by = 50
    filterset_class = NewsItemFilter

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(NewsListView, self).get_context_data(**kwargs)
        context["draft"] = 0
        context["in_review"] = 0
        context["released"] = 0

        if self.request.user.has_perm(is_editor):
            counts = NewsItem.objects.values("status").annotate(Count("status"))

            for count in counts:
                match count["status"]:
                    case 0:
                        context["draft"] = count["status__count"]
                    case 1:
                        context["in_review"] = count["status__count"]
                    case 2:
                        context["released"] = count["status__count"]

        return context


class NewsAddView(SuccessMessageMixin, CreateView):
    model = NewsItem
    form_class = NewsItemForm
    success_url = reverse_lazy("clubmanager_admin:news:news_index")
    success_message = _("News item %(title)s was created succesfully")

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, title=self.object.title)

    def form_valid(self, form: NewsItemForm) -> HttpResponse:
        form.instance.author = self.request.user

        return super(NewsAddView, self).form_valid(form)


class NewsEditView(SuccessMessageMixin, UpdateView):
    model = NewsItem
    form_class = NewsItemForm
    success_url = reverse_lazy("clubmanager_admin:news:news_index")
    success_message = _("News item %(title)s was updated succesfully")

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, title=self.object.title)


class NewsDeleteView(SuccessMessageMixin, DeleteView):
    model = NewsItem
    success_url = reverse_lazy("clubmanager_admin:news:news_index")
    success_message = _("News item was succesfully deleted")


""" from typing import Any
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django_filters.views import FilterView

from .filters import MemberFilter
from .forms import MemberForm
from .models import Member


class MemberListView(FilterView):
    filterset_class = MemberFilter
    paginate_by = 50


class MemberDeleteView(SuccessMessageMixin, DeleteView):
    model = Member
    success_url = reverse_lazy("clubmanager_admin:members:index")
    success_message = _("Member was succesfully deleted")


class MemberAddView(SuccessMessageMixin, CreateView):
    model = Member
    form_class = MemberForm
    success_url = reverse_lazy("clubmanager_admin:members:index")
    success_message = _("Member %(name)s was created succesfully")

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.user.get_full_name())


class MemberEditView(SuccessMessageMixin, UpdateView):
    model = Member
    form_class = MemberForm
    success_url = reverse_lazy("clubmanager_admin:members:index")
    success_message = _("Member %(name)s was updated succesfully")

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=self.object.user.get_full_name())

    def get_initial(self) -> dict[str, Any]:
        initial_data = super(MemberEditView, self).get_initial()

        initial_data["first_name"] = self.object.first_name
        initial_data["last_name"] = self.object.last_name
        initial_data["email"] = self.object.email

        return initial_data
 """
