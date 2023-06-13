from django.http import HttpResponseServerError
from django.db.models import Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models import Artist

class ArtistView(ViewSet):
    """Tuna API artist view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single artist

        Returns:
            Response -- JSON serialized artist
        """
        try:
            artist = Artist.objects.annotate(song_count=Count('songs')).get(pk=pk)
            serializer = ArtistSerializer(artist)
            return Response(serializer.data)
        except Artist.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)


    def list(self, request):
        """Handle GET requests to get all artists

        Returns:
            Response -- JSON serialized list of artists
        """
        artists = Artist.objects.all()

        for artist in artists:
            artist = Artist.objects.annotate(song_count=Count('songs')).get(pk=artist.id)

        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized artist instance
        """

        artist = Artist.objects.create(
            name=request.data["name"],
            age=request.data["age"],
            bio=request.data["bio"],
        )
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a artist

        Returns:
            Response -- Empty body with 204 status code
        """

        artist = Artist.objects.get(pk=pk)
        artist.name = request.data["name"]
        artist.age = request.data["age"]
        artist.bio = request.data["bio"]
        artist.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE requests for single artist
        
        Returns:
            Response -- Empty body with 204 status code
        """
        artist = Artist.objects.get(pk=pk)
        artist.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for artists
    """
    song_count = serializers.IntegerField(default=None)
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio', 'song_count', 'songs')
        depth = 1
