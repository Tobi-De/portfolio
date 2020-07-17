from django.http import Http404


# TODO replace the raise Htpp404 by a page that tell the user the post is not published yet


class PostPublishedRequiredMixin:
    def get_object(self, queryset=None):
        obj = super(PostPublishedRequiredMixin, self).get_object(queryset=queryset)
        if not obj.is_published and not self.request.user.is_superuser:
            raise Http404
        return obj
