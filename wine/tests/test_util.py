from wine.models import Category, SubCategory


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
