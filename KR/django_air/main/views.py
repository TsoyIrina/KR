import datetime

from django.contrib.auth import logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, FormView, ListView, DeleteView
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from db import *
from main.dt import DateConverter
from main.forms import LoginUserForm, RegUserForm, UpdateForm
from main.models import Ticket, Profile
from main.serializers import TicketsSerializer, ProfilesSerializer


# открытие главной страницы с проверкой на сохранение билета
def index(request, confirm_ticket=0):
    if confirm_ticket == '1':
        Ticket.pend_commit()
    else:
        Ticket.pend_clear()
    return render(request, 'main/index.html')


# переход на (1) начальный этап "Поиск билетов" для ввода точек отправления и назначения
def search_tick(request):
    air_from = request.GET.get('input_from')
    air_to = request.GET.get('input_to')
    if air_from is not None and air_to is not None:
        return redirect('res', tick_from_slug=air_from, tick_to_slug=air_to)

    air_list = take_airports()
    context = {
        'air_list': air_list
    }
    return render(request, 'tick/find_tick.html', context)


# переход на 3 этап с возможностью указания кол-ва и возраста пассажиров и даты + соответствующие проверки
def who_air_v(request, tick_from_slug, tick_to_slug, id):
    date = request.GET.get('input_date')
    dt = DateConverter()
    adult_count = (request.GET.get('adult_count'))
    child_count = (request.GET.get('child_count'))
    infant_count = (request.GET.get('infant_count'))

    if str(date) < str(datetime.datetime.today()):
        context = {
            'date_error': 'Неверная дата'
        }
        return render(request, 'tick/who.html', context)
    if adult_count is not None:
        if int(adult_count) < 1:
            context = {
                'person_error': 'Взрослых маловато'
            }
            return render(request, 'tick/who.html', context)

        if int(adult_count) < int(infant_count):
            context = {
                'person_error': 'Взрослых маловато'
            }
            return render(request, 'tick/who.html', context)

        else:
            return redirect('ticket', tick_from_slug=tick_from_slug, tick_to_slug=tick_to_slug, id=id,
                            date=dt.to_python(date),
                            ad=int(adult_count), ch=int(child_count),
                            inf=int(infant_count))
    return render(request, 'tick/who.html')


# переход на 2 этап с результатом предыдущего запроса и возможностью выбора подходящего билета
def res_tick(request, tick_from_slug, tick_to_slug, id, date, ad=1, ch=0, inf=0):
    flight = take_flights(tick_from_slug, tick_to_slug, 2)[id]
    price = round(flight['total_price'] * (ad + ch * 0.8 + inf * 0.2), 2)
    context = {
        'flight': flight,
        'date': date,
        'ad': ad,
        'ch': ch,
        'inf': inf,
        'price': price
    }
    Ticket.pend_save(request.user, **context)
    return render(request, 'tick/res_tick.html', context)


# 4 этап окончательный результат, билет
def res(request, tick_from_slug, tick_to_slug):
    id_flight = request.GET.get('input_airline')
    if id_flight is not None:
        return redirect('who', id_flight=id_flight)
    flights = take_flights(tick_from_slug, tick_to_slug, 2)
    context = {
        'flights': flights,
        'from': tick_from_slug,
        'to': tick_to_slug
    }
    return render(request, 'tick/response_airline.html', context)


# форма регистрации
class RegisterUser(CreateView):
    form_class = RegUserForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('log')


# форма авторизации
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'user/login.html'

    def get_success_url(self):
        return reverse_lazy('main')


# выход из уч.записи
def logout_user(request):
    logout(request)
    return redirect('main')


# показ профиля пользователя
class ShowProfile(DetailView):
    model = Profile
    template_name = 'user/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)

        profile = user.profile
        return profile


# изменение данных профиля
class EditProfile(FormView):
    form_class = UpdateForm
    template_name = 'user/edit.html'

    def get_initial(self):
        self.initial['first_name'] = self.request.user.first_name
        self.initial['last_name'] = self.request.user.last_name
        self.initial['email'] = self.request.user.email
        self.initial['location'] = self.request.user.profile.location
        return self.initial

    def get_success_url(self):
        return reverse('profile', kwargs={'username': self.request.user})

    def form_valid(self, form):
        user = self.request.user
        form.save(user, commit=True)
        return super().form_valid(form)

    extra_context = {
        'air_list': take_airports()
    }


# неоплаченные билеты
class ShowTicketUnpaid(ListView):
    model = Ticket
    template_name = 'user/ticket.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        ticket = user.profile.ticket_set.all().filter(paid=False)
        return ticket


# оплаченные билеты
class ShowTicketPaid(ListView):
    model = Ticket
    template_name = 'user/ticket.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        ticket = user.profile.ticket_set.all().filter(paid=True)
        return ticket


# оплата билета
class Payment(UpdateView):
    model = Ticket
    fields = ['paid']
    template_name = 'user/payment.html'

    def get_success_url(self):
        return reverse('tick_paid', kwargs={'username': self.request.user})


# удаление билета
class TicketDeleteView(DeleteView):
    model = Ticket
    template_name = 'user/tick_del.html'

    def get_success_url(self):
        return reverse('tick_unpaid', kwargs={'username': self.request.user})


class TicketsAPIView(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketsSerializer


class ProfilesAPIView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfilesSerializer


class LoginAPIView(APIView):
    http_method_names = ['post']
    permission_classes = [AllowAny]

    def post(self, request):
        errors = {}
        username, password = request.data.get('username', ''), request.data.get('password', '')
        if not username:
            errors['username'] = ['Обязательное поле']
        if not password:
            errors['password'] = ['Обязательное поле']
        if errors:
            return Response(data=errors, status=status.HTTP_400_BAD_REQUEST)
        if not (user := authenticate(username=username, password=password)):
            return Response(data={'non_field': ['Неверные логин и пароль']}, status=status.HTTP_401_UNAUTHORIZED)
        profile = user.profile
        instance = ProfilesSerializer(instance=profile)
        return Response(data=instance.data, status=status.HTTP_200_OK)
