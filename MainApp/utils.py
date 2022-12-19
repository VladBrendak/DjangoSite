
navMenu = [ {'title': "Home", 'url_name' : "home"},
            { 'title': "Shop", 'url_name' : "shop"},
            {'title': "Novelties", 'url_name' : "novelties"},]

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['navMenu'] = navMenu
        return context
