from django.http import Http404
from django.views.generic.base import TemplateView

from mysite.core.models import AboutPage, HomePage


class HomeView(TemplateView):
    """
    Home Page
    """

    template_name = "core/home_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            # There is only one item in the table, so we can just get it
            context["home_page"] = HomePage.objects.get()
        except HomePage.DoesNotExist:
            raise Http404("Sorry, we couldn't find the page you're looking for")

        return context


class AboutView(TemplateView):
    """
    About Page
    """

    template_name = "core/about_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            # There is only one item in the table, so we can just get it
            context["about_page"] = AboutPage.objects.get()
        except AboutPage.DoesNotExist:
            raise Http404("Sorry, we couldn't find the page you're looking for")

        return context
