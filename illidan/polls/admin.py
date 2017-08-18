from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    # fields = ['pub_date', 'question_text']
    fieldsets = [
        (None,  {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]

    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']

    search_fields = ['question_text']

    inlines = [ChoiceInline]


# register Question and Choice to admin dashboard.
admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)