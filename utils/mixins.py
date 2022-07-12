class SerializerByMethodMixin:
    def get_serializer_class(self):
        return self.serializers.get(self.request.method)
