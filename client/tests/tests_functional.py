from datetime import date, timedelta

from model_mommy import mommy

from commons.test import CustomAPITestCase


class TestClientBookAPI(CustomAPITestCase):

    def setUp(self):
        self.path = '/v1/clients/{}/books'

    def _create_book_fixtures(self):
        mommy.make('Book', title="Chapeuzinho Vermelho", id=1)
        mommy.make('Book', title="Branca de Neve", id=2)
        mommy.make('Book', title="A Cabana", id=3)
        mommy.make('Book', title="O azul do mar", id=4)

    def _create_client_fixtures(self):
        mommy.make('Client', name="Giovana", id=1)
        mommy.make('Client', name="Paula", id=2)

    def _create_lending_book_fixtures(self):
        mommy.make('LendingBook', book_id=1, client_id=1, date_to_return=(date.today() + timedelta(days=10)))
        mommy.make('LendingBook', book_id=2, client_id=1, date_to_return=(date.today() + timedelta(days=5)))
        mommy.make('LendingBook', book_id=3, client_id=2, date_to_return=(date.today() + timedelta(days=2)))

    def test_get_books_by_client__success(self):
        self._create_book_fixtures()
        self._create_client_fixtures()
        self._create_lending_book_fixtures()

        client_id = 1
        url = self.path.format(client_id)
        response = self.client.get(url)

        obtained_data = response.data

        self.assertEqual(2, len(obtained_data))

    def test_get_book_with_one_day_delayed__success(self):
        days = -1
        obtained_data = self.get_books_with_delayed_of(days)
        self.assertEqual(1, len(obtained_data))
        self.assertEqual(1, obtained_data[0]['delayed_days'])
        self.assertEqual(3, obtained_data[0]['fine'])
        self.assertEqual(0.2, float(obtained_data[0]['rates']))

    def test_get_book_with_four_days_delayed__success(self):
        days = -4
        obtained_data = self.get_books_with_delayed_of(days)
        self.assertEqual(1, len(obtained_data))
        self.assertEqual(4, obtained_data[0]['delayed_days'])
        self.assertEqual(5, obtained_data[0]['fine'])
        self.assertEqual(0.4, float(obtained_data[0]['rates']))

    def test_get_book_with_six_days_delayed__success(self):
        days = -6
        obtained_data = self.get_books_with_delayed_of(days)
        self.assertEqual(1, len(obtained_data))
        self.assertEqual(6, obtained_data[0]['delayed_days'])
        self.assertEqual(7, obtained_data[0]['fine'])
        self.assertEqual(0.6, float(obtained_data[0]['rates']))

    def test_get_book_without_days_delayed__success(self):
        days = 0
        obtained_data = self.get_books_with_delayed_of(days)
        self.assertEqual(1, len(obtained_data))
        self.assertEqual(0, obtained_data[0]['delayed_days'])
        self.assertEqual(0, obtained_data[0]['fine'])
        self.assertEqual(0, float(obtained_data[0]['rates']))

    def get_books_with_delayed_of(self, days):
        self._create_book_fixtures()
        self._create_client_fixtures()
        mommy.make('LendingBook', book_id=3, client_id=1, date_to_return=(date.today() + timedelta(days=days)))

        client_id = 1
        url = self.path.format(client_id)
        response = self.client.get(url)

        return response.data
