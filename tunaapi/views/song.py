from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers, status
from tunaapi.models import Song, Artist, Genre, SongGenre


class SongView(ViewSet):
    """Tuna API songs view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single song

        Returns:
            Response -- JSON serialized song
        """

        try:
            song = Song.objects.get(pk=pk)
            serializer = SongSerializer(song)
            return Response(serializer.data)
        except Song.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all songs

        Returns:
            Response -- JSON serialized list of songs
        """
        songs = Song.objects.all()

        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations
        
        Returns
            Response -- JSON serialized song instance
        """
        artist = Artist.objects.get(pk=request.data["artistId"])

        song = Song.objects.create(
            artist_id=artist,
            title=request.data["title"],
            album=request.data["album"],
            length=request.data["length"]
        )
        serializer = SongSerializer(song)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for an song

        Returns:
            Response -- Empty body with 204 status code
        """

        song = Song.objects.get(pk=pk)
        song.title = request.data["title"]
        song.album = request.data["album"]
        song.length = request.data["length"]
        song.artist_id = Artist.objects.get(pk=request.data["artistId"])

        song.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE requests for single song
        
        Returns:
            Response -- Empty body with 204 status code
        """
        song = Song.objects.get(pk=pk)
        song.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def addgenre(self, request, pk):
        """Post request for a user to add a genre to a song"""

        genre = Genre.objects.get(pk=pk)
        song = Song.objects.get(pk=pk)
        songgenre = SongGenre.objects.create(
            genre_id=genre,
            song_id=song
        )
        return Response({'message': 'Genre added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def removegenre(self, request, pk):
        """Delete request for a user to remove a genre from a song"""

        genre = Genre.objects.get(pk=pk)
        song = Song.objects.get(pk=pk)
        songgenre = SongGenre.objects.create(
            genre_id=genre,
            song_id=song
        )
        songgenre.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class SongGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongGenre
        fields = ( 'genre_id', )
        depth = 1
class SongSerializer(serializers.ModelSerializer):
    """JSON serializer for songs
    """
    genres = SongGenreSerializer(many=True, read_only=True)
    class Meta:
        model = Song
        fields = ('id', 'title', 'artist_id', 'album', 'length', 'genres')
        depth = 1
