from django.utils.text import slugify


def generate_unique_slug(wine_vintage):
    from wine.models import WineVintage
    slug = generate_slug(wine_vintage)
    if WineVintage.objects.filter(slug=slug).count():
        # conflict - find the next available number
        existing_slugs = set(WineVintage.objects.filter(slug__startswith=slug).values_list('slug', flat=True))
        suffix = 2
        candidate_slug = slug
        while candidate_slug in existing_slugs:
            candidate_slug = '{}-{}'.format(slug, suffix)
            suffix += 1
        return candidate_slug
    else:
        return slug


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

