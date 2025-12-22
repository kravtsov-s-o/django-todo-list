class TitleContextMixin:
    """
    Adds a page title to the template context.
    """
    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.title:
            context["title"] = self.title

        return context