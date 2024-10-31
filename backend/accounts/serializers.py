from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from core.managers import DateFormatManager
from .managers import (
    UserAPIManager, StudentManager, ProviderManager
)
from .models import (
    UserModel, ProfileModel,
    PersonModel, StudentModel, ProviderModel
)

class UserCreateSerializer(UserCreateSerializer):    
    class Meta(UserCreateSerializer.Meta):
        model = UserModel
        fields = ('id', 'email', 'first_name', 'last_name', 'role', 'password')


class UserUpdateSerializer(UserAPIManager):
    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name']

class ProfileCustomSerializer(serializers.ModelSerializer):
    gender_display = serializers.SerializerMethodField()

    class Meta:
        model = ProfileModel
        fields = ['id', 'gender_display', 'age']

    def get_gender_display(self, obj):
        return obj.get_gender_display()


class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ['id', 'gender', 'birthdate', 'bio']

class ProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = '__all__'

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ['gender', 'birthdate', 'bio']

class UserListSerializer(serializers.ModelSerializer):
    profile = ProfileCustomSerializer(read_only=True)
    role_display = serializers.SerializerMethodField()
    
    class Meta:
        model = UserModel
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'role_display', 'profile']
        extra_kwargs = {'password': {'write_only': True}}

    def get_role_display(self, obj):
        return obj.get_role_display()
    
class UserDetailSerializer(serializers.ModelSerializer):
    role_display = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        exclude = ['password']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_role_display(self, obj):
        return obj.get_role_display()
        
class PersonCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonModel
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number']

class StudentCreateUpdateSerializer(StudentManager):
    class Meta:
        model = StudentModel
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'control_number', 'degree']

class ProviderCreateUpdateSerializer(ProviderManager):
    class Meta:
        model = ProviderModel
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'RFC', 'NSS']

class StudentListSerializer(serializers.ModelSerializer):
    degree_display = serializers.SerializerMethodField()

    class Meta:
        model = StudentModel
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'control_number', 'degree_display']

    def get_degree_display(self, obj):
        return obj.get_degree_display()

class ProviderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProviderModel
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'RFC', 'NSS']

class StudentDetailSerializer(StudentManager, DateFormatManager):
    degree_display = serializers.SerializerMethodField()

    class Meta:
        model = StudentModel
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def get_degree_display(self, obj):
        return obj.get_degree_display()
    
class ProviderDetailSerializer(ProviderManager, DateFormatManager):
    class Meta:
        model = ProviderModel
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']