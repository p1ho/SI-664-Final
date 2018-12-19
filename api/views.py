from meteorite_landings.models import MeteoriteClass, MeteoriteLanding
from api.serializers import MeteoriteClassSerializer
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response

class MeteoriteClassViewSet(viewsets.ModelViewSet):
    queryset = MeteoriteClass.objects.order_by('code')
    serializer_class = MeteoriteClassSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def delete(self, request, pk, format=None):
        meteorite_class = self.get_object(pk)
        self.perform_destroy(self, meteorite_class)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
