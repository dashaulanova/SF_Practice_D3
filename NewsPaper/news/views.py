
from django.views.generic import ListView, DetailView # импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
from .models import Post


class PostList(ListView):
    model = Post  # указываем модель, объекты которой мы будем выводить
    template_name = 'news/news.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'news'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон.shortcuts import render
    queryset = model.objects.all().order_by("-time_add")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sorted_list"] = self.queryset
        return context


class PostDetail(DetailView):
    model = Post # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'news/new.html' # название шаблона будет product.html
    context_object_name = 'new' # название объекта
# Create your views here.
