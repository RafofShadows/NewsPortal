from django import template

register = template.Library()


BANNED_WORDS = ['казнь', 'Казнь', 'террор', 'Террор']
@register.filter()
def censor(text):
    if not type(text) is str:
        raise TypeError("Неверный тип переменной. Фильтр censor должен применяться к тексту.")
    for word in BANNED_WORDS:
        if word in text:
            text = text.replace(word, word[0]+'*'*(len(word)-1))
    return text
