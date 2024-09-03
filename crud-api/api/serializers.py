from rest_framework.serializers import ModelSerializer
from .models import Student, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']
        extra_fields = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }
    
    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password']
        )
        user.save()
        
        return user


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'