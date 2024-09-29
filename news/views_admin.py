from typing import Any

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Count
from django.db.models.query import QuerySet
from django.forms import Form
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.views.generic.list import ListView
from django_filters.views import FilterView
from rules.contrib.views import PermissionRequiredMixin, objectgetter, permission_required

from .filters import NewsItemFilter
from .forms import EditorAddForm, NewsItemForm, NewsItemPictureFormSet
from .models import NewsItem
from .rules import is_editor


class EditorListView(PermissionRequiredMixin, ListView):
    model = get_user_model()
    paginate_by = 200
    template_name = "news/editor_list.html"
    permission_required = "editors"
    permission_denied_message = _("You do not have sufficient access rights to access the editor list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def get_queryset(self) -> QuerySet[Any]:
        group = Group.objects.get(name="editors")

        return super(EditorListView, self).get_queryset().filter(groups=group, is_active=True).order_by("last_name", "first_name")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(EditorListView, self).get_context_data(**kwargs)
        context["form"] = EditorAddForm()

        return context


class EditorAddView(PermissionRequiredMixin, SuccessMessageMixin, FormView):
    form_class = EditorAddForm
    success_url = reverse_lazy("clubmanager_admin:news:editors_index")
    success_message = _("Editor <strong>%(name)s</strong> added succesfully")
    template_name = "news/editor_form.html"
    permission_required = "editors"
    permission_denied_message = _("You do not have sufficient access rights to access the editor list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def form_valid(self, form: EditorAddForm) -> HttpResponse:
        form.save_member()

        return super(EditorAddView, self).form_valid(form)

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=cleaned_data["member"].user.get_full_name())


class EditorDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy("clubmanager_admin:news:editors_index")
    success_message = _("Editor <strong>%(name)s</strong> deleted succesfully")
    model = get_user_model()
    template_name = "news/editor_confirm_delete.html"
    permission_required = "editors"
    permission_denied_message = _("You do not have sufficient access rights to access the editor list")

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:index"))

    def form_valid(self, form: Form) -> HttpResponse:
        self.object = self.get_object()

        editors = Group.objects.get(name="editors")
        self.object.groups.remove(editors)

        return HttpResponseRedirect(self.get_success_url())

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, name=cleaned_data["member"].user.get_full_name())


class NewsListView(PermissionRequiredMixin, FilterView):
    model = NewsItem
    paginate_by = 25
    filterset_class = NewsItemFilter
    permission_required = "news.add_newsitem"

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

    def get_queryset(self) -> QuerySet[Any]:
        return super(NewsListView, self).get_queryset().select_related("author")


class NewsAddView(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = NewsItem
    form_class = NewsItemForm
    success_url = reverse_lazy("clubmanager_admin:news:news_index")
    success_message = _("News item <strong>%(title)s</strong> added succesfully")
    permission_required = "news.add_newsitem"
    permission_denied_message = _("You do not have sufficient access rights to add a new news item")

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, title=self.object.title)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(NewsAddView, self).get_context_data(**kwargs)

        if self.request.POST:
            context["pictures"] = NewsItemPictureFormSet(self.request.POST, self.request.FILES)
        else:
            context["pictures"] = NewsItemPictureFormSet()

        return context

    def form_valid(self, form: NewsItemForm) -> HttpResponse:
        context = self.get_context_data()

        pictures = context["pictures"]
        with transaction.atomic():
            form.instance.author = self.request.user
            self.object = form.save()

            if pictures.is_valid():
                pictures.instance = self.object
                pictures.save()

        return super(NewsAddView, self).form_valid(form)


class NewsEditView(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = NewsItem
    form_class = NewsItemForm
    success_url = reverse_lazy("clubmanager_admin:news:news_index")
    success_message = _("News item <strong>%(title)s</strong> updated succesfully")
    permission_required = "news.change_newsitem"
    permission_denied_message = _("You do not have sufficient access rights to edit <strong>%(title)s</strong>")

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, title=self.object.title)

    def get_permission_denied_message(self) -> str:
        return self.permission_denied_message % dict(title=self.get_object().title)

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=self.success_url)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(NewsEditView, self).get_context_data(**kwargs)

        if self.request.POST:
            context["pictures"] = NewsItemPictureFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context["pictures"] = NewsItemPictureFormSet(instance=self.object)

        return context

    def form_valid(self, form: NewsItemForm) -> HttpResponse:
        context = self.get_context_data()

        pictures = context["pictures"]
        with transaction.atomic():
            self.object = form.save()

            if pictures.is_valid():
                pictures.save()

        return super(NewsEditView, self).form_valid(form)


class NewsDeleteView(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    model = NewsItem
    success_url = reverse_lazy("clubmanager_admin:news:news_index")
    success_message = _("News item <strong>%(title)s</strong> deleted succesfully")
    permission_required = "news.delete_newsitem"
    permission_denied_message = _("You do not have sufficient access rights to delete <strong>%(title)s</strong>")

    def get_success_message(self, cleaned_data: dict[str, str]) -> str:
        return self.success_message % dict(cleaned_data, title=self.object.title)

    def get_permission_denied_message(self) -> str:
        return self.permission_denied_message % dict(title=self.get_object().title)

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=self.success_url)


class NewsPreviewView(PermissionRequiredMixin, DetailView):
    model = NewsItem
    permission_required = "news.view_newsitem"
    permission_denied_message = _("You do not have sufficient access rights to view <strong>%(title)s</strong>")

    def get_permission_denied_message(self) -> str:
        return self.permission_denied_message % dict(title=self.get_object().title)

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.error(self.request, self.get_permission_denied_message())
        return HttpResponseRedirect(redirect_to=reverse_lazy("clubmanager_admin:news:news_index"))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(NewsPreviewView, self).get_context_data(**kwargs)
        context["pictures"] = self.object.pictures.filter(main_picture=False)

        return context


@permission_required("news.release_newsitem")
def release_newsitem(request, pk: int) -> HttpResponse:
    news_item = NewsItem.objects.get(pk=pk)
    news_item.status = NewsItem.StatusChoices.RELEASED
    news_item.save(update_fields=["status"])

    messages.success(request, _("News item <strong>%(name)s</strong> succesfully released" % ({"name": news_item.title})))

    return HttpResponseRedirect(reverse_lazy("clubmanager_admin:news:news_index"))


@permission_required("news.change_newsitem", fn=objectgetter(NewsItem, "pk"))
def update_status_newsitem(request, pk: int, status: str) -> HttpResponse:
    news_item = NewsItem.objects.get(pk=pk)

    news_item.status = NewsItem.StatusChoices.DRAFT
    if status == "in_review":
        news_item.status = NewsItem.StatusChoices.IN_REVIEW

    news_item.save(update_fields=["status"])

    messages.success(request, _("News item <strong>%(name)s</strong> succesfully changed" % ({"name": news_item.title})))

    return HttpResponseRedirect(reverse_lazy("clubmanager_admin:news:news_index"))
