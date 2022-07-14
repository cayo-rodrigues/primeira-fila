from django.db.models import Model


def bulk_get_or_create(
    model: Model,
    values: list[dict],
    nested_values: list[tuple[str, Model]] = None,
    **kwargs
) -> list:
    existing_values = []
    values_to_create = []

    for value in values:
        value.update(**kwargs)

        if nested_values:
            for nested_key, nested_model in nested_values:
                value.update(
                    **{
                        nested_key: nested_model.objects.get_or_create(
                            **value[nested_key]
                        )[0],
                    }
                )

        values_found = model.objects.filter(**value)
        if values_found:
            existing_values.extend(values_found)
        else:
            values_to_create.append(model(**value))

    return model.objects.bulk_create(values_to_create) + existing_values


def normalize_text(
    text: str,
    is_title: bool = False,
    join_by: str = "",
    split_by: str = None,
    is_lower: bool = False,
) -> str:
    """
    Normalizes the given string, striping off leading and trailing whitespaces.
    You can pass parameters to specify additional normalization steps.
    - is_title: Turns The String Into A Title Case String.
    - join_by: A string to be the separator of words in a sentence.
    - splt_by: turns the stirng into a list, spliting it by this parameter
    - is_lower: turns the string into a lower case string.
    """
    text = text.strip()

    if is_title:
        text = text.title()
    elif is_lower:
        text = text.lower()

    if join_by:
        text = join_by.join(text.split(split_by))
    if split_by:
        text = text.split(split_by)

    return text
