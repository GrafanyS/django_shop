import logging
import datetime

from django.http import HttpResponse
from django.shortcuts import render

from shop_app import admin
# from django.shortcuts import render

from shop_app.models import Client, Order, Goods

logger = logging.getLogger(__name__)


def get_clients(request):
    clients = Client.objects.all()
    context = '\n'.join(str(client) for client in clients)
    logger.info(f'context: {context}')
    return HttpResponse(context)


def get_goods(request):
    goods = Goods.objects.all()
    context = '\n'.join(str(g) for g in goods)
    logger.info(f'context: {context}')
    return HttpResponse(context)


def get_orders(request):
    orders = Order.objects.all()
    context = '\n'.join(str(order) for order in orders)
    logger.info(f'context: {context}')
    return HttpResponse(context)


def get_orders_by_client_id(request, client_id: int):
    orders = Order.objects.filter(client_id=client_id)
    if orders:
        context = '\n'.join(str(order) for order in orders)
    else:
        context = f'У пользователя с id: {client_id} нет заказов'
    logger.info(f'context: {context}')
    return HttpResponse(context)


def delete_client(request, client_id: int):
    client = Client.objects.filter(pk=client_id)
    if client:
        client.delete()
        logger.info(f'Пользователь удален')
        return HttpResponse('Пользователь удален')
    else:
        logger.info(f'Пользователь не найден')
        return HttpResponse('Пользователь не найден')


def delete_goods(request, goods_id: int):
    goods = Goods.objects.filter(pk=goods_id)
    if goods:
        goods.delete()
        logger.info(f'Товар удален')
        return HttpResponse('Товар удален')
    else:
        logger.info(f'Товар не найден')
        return HttpResponse('Товар не найден')


def delete_order(request, order_id: int):
    order = Order.objects.filter(pk=order_id)
    if order:
        order.delete()
        logger.info(f'Заказ удален')
        return HttpResponse('Заказ удален')
    else:
        logger.info(f'Заказ не найден')
        return HttpResponse('Заказ не найден')


def edit_client_name(request, client_id: int, name: str):
    client = Client.objects.filter(pk=client_id).first()
    if client:
        client.name = name
        client.save()
        logger.info(f'Имя клиента изменено')
        return HttpResponse('Имя клиента изменено')
    else:
        logger.info(f'Клиент не найден')
        return HttpResponse('Клиент не найден')


def edit_goods_price(request, goods_id: int, price: int):
    goods = Goods.objects.filter(pk=goods_id).first()
    if goods:
        goods.price = price
        goods.save()
        logger.info(f'Цена товара изменена')
        return HttpResponse('Цена товара изменена')
    else:
        logger.info(f'Товар не найден')
        return HttpResponse('Товар не найден')


def edit_order_goods_id(request, order_id: int, goods_id: int):
    order = Order.objects.filter(pk=order_id).first()
    goods = Goods.objects.filter(pk=goods_id).first()
    if order:
        order.goods_id = goods
        order.save()
        return HttpResponse('Товар в заказе изменен')
    else:
        return HttpResponse('Такой заказ не найден')


def test(request):
    context = {
        'title': 'Тестовая страница',
        'pk': Client.objects.order_by('name')
    }
    logger.info(f'context: {context}')
    return render(request, 'shop_app/test.html', context)


def get_client_goods(request, client_id: int):
    COUNT_DAYS = 7
    start = datetime.date.today() - datetime.timedelta(days=COUNT_DAYS)
    client = Client.objects.get(id=client_id)
    orders = Order.objects.filter(client_id=client_id, create_at__gte=start)
    context = {
        'title': 'Тестовая страница',
        'count_days': COUNT_DAYS,
        'client': client,
        'orders': orders
    }
    logger.info(f'context: {context}')
    return render(request, 'shop_app/client_goods.html', context)


def client_goods(request):
    context = {
        'title': 'Тестовая страница',
        'text': 'http://127.0.0.1:8000/get_client_goods'
    }
    return render(request, 'shop_app/test.html', context=context)


def main(request):
    context = {
        'title': 'Главная страница',
        'pk': Client.objects.order_by('name')
    }
    logger.info(f'context: {context}')
    return render(request, 'shop_app/index.html', context)


def get_catalog(request, pk=None):
    if pk:
        book_list = Client.objects.all().filter(cat_fk=pk)
        topic = Goods.objects.filter(id=pk)
    else:
        book_list = Client.objects.all()
        topic = None

    cat_menu = [(c.id, c.name) for c in Client.objects.order_by('name')]
    """ Сначала хотел: {c.id: c.name for c in BookCategory.objects.order_by('name')}, Но почему-то не заработало в 
    шаблоне. {{ cat_menu.m }} где m - ключ словаря cat_menu, возвратило ничего. """

    content = {
        'books': book_list,
        'topic_name': topic[0].name if topic else None,
        'cat_menu': cat_menu
    }
    return render(request, 'shop_app/catalog.html', context=content)


def contacts(request):
    title = "Контакты"
    clients = Client.objects.all()
    context = {
        'title': title,
        'clients': clients,
    }
    logger.info(f'context: {context}')
    return render(request, 'shop_app/contacts.html', context)




