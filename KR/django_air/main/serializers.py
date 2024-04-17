from rest_framework import serializers

from main.models import Ticket, Profile, Flight, User, Airport, Airline


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class ProfilesSerializer(serializers.ModelSerializer):
    user = UsersSerializer()

    class Meta:
        model = Profile
        fields = ('id', 'user', 'location')

    def update(self, instance, validated_data):
        instance.location = validated_data.get('location', instance.location)
        instance.save()

        if validated_data.setdefault('user') is not None:
            user_data = validated_data.pop('user')
            user = instance.user

            user.first_name = user_data.get('first_name', user.first_name)
            user.last_name = user_data.get('last_name', user.last_name)
            user.email = user_data.get('email', user.email)
            user.save()
        return instance


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ('code', 'name')

class AirlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airline
        fields = ('code', 'name')

class FlightsSerializer(serializers.ModelSerializer):
    from_airport = AirportSerializer()
    to_airport = AirportSerializer()
    airline = AirlineSerializer()

    class Meta:
        model = Flight
        fields = ('from_airport', 'to_airport', 'airline', 'price')


class TicketsSerializer(serializers.ModelSerializer):
    flights = FlightsSerializer(many=True)

    class Meta:
        model = Ticket
        fields = ('id', 'profile', 'flights', 'num_stops', 'ad', 'ch', 'inf', 'date', 'price', 'paid')

    def create(self, validated_data):
        profile = validated_data.pop('profile')
        flights = validated_data.pop('flights')
        fls = []
        for fl in flights:
            air_from = \
                Airport.objects.get_or_create(code=fl['from_airport']['code'], name=fl['from_airport']['name'])[
                    0]
            air_to = Airport.objects.get_or_create(code=fl['to_airport']['code'], name=fl['to_airport']['name'])[0]
            airline = Airline.objects.get_or_create(code=fl['airline']['code'], name=fl['airline']['name'])[0]

            flight_sup = \
                Flight.objects.get_or_create(from_airport=air_from, to_airport=air_to, airline=airline,
                                             price=fl['price'])[0]
            fls.append(flight_sup)
        ticket = Ticket.objects.create(profile=profile, **validated_data)
        ticket.flights.set(fls)
        return ticket
