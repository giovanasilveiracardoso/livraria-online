from model_mommy import mommy
from rest_framework import status

from book.models import Reserve, BookStatus
from commons.test import CustomAPITestCase


class TestBookAPI(CustomAPITestCase):

    def setUp(self):
        self.path = '/v1/books/'

    def _create_book_fixtures(self):
        mommy.make('Book', title="Chapeuzinho Vermelho")
        mommy.make('Book', title="Branca de Neve")

    def test_get__success(self):
        self._create_book_fixtures()

        response = self.client.get(self.path)

        obtained_data = response.data

        self.assertTrue(len(obtained_data))
        self.assertEqual(2, len(obtained_data))


class TestBookReserveAPI(CustomAPITestCase):

    def setUp(self):
        self.path = '/v1/books/{}/reserve'

    def _create_book_fixtures(self):
        mommy.make('Book', title="Chapeuzinho Vermelho", id=1)
        mommy.make('Book', title="Branca de Neve", id=2)

    def _create_client_fixtures(self):
        mommy.make('Client', name="Giovana", id=1)
        mommy.make('Client', name="Paula", id=2)

    def test_post_reserve_book__success(self):
        self._create_book_fixtures()
        self._create_client_fixtures()

        client_id = 1
        data = {
            "client": client_id
        }

        book_id = 1
        url = self.path.format(book_id)
        response = self.send_post(path=url, data=data)

        self.assertResponse(response, status.HTTP_200_OK, 'Reserva registrada!')

        reserve = Reserve.objects.filter(client_id=client_id, book_id=book_id)
        self.assertEqual(1, len(reserve))

    def test_post_reserve_book__book_already_borrowed__error(self):
        book_id = 1
        mommy.make('Book', title="Chapeuzinho Vermelho", id=1, status=BookStatus.BORROWED.id)
        self._create_client_fixtures()

        client_id = 1
        data = {
            "client": client_id
        }

        url = self.path.format(book_id)
        response = self.send_post(path=url, data=data)

        self.assertResponse(response, status.HTTP_406_NOT_ACCEPTABLE, 'This book is unavailable!')

        reserve = Reserve.objects.filter(client_id=client_id, book_id=book_id)
        self.assertEqual(0, len(reserve))
