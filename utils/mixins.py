class SerializerByMethodMixin:
    def get_serializer_class(self):
        return self.serializers.get(self.request.method)


class MovieQueryParamsMixin:
    def use_query_params(self):
        age_group = self.request.GET.get("age_group")
        age_group_lte = self.request.GET.get("age_group_lte")
        age_group_gte = self.request.GET.get("age_group_gte")
        distributor = self.request.GET.get("distributor")
        genres = self.request.GET.get("genres")

        if age_group:
            self.queryset = self.queryset.filter(age_group__minimum_age=age_group)
        else:
            if age_group_lte:
                self.queryset = self.queryset.filter(
                    age_group__minimum_age__lte=age_group_lte
                )
            if age_group_gte:
                self.queryset = self.queryset.filter(
                    age_group__minimum_age__gte=age_group_gte
                )

        if distributor:
            self.queryset = self.queryset.filter(
                distributor__name__icontains=distributor.strip()
            )
        if genres:
            self.queryset = self.queryset.filter(genres__name__in=genres.split(","))

        return self.queryset
