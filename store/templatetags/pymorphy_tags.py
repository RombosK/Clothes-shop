# from django import template
# from pymorphy2 import MorphAnalyzer
#
# register = template.Library()
#
#
# @register.filter
# def inflect_to_dative(word):
#     morph = MorphAnalyzer()
#     parsed_word = morph.parse(word)[0]
#     inflected_word = parsed_word.inflect({'datv'}).word
#     return inflected_word.capitalize()


from django import template
from pymorphy2 import MorphAnalyzer

register = template.Library()
morph = MorphAnalyzer()

@register.filter
def format_product_count(count):
    try:
        count = int(count)
    except (ValueError, TypeError):
        return f"{count} товаров"

    # Определяем правильную форму слова "товар"
    if count % 10 == 1 and count % 100 != 11:
        return f"{count} товар найден"
    elif 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 >= 20):
        return f"{count} товара найдено"
    else:
        return f"{count} товаров найдены"
