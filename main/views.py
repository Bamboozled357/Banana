from django_filters import rest_framework as filters
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework import filters as rest_filters

from main.models import Publication, Comment
from main.permissions import IsAuthorOrIsAdmin, IsAuthor
from main.serializers import (PublicationListSerializer,
                              PublicationDetailSerializer,
                              CreatePublicationSerializer,
                              CommentSerializer)


class PublicationFilter(filters.FilterSet):
    created_at = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Publication
        fields = ('status', 'created_at')


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = CreatePublicationSerializer
    permission_classes = [IsAuthorOrIsAdmin, ]
    filter_backends = [filters.DjangoFilterBackend,
                       rest_filters.SearchFilter,
                       rest_filters.OrderingFilter]
    filterset_class = PublicationFilter
    search_fields = ['title', 'text']
    ordering_fields = ['created_at', 'title']

    def get_serializer_class(self):
        if self.action == 'list':
            return PublicationListSerializer
        elif self.action == 'retrieve':
            return PublicationDetailSerializer
        return CreatePublicationSerializer


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthor()]