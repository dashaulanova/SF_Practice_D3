from django import template

register = template.Library()

@register.filter(name="censor")
def censor(value):
    with open("/Users/home/Downloads/SF_Practice_D3/NewsPaper/news/templatetags/obscene_words.txt", "r") as f:
        value_list = value.split()
        data = f.read().split()
        for i in range(len(value_list)):
            if value_list[i] in data:
                raise ValueError("Замените нецензурную лексику на нормативную")

        return value

        # возвращаемое функцией значение — это то значение, которое подставится к нам в шаблон