from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User as DjUser


class Airport(models.Model):
    code = models.CharField(verbose_name='Код', max_length=20)
    name = models.CharField(verbose_name='Название', max_length=60)


class Profile(models.Model):
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # location = models.ForeignKey(Airport, on_delete=models.CASCADE, verbose_name='Из', related_name='location',
    #                                  null=True)
    location = models.CharField(verbose_name='Ближайший аэропорт', max_length=30, null=True)

    def __str__(self):
        return f'Профиль {self.user.username}'

    @property
    def username(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


class User(DjUser):
    class Meta:
        proxy = True

    @property
    def profile(self):
        return Profile.objects.get_or_create(user_id=self.id)


class Ticket(models.Model):
    class Meta:
        verbose_name = 'Билет'
        verbose_name_plural = 'Билеты'

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Профиль')
    flights = models.ManyToManyField('Flight', verbose_name='Полет', blank=True)

    num_stops = models.IntegerField('Кол-во пересадок', null=True)

    ad = models.IntegerField('Кол-во взрослых', null=True)
    ch = models.IntegerField('Кол-во детей', null=True)
    inf = models.IntegerField('Кол-во младенцев', null=True)

    date = models.DateField('Дата', null=True, blank=True)
    price = models.DecimalField('Цена', max_digits=9, decimal_places=2, default=0, null=True)
    paid = models.BooleanField('Оплачен', default=False)

    def __str__(self):
        return f'Билет {self.profile.username}'

    pend_flights = []

    @classmethod
    def pend_save(cls, user, flight, ad, ch, inf, date, price):
        pend_ticket = Ticket(profile=user.profile, num_stops=flight['num_stops'], date=date, ad=ad, ch=ch, inf=inf,
                             price=price, paid=False)
        for fl in flight['flights']:
            air_from = Airport.objects.get_or_create(code=fl['from_airport']['code'], name=fl['from_airport']['name'])[
                0]
            air_to = Airport.objects.get_or_create(code=fl['to_airport']['code'], name=fl['to_airport']['name'])[0]

            airline = Airline.objects.get_or_create(code=fl['airline']['code'], name=fl['airline']['name'])[0]

            flight_sup = \
                Flight.objects.get_or_create(from_airport=air_from, to_airport=air_to, airline=airline,
                                             price=fl['price'])[0]
            cls.pend_flights.append(flight_sup)

        cls.pend_instance = pend_ticket

    @classmethod
    def pend_commit(cls):
        if hasattr(cls, 'pend_instance'):
            if cls.pend_instance is not None:
                cls.pend_instance.save(force_insert=True)
                cls.pend_instance.flights.set(cls.pend_flights)
                cls.pend_instance = None

    @classmethod
    def pend_clear(cls):
        cls.pend_instance = None
        cls.pend_flights = []


class Airline(models.Model):
    code = models.CharField(verbose_name='Код', max_length=20)
    name = models.CharField(verbose_name='Название', max_length=60)


class Flight(models.Model):
    class Meta:
        verbose_name = 'Полет'
        verbose_name_plural = 'Полеты'

    # from_air = models.ManyToManyField('Airport', verbose_name='Из', blank=True, related_name='from_air')
    # to_air = models.ManyToManyField('Airport', verbose_name='В', blank=True, related_name='to_air')
    from_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, verbose_name='Из', related_name='from_airport',
                                     null=True)
    to_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, verbose_name='В', related_name='to_airport',
                                   null=True)
    # airline = models.CharField(verbose_name='Авиакомпания', max_length=30)
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, verbose_name='Авиакомпания', null=True)
    price = models.DecimalField('Цена', max_digits=9, decimal_places=2, default=0)
