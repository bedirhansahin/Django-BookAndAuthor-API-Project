from books.api.serializers import (
    AuthorDetailSerializer,
    AuthorSerializer,
    CategorySerializer,
    BookSerializer,
    BookDetailSerializer)
from books.models import Author, Book, Category

from rest_framework import authentication, permissions, viewsets, mixins

from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiTypes


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(
            user=self.request.user
        ).order_by('id').distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorDetailSerializer
    queryset = Author.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(
            user=self.request.user
        ).order_by('id').distinct()

    def get_serializer_class(self):
        if self.action == 'list':
            return AuthorSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'categories',
                OpenApiTypes.STR,
                description='Comma separated list of tag IDs to filter',
            ),
        ]
    )
)
class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookDetailSerializer
    queryset = Book.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def _params_to_ints(self, qs):
        """Convert a list of string to integer"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        categories = self.request.query_params.get('categories')
        queryset = self.queryset
        if categories:
            categories_ids = self._params_to_ints(categories)
            queryset = queryset.filter(categories__id__in=categories_ids)

        return queryset.all().order_by('id').distinct()

    def get_serializer_class(self):
        if self.action == 'list':
            return BookSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




# @extend_schema_view(
#     list=extend_schema(
#         parameters=[
#             OpenApiParameter(
#                 'assigned_only',
#                 OpenApiTypes.INT, enum=[0, 1],
#                 description='Filter by items assigned to recipes.'
#             )
#         ]
#     )
# )
# class BaseBookAttributesViewSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet,):
#     """Base Viewset for another viewsets"""
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         """Filter queryset to authenticated user."""
#         assigned_only = bool(
#             int(self.request.query_params.get('assigned_only', 0))
#         )
#         queryset = self.queryset
#         if assigned_only:
#             queryset = queryset.filter(book__isnull=False)

#         return queryset.filter(user=self.request.user).order_by('-name').distinct()
