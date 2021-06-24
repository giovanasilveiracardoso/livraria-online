from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from book.serializers import BookDtoResponseSerializer
from book.services import BookService


class ClientBookView(GenericAPIView):

    def __init__(self):
        super().__init__()
        self.service = BookService()

    def get(self, request, client_id):
        params = request.data.copy()
        params['client'] = client_id

        data = self.service.find_books_by_client(params)
        serialized = BookDtoResponseSerializer(data, many=True)

        return Response(serialized.data)
