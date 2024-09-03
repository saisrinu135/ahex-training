from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication, authenticate
from rest_framework.authtoken.models import Token

from .models import Student, User
from .serializers import StudentSerializer, UserSerializer


class UserView(ModelViewSet):
    """A viewset for viewing and editing user instances.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Create a new user instance.

        Args:
            request: The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A response object with the created user data or error message.
        """
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({'message':"Successful", 'data': serializer.data}, status=201, headers=headers)
        except Exception as e:
            return Response({'message': serializer.errors}, status=400)
    
    def list(self, request):
        """
        List all user instances.

        Args:
            request: The HTTP request object.

        Returns:
            Response: A response object with the list of users or error message.
        """
        try:
            queryset = self.get_queryset()
            serializer = self.serializer_class(queryset, many=True)
            return Response({'message':"Successful", 'data': serializer.data}, status=200)
        except Exception:
            return Response({'message': 'Failed', 'error':serializer.errors}, status=400)
    
    def retrieve(self, request, pk=None):
        """
        Retrieve a user instance.

        Args:
            request: The HTTP request object.
            pk: The primary key of the user to retrieve.

        Returns:
            Response: A response object with the user data or error message.
        """
        try:
            queryset = self.get_object()
            serializer = self.serializer_class(queryset)
            return Response({'message':"Successful", 'data': serializer.data}, status=200)
        except Exception:
            return Response({'message': 'Failed', 'error':serializer.errors}, status=400)
    
    def update(self, request, pk=None):
        """
        Update a user instance.

        Args:
            request: The HTTP request object.
            pk: The primary key of the user to update.

        Returns:
            Response: A response object with the updated user data or error message.
        """
        try:
            queryset = self.get_object()
            serializer = self.serializer_class(queryset, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message':"Successful", 'data': serializer.data}, status=200)
        except Exception as e:
            return Response({'message': 'Failed', 'error':serializer.errors}, status=400)
    
    def destroy(self, request, pk):
        """
        Delete a user instance.

        Args:
            request: The HTTP request object.
            pk: The primary key of the user to delete.

        Returns:
            Response: A response object with a success message or error message.
        """
        try:
            queryset = self.get_object()
            queryset.delete()
            return Response({'message':"Successful", 'data': 'User deleted successfully'}, status=200)
        except Exception as e:
            return Response({'message': 'Failed', 'error':str(e)}, status=400)


# Login View - Generates token for user
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # authenticating user using email and password
        try:
            user = authenticate(request, email=email, password=password)
            # creating auth token or getting existing token
            token, created = Token.objects.get_or_create(user=user)
            return Response({'message': 'Login successful', 'token': token.key}, status=200)
        except Exception:
            return Response({'message': 'Failed', 'error': 'Invalid credentials'}, status=400)



class StudentView(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]