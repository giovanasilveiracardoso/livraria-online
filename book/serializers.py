from rest_framework import serializers

from .models import Book, Author, Publisher


class AuthorResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = '__all__'


class PublisherResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publisher
        fields = '__all__'


class BookResponseSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    author = AuthorResponseSerializer()
    publisher = PublisherResponseSerializer()

    class Meta:
        model = Book
        fields = '__all__'


class BookDtoResponseSerializer(serializers.Serializer):
    title = serializers.CharField()
    delayed_days = serializers.IntegerField()
    rates = serializers.DecimalField(max_digits=15, decimal_places=1)
    fine = serializers.IntegerField()


class ReserveInputSerializer(serializers.Serializer):

    client = serializers.IntegerField(help_text="Client Id", required=True)
