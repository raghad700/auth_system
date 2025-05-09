from django.db import models
from django.contrib.auth.models import AbstractUser
import bcrypt

class User(AbstractUser):
    """
    Custom User model that extends Django's built-in AbstractUser.
    Adds email uniqueness and custom password hashing using bcrypt.
    """
    email = models.EmailField(unique=True)  # Ensures email addresses are unique across all users
    
    def save(self, *args, **kwargs):
        """
        Overrides the default save method to hash passwords using bcrypt.
        Only hashes if the password isn't already hashed (doesn't start with 'bcrypt$').
        """
        if self.password and not self.password.startswith('bcrypt$'):
            # Hash the password using bcrypt with auto-generated salt
            hashed = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            # Store with 'bcrypt$' prefix to identify our hashing method
            self.password = f"bcrypt${hashed}"
        super().save(*args, **kwargs)
    
    def check_password(self, raw_password):
        """
        Checks if the given raw password matches the stored hashed password.
        Handles both bcrypt hashed passwords (with 'bcrypt$' prefix) and default Django hashes.
        """
        if self.password.startswith('bcrypt$'):
            # Extract the actual bcrypt hash (after the prefix)
            stored_password = self.password.split('bcrypt$')[1]
            # Compare the raw password with the stored hash
            return bcrypt.checkpw(raw_password.encode('utf-8'), stored_password.encode('utf-8'))
        # Fall back to Django's default password checking for other hash types
        return super().check_password(raw_password)