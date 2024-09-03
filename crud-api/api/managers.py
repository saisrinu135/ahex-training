from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self, email, password, **extra_filelds):
        if not email:
            raise ValueError("Email is required")
        
        # Creating a user
        user = self.model(email=email, password=password, **extra_filelds)
        user.set_password(password)
        user.save()
        
        return user
    
    def create_superuser(self, email, password, **extra_fileds):
        # setting is_staff and is_superuser to True
        extra_fileds.setdefault('is_staff', True)
        extra_fileds.setdefault('is_superuser', True)
        extra_fileds.setdefault('is_active', True)
        
        if extra_fileds.get('is_staff') is not True:
            raise ValueError("Super user must have is_staff=True.")
        
        # creating a user
        return self.create_user(email, password, **extra_fileds)