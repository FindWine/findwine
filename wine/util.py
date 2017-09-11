from django.utils.text import slugify


def generate_slug(wine_vintage):
    """
    Slug format should be: [producer name]-[wine name]-[winevintage year]
    """
    return generate_slug_from_parts(
        producer_name=wine_vintage.wine.producer.name,
        wine_name=slugify(wine_vintage.wine.name),
        year=wine_vintage.year,
    )


def generate_slug_from_parts(producer_name, wine_name, year):
    producer_name = producer_name or 'Unknown Producer'
    wine_name = wine_name or 'Unknown Wine'
    return '{producer}-{wine}-{year}'.format(
        producer=slugify(producer_name),
        wine=slugify(wine_name),
        year=year,
    )

