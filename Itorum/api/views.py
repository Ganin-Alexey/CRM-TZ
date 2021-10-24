import base64
import json
from datetime import timedelta, date
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib import auth
from .models import Order, Customer
from django.core import serializers


class Login(View):
    """ Вход в аккаунт, если пользователь авторизирован уже, то редирект"""

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('ordersList')
        return render(request, 'loginUI.html')

    def post(self, request):
        if 'login' in request.POST and 'password' in request.POST:
            login = request.POST['login']
            password = request.POST['password']
            user = auth.authenticate(username=login, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return redirect('ordersList')
        return render(request, 'loginUI.html',
                      context={'error': 'Проверьте корректность введенных данных!', 'status': 401})


class Logout(LoginRequiredMixin, View):
    """ Выход в аккаунта, не авторизирован, то редирект на форму со входом"""
    login_url = 'login'

    def get(self, request):
        auth.logout(request)
        return redirect('login')


class GetListOfOrders(LoginRequiredMixin, View):
    """ Получаем таблицу с заказами, в которой можно создавать или удалять записи """
    login_url = 'login'

    def get(self, request):
        orders = Order.objects.all()
        customers = Customer.objects.all()
        return render(request, 'list_of_orders.html', context={'orders': orders, 'customers': customers})


class DeleteOrder(LoginRequiredMixin, View):
    """ Реализуем удаление заказа через API """
    login_url = 'login'

    def delete(self, request, order_id):
        get_object_or_404(Order, id=order_id).delete()
        return JsonResponse({'status': 200})


class AddOrder(LoginRequiredMixin, View):
    """ Реализуем создание нового заказа через API """
    login_url = 'login'

    def post(self, request):
        if 'customer' in request.POST and 'sum' in request.POST:
            if not request.POST['sum'].isdigit():
                return JsonResponse({'status': 401})
            user = get_object_or_404(Customer, id=request.POST['customer'])
            obj = Order(user=user, total=request.POST['sum'])
            obj.save()
            return JsonResponse({'id': obj.pk, 'total': obj.total, 'customer': obj.user.name, 'date': obj.created_at})
        else:
            return JsonResponse({'status': 401})


class FreeListOfOrders(View):
    """ Получаем таблицу с заказами за последний месяц, с фильтрацией по неделям, в режиме просмотра """

    def get(self, request, week=1):
        # Формируем выборку из последних 4-x недель и считаем итог за выбранную неделю
        total_sum_for_week = 0
        list_of_customers_for_week = []
        weeks_date_list = []
        for num_week in range(1, 5, 1):
            startdate = date.today() - timedelta(weeks=num_week) + timedelta(days=1)
            enddate = date.today() - timedelta(weeks=num_week - 1)
            # Если выбрана наша неделя, то считаем итоги
            if week == num_week:
                orders_for_week = Order.objects.filter(created_at__range=[startdate, enddate + timedelta(days=1)])
                total_sum_for_week = orders_for_week.aggregate(Sum('total'))['total__sum']
                for order in orders_for_week:
                    list_of_customers_for_week.append(order.user.name)
            weeks_date_list.append(str(startdate) + ' - ' + str(enddate))

        # Словарь с данными каждого дня
        days_dict = {}
        for day in reversed(range(0, 7)):
            startdate = date.today() - timedelta(weeks=week - 1) - timedelta(days=day)
            enddate = date.today() - timedelta(weeks=week - 1) - timedelta(days=day - 1)
            orders_for_day = Order.objects.filter(created_at__range=[startdate, enddate])
            list_of_customers = []
            for order in orders_for_day:
                list_of_customers.append(order.user.name)
            days_dict.update({str(startdate): {'customers': '; '.join(list(set(list_of_customers))),
                                               'total_sum': orders_for_day.aggregate(Sum('total'))['total__sum']}})

        if not request.is_ajax():
            return render(request, 'free_list_of_orders.html',
                          context={'days_dict': days_dict, 'weeks_date_list': weeks_date_list,
                                   'list_of_customers_for_week': '; '.join(list(set(list_of_customers_for_week))),
                                   'total_sum_for_week': total_sum_for_week})

        days_dict.update({'total_sum_for_week': total_sum_for_week,
                          'list_of_customers_for_week': '; '.join(list(set(list_of_customers_for_week)))})
        return JsonResponse(json.dumps(days_dict), safe=False)


class GetAllOrders(View):
    """ Реализуем возврат всех заказов, если пройдена Basic-аутентификация """

    def get(self, request):
        if 'HTTP_AUTHORIZATION' in request.META:
            authen = request.META['HTTP_AUTHORIZATION'].split()
            if len(authen) == 2:
                if authen[0].lower() == "basic":
                    uname, passwd = base64.b64decode(authen[1]).decode("utf-8").split(':')
                    user = auth.authenticate(username=uname, password=passwd)
                    if user is not None and user.is_active:
                        orders = serializers.serialize("json", Order.objects.all())
                        return JsonResponse(orders, safe=False)
        response = HttpResponse()
        response.status_code = 401
        response['WWW-Authenticate'] = 'Basic realm="%s"' % "Basci Auth Protected"
        return response
