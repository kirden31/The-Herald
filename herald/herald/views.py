__all__ = ('HomeView',)

from django.http import HttpResponse
import django.shortcuts


class HomeView(django.views.View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return django.shortcuts.render(request, self.template_name)
