from django.db.models import Model


def bulk_get_or_create(model: Model, values: list[dict], **kwargs):
    existing_values = []
    values_to_create = []

    for value in values:
        value.update(**kwargs)

        values_found = model.objects.filter(**value)
        if values_found:
            existing_values.extend(values_found)
        else:
            values_to_create.append(model(**value))

    return model.objects.bulk_create(values_to_create) + existing_values
