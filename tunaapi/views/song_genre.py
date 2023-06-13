from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import SongGenre


class SongGenreView(ViewSet):
    """Tuna API models view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single song genre

        Returns:
            Response -- JSON serialized song genre
        """

        try:
            song_genre = SongGenre.objects.get(pk=pk)
            serializer = SongGenreSerializer(song_genre)
            return Response(serializer.data)
        except SongGenre.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all song genres

        Returns:
            Response -- JSON serialized list of song genres
        """
        song_genres = SongGenre.objects.all()
        serializer = SongGenreSerializer(song_genres, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk):
        """Handle DELETE requests for single song genre
        
        Returns:
            Response -- Empty body with 204 status code
        """
        song_genre = SongGenre.objects.get(pk=pk)
        song_genre.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class SongGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongGenre
        fields = ('id', 'song_id', 'genre')
