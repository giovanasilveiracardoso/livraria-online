from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import BookResponseSerializer, ReserveInputSerializer
from .services import BookService, BookReserveService


class BookView(GenericAPIView):

    def __init__(self):
        super().__init__()
        self.service = BookService()

    def get(self, request):
        data = self.service.get_all()
        serialized = BookResponseSerializer(data, many=True)

        return Response(serialized.data)


class BookReserveView(GenericAPIView):
    serializer_class = ReserveInputSerializer

    def __init__(self):
        super().__init__()
        self.service = BookReserveService()

    def post(self, request, book_id):
        params = request.data.copy()
        params['book'] = book_id

        self.service.insert(params)

        result = {'detail': 'Reserva registrada!'}

        return Response(result)
