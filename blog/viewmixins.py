from django.http import Http404


class PostPublishedRequiredMixin:
    def get_object(self, queryset=None):
        obj = super(PostPublishedRequiredMixin, self).get_object(queryset=queryset)
        if not obj.is_published and not self.request.user.is_superuser:
            raise Http404
        return obj
