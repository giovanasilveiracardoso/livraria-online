from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Book, LendingBook, Reserve, Publisher, Author
from .services import BookReserveService

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publisher)


class LendingBookAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service_reserve = BookReserveService()

    def clean(self):
        try:
            self.service_reserve.check_if_book_is_reserved(self.cleaned_data['book'].id)
        except Exception as e:
            raise ValidationError(e)


@admin.register(LendingBook)
class LendingBookAdmin(admin.ModelAdmin):
    form = LendingBookAdminForm
    list_display = ("book", "client")


@admin.register(Reserve)
class ReserveBookAdmin(admin.ModelAdmin):
    list_display = ("book", "client")
