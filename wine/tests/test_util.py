from wine.models import Category, SubCategory, Producer, Wine, WineVintage


def bootstrap_categories():
    category = bootstrap_category()
    subcategory = bootstrap_subcategory(category)
    return category, subcategory


def bootstrap_category():
    category = Category(name='Red')
    category.save()
    return category


def bootstrap_subcategory(category):
    subcategory = SubCategory(name='Merlot')
    subcategory.save()
    subcategory.category.add(category)
    subcategory.save()
    return subcategory


def get_a_new_wine():
    producer = Producer(name='Warwick')
    producer.save()
    wine = Wine(producer=producer, name='Grey Lady')
    wine.save()
    return wine


def get_a_new_wine_vintage():
    category, subcategory = bootstrap_categories()
    wine = get_a_new_wine()
    return WineVintage.objects.create(wine=wine, year=2017, category=category, sub_category=subcategory)
