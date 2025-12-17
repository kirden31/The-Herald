__all__ = ('HomeView',)

import django.shortcuts


class HomeView(django.views.View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        return django.shortcuts.render(request, self.template_name)
