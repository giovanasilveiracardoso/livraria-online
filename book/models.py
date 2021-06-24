from enum import Enum

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class BookStatus(Enum):
    AVAILABLE = (0, 'Disponível')
    BORROWED = (1, 'Emprestado')

    def __init__(self, index, status_name):
        self.id = index
        self.status_name = status_name


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    synopsis = models.TextField(null=True, blank=True)
    author = models.ForeignKey('book.Author', on_delete=models.CASCADE, null=True, blank=True)
    isbn = models.CharField(max_length=13, null=True, blank=True)
    publisher = models.ForeignKey('book.Publisher', on_delete=models.CASCADE, null=True, blank=True)
    edition_year = models.IntegerField(null=True, blank=True)
    edition = models.IntegerField(null=True, blank=True)
    language = models.CharField(max_length=100, null=True, blank=True)
    number_of_pages = models.IntegerField(null=True, blank=True)
    country_of_origin = models.CharField(max_length=100, null=True, blank=True)
    acquisition_date = models.DateField(null=True, blank=True)
    status = models.IntegerField(default=BookStatus.AVAILABLE.id, editable=False,
                                 choices=[(tag.id, tag.status_name) for tag in BookStatus])

    class Meta:
        db_table = 'book'

    def __str__(self):
        return self.title


class Reserve(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey('book.Book', on_delete=models.CASCADE)
    client = models.ForeignKey('client.Client', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'author'

    def __str__(self):
        return self.name


class Publisher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'publisher'

    def __str__(self):
        return self.name


class LendingBook(models.Model):
    book = models.ForeignKey('book.Book', on_delete=models.CASCADE)
    client = models.ForeignKey('client.Client', on_delete=models.CASCADE)
    date_to_return = models.DateField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'lending_book'

    def save(self, *args, **kwargs):
        book = Book(id=self.book_id, status=BookStatus.BORROWED.id)
        book.save(update_fields=['status'])

        super(LendingBook, self).save(*args, **kwargs)


@receiver(post_delete, sender=Reserve)
@receiver(post_delete, sender=LendingBook)
def delete_hook(sender, instance, **kwargs):
    book = Book(id=instance.book_id, status=BookStatus.AVAILABLE.id)
    book.save(update_fields=['status'])
