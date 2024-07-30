from store.models import Product
from .models import Category


def menu_links(request):
    """
    Получаем ссылки для всех категорий в базе данных.
    После этого мы можем использовать эти ссылки в шаблонах в любом месте проекта.
    :param request:
    :return: словарь ссылок
    """
    links = Category.objects.all().order_by('category_name')
    count_products_by_category = [len(Product.objects.filter(category=link, is_available=True)) for link in links]
    return dict(links=links, count_products_by_category=count_products_by_category)
