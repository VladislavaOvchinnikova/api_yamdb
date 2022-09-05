from rest_framework import mixins, viewsets


class ListCreateDestroyViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """View-класс для операций с данными"""
    pass


class ListCreateRetrieveViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """View-класс для операций с данными"""
    pass
