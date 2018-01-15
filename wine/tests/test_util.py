from wine.models import Category, SubCategory, Producer, Wine


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
