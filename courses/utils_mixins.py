from django.views.generic.base import ContextMixin


class CourseIDMixin(ContextMixin):
    """
    This is for other Classes to inherit so that they can all have the section id needed
    to link back to the previous section's page. I use this for the Create/Update/List forms.
    """



    def get_context_data(self, **kwargs):
        context = super(CourseIDMixin, self).get_context_data(**kwargs)
        course_pk = self.kwargs['course']
        context['current_course_pk'] = course_pk
        print(context)
        return context
