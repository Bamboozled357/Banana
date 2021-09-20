from django.urls import path, include
from rest_framework.routers import SimpleRouter

from main.views import (PublicationViewSet,
                        CommentViewSet)

# Первый способ привязки с урлам:
# urlpatterns = [
#     path('publications/', PublicationsListView.as_view(), name='publications-list'),
#     path('publications/<int:pk>', PublicationDetailsView.as_view(), name='publication-details'),
#     path('publications/create/', CreatePublicationView.as_view(), name='create-publication'),
#     path('publications/delete/<int:pk>', DeletePublicationView.as_view(), name='delete-publication'),
#     path('publications/update/<int:pk>/', UpdatePublicationView.as_view(), name='update-publication')
# ]

# Второй способ привязки с урлам:
# urlpatterns = [
#     path('publications/', PublicationViewSet.as_view(
#         {'get': 'list'}), name='publications-list'),
#     path('publications/<int:pk>', PublicationViewSet.as_view(
#         {'get': 'retrieve'}
#     ), name='publication-details'),
#     path('publications/create/', PublicationViewSet.as_view(
#         {'post': 'create'}
#     ), name='create-publication'),
#     path('publications/delete/<int:pk>', PublicationViewSet.as_view(
#         {'delete': 'destroy'}
#     ), name='delete-publication'),
#     path('publications/update/<int:pk>/', PublicationViewSet.as_view(
#         {'put': 'update', 'patch': 'partial_update'}
#     ), name='update-publication')
# ]

# четвёртый способ приявязки к урлам:
router = SimpleRouter()
router.register('publications', PublicationViewSet, 'publications')
router.register('comments', CommentViewSet, 'comments')

urlpatterns = [
    path('', include(router.urls))
]

# третий способ привязки к урлам:
# urlpatterns = [
#     path('publications/', PublicationViewSet.as_view(
#         {'get': 'list',
#          'post': 'create'}),
#          name='publications-list'),
#     path('publications/<int:pk>/', PublicationViewSet.as_view(
#         {'get': 'retrieve',
#          'put': 'update',
#          'patch': 'partial_update',
#          'delete': 'destroy'}
#     ), name='publication-details'),
#     path('comments/', CreateCommentView.as_view()),
#     path('comments/update/<int:pk>', UpdateCommentView.as_view()),
#     path('comments/delete/<int:pk>/', DeleteCommentView.as_view())
# ]