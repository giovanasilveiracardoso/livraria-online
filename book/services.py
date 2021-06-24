from datetime import date

from rest_framework.exceptions import NotAcceptable

from client.models import Client
from commons.decorators import validate_requirements, validate_existence
from .models import Book, Reserve, BookStatus, LendingBook


class BookService:

    def get_all(self):
        return Book.objects.all()

    @validate_existence((Client, 'client'), is_critical=True)
    def find_books_by_client(self, params):
        query = LendingBook.objects.filter(client_id=params['client'])

        books_dto = []
        for lending_book in query:
            delayed_days, fine, rates = self.get_rates_fine_and_delayed_days(lending_book.date_to_return)

            book_dto = {
                "title": lending_book.book.title,
                "delayed_days": delayed_days,
                "fine": fine,
                "rates": rates
            }

            books_dto.append(book_dto)

        return books_dto

    def get_rates_fine_and_delayed_days(self, date_to_return):
        delayed_days = (date.today() - date_to_return).days
        rates = 0
        fine = 0
        if 0 < delayed_days <= 3:
            rates = 0.2
            fine = 3
        elif 3 < delayed_days <= 5:
            rates = 0.4
            fine = 5
        elif delayed_days > 5:
            rates = 0.6
            fine = 7
        else:
            delayed_days = 0

        return delayed_days, fine, rates


class BookReserveService:

    def __init__(self):
        super().__init__()
        self.TIME_LIMIT_RESERVE = 3

    @validate_requirements('book', 'client')
    @validate_existence((Book, 'book'), (Client, 'client'), is_critical=True)
    def insert(self, params):
        book_id = params['book']
        book = Book.objects.get(id=book_id)

        if book.status == BookStatus.BORROWED.id:
            raise NotAcceptable(detail='This book is unavailable!')

        self.check_if_book_is_reserved(book_id)

        reserve = Reserve(book_id=book_id, client_id=params['client'])
        reserve.save()

        return reserve

    def check_if_book_is_reserved(self, book_id):
        reserve_actual = Reserve.objects.filter(book_id=book_id).first()
        if reserve_actual:
            days_reserved = (date.today() - reserve_actual.date).days

            if days_reserved > self.TIME_LIMIT_RESERVE:
                reserve_actual.delete()
            else:
                raise NotAcceptable(detail='This book already is reserved')
