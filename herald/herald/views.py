__all__ = ('HomeView',)

import django.shortcuts
import django.views


class HomeView(django.views.View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return django.shortcuts.render(request, self.template_name)
