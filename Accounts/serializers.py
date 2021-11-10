from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from .validators import *
import django.contrib.auth.password_validation as validators
from django.core import exceptions
from django.contrib.auth import get_user_model
User = get_user_model() 

class RegistrationSerializers(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    # password2 = serializers.CharField(style={'input_type':'passsword'}, write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'admin', 'password', 'player','wallet_address']
        extra_kwargs = {
            'password' : {'write_only':True},
            'admin' : {'write_only':True},
            'player' : {'write_only':True},
        }

    def save(self):
        password = self.validated_data.get('password', None)
        errors = dict() 
        try:
            validators.validate_password(password=password, user=User)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        email = self.validated_data.get('email',None)
        first_name = self.validated_data.get('first_name', None)
        last_name = self.validated_data.get('last_name', None)
        wallet_address = self.validated_data.get('wallet_address', None)
        # if password != password2:
        #     raise serializers.ValidationError({'password':'Passwords must match.'})
        user = User.objects.create_player(email=email,password=password, first_name=first_name, last_name=last_name, wallet_address=wallet_address)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email', '')
        password = data.get('password', '')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'account' : 'Account with this email not found'})
        
        if user is not None:
            if not check_password(password, user.password):
                raise serializers.ValidationError({'password' : 'Incorrect password'})
       
        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError({'credentials' : 'Invalid credentials'})
        return data
