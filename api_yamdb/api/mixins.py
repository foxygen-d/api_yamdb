from rest_framework import mixins, viewsets


class CreateRetrieveDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class RetrieveUpdateViewset(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    pass
