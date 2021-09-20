from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from main.models import Publication, Comment
from main.permissions import IsAuthorOrIsAdmin, IsAuthor
from main.serializers import PublicationListSerializer, PublicationDetailSerializer, CreatePublicationSerializer, \
    CommentSerializer


# class PublicationsListCreateView(ListCreateAPIView):
#     queryset = Publication.objects.all()
#     serializer_class = PublicationListSerializer
#
#
# class PublicationDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = Publication.objects.all()
#     serializer_class = PublicationDetailSerializer



# CRUD => CREATE RETRIEVE UPDATE DELETE
#         CREATE READ UPDATE DESTROY
#         POST GET PUT/PATCH DELETE

# CREATE, LIST, RETRIEVE, UPDATE/PARTIAL_UPDATE, DESTROY
# POST,       GET,           PUT/PATCH,          DELETE

# вьюшки можно писать функциями:
# @api_view([GET])
# def piblications_list(request):
#     pubs = Publication.objects.all() # получаем queryset [pub1, pub2, ..]
# # далее эти объекты следует сериализовать. для этого наужно прописать сериалайзер:
#     serializer = PublicationListSerializer(pubs, many=True)  # он берет объект который попадает в него, и приводит в вид,
#     # который будет передан на фронт: {'id': 1, 'title': '...', 'text': '...'}, {}, {} проще говоря он объект класса,
# #     превращает в объект встроенного класса
#     return Response(serializer.data) # возвращает http ответ после подключения в вьюхам

# class PublicationListView(APIView):
#     def get(self, request):
#         pubs = Publication.objects.all()
#         serializer = PublicationListSerializer(pubs,
#                                                many=True)
#         return Response(serializer.data)


# class PublicationsListView(ListAPIView):
#     queryset = Publication.objects.all()
#     serializer_class = PublicationListSerializer
#
#
# class PublicationDetailsView(RetrieveAPIView):
#     queryset = Publication.objects.all()
#     serializer_class = PublicationDetailSerializer
#     # lookup_url_kwarg = 'id'
#
#
# class CreatePublicationView(CreateAPIView):
#     queryset = Publication.objects.all()
#     serializer_class = CreatePublicationSerializer
#
#
# class UpdatePublicationView(UpdateAPIView):
#     queryset = Publication.objects.all()
#     serializer_class = CreatePublicationSerializer
#
#
# class DeletePublicationView(DestroyAPIView):
#     queryset = Publication.objects.all()
#     serializer_class = CreatePublicationSerializer
#
# TODO: Объявления создаются со статусом draft, и только затем автор может поменять на open
# TODO: draft может видеть только автор
class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    # queryset - список объектов модели
    serializer_class = CreatePublicationSerializer
    # класс, которым будут сериализоваться эти объекты
    permission_classes = [IsAuthorOrIsAdmin, ]  #если для разных действий нужны разные permission, то используем так <--
    # проверяет права для действия с объектами через API
    # pagination_class = класс пагинации для данной вьюшки
    # paginate_by = page_size для данной вьюшки

    # def get_permissions(self):
    #     if self.action == 'create': # если действие create то, даёт доступ только авторизованным юзерам
    #         return [IsAuthenticated()]
    #     elif self.action in ['update', 'partial_update', 'destroy']: # если действие одно из трёх, то зададим своё собственное разрешение
    #         return [IsAuthorOrIsAdmin()]
    #     return []


    def get_serializer_class(self):
        if self.action == 'list':
            return PublicationListSerializer
        elif self.action == 'retrieve':
            return PublicationDetailSerializer
        return CreatePublicationSerializer

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     request = self.request
    #     status = request.query_params.get('status')
    #     if status is not None:
    #         queryset = queryset.filter(status=status)
    #     return queryset


# http://127.0.0.1:8000/publications/?status=closed&create_at=...


# TODO: сделать комментарии

class CreateCommentView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'request': self.request}


class UpdateCommentView(UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthor]


class DeleteCommentView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthor]


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



# TODO: пагинация, фильтрация, поиск и документация