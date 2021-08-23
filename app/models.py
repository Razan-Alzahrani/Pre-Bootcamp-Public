from django.db import models
import re 
import bcrypt
# Create your models here.

# =========================================
#           User validation
# =========================================
class UserManager(models.Manager):
    def register_validator(self , postData):
        errors = {}
        user_in_db = Freelancer.objects.filter(email=postData['email'])
        if len(postData['fname']) < 3:
            errors['fname'] = "First name must be more then 3 characters"
        if len(postData['lname']) < 3:
            errors['lname'] = "Last name must be more then 3 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email"
        if len(postData['password']) < 8:
            errors['password'] = "password must be more then 8"
        if postData['password'] != postData['confpassword']:
            errors['password'] = "passwords must match"
        if user_in_db:
            errors['email'] = "user alrready exists"
        return errors

    def login_validator(self, postData):
        errors = {}
        user = Freelancer.objects.filter(email=postData['email'])
        if user:
            login_user = user[0]
            if not bcrypt.checkpw(postData['password'].encode(),login_user.password.encode()):
                errors['password'] = "Invalid login"
        else:
            errors['password'] = "Invalid login"
        return errors


# =========================================
#           Costumer validation
# =========================================
class CostumerManager(models.Manager):
    def register_validator(self , postData):
        errors = {}
        user_in_db = Customer.objects.filter(email=postData['email'])
        if len(postData['fname']) < 3:
            errors['fname'] = "must be more then 3 characters"
        if len(postData['lname']) < 3:
            errors['lname'] = "must be more then 3 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email"
        if len(postData['password']) < 8:
            errors['password'] = "password must be more then 8"
        if postData['password'] != postData['confpassword']:
            errors['password'] = "passwords must match"
        if user_in_db:
            errors['email'] = "user alrready exists"
        return errors

    def login_validator(self, postData):
        errors = {}
        user = Customer.objects.filter(email=postData['email'])
        if user:
            login_user = user[0]
            if not bcrypt.checkpw(postData['password'].encode(),login_user.password.encode()):
                errors['password'] = "Invalid login"
        else:
            errors['password'] = "Invalid login"
        return errors


# # =========================================
# #            Service validation
# # =========================================
# # class ServiceManager(models.Manager):
# #     def service_validator(self , postData):
# #         errors = {}
# #         if len(postData['----']) < 3:
# #                 errors['----'] = "--------------"
# #         if len(postData['----']) < 0:
# #                 errors['-----'] = "--------"
# #         return errors


# =========================================
#           Freelancer class
# =========================================
class Freelancer(models.Model):
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    phone_no= models.IntegerField()
    email = models.CharField(max_length=30)
    category=models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

# =========================================
#           Costumer class
# =========================================
class Customer(models.Model):
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    phone_no= models.IntegerField()
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CostumerManager()

# =========================================
#          Project class
# =========================================
class Project(models.Model):
    proj_name = models.CharField(max_length=250)
    freelancer=models.ForeignKey(Freelancer, related_name="freelancer" ,on_delete = models.CASCADE, null=True)
    customer=models.ForeignKey(Customer, related_name="customer" ,on_delete = models.CASCADE)
    start_date=models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(auto_now=True)
    discription = models.CharField(max_length=230)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # objects = ServiceManager()

# =========================================
#          Request class
# =========================================
class Request(models.Model):
    request = models.CharField(max_length=250)
    offer_from=models.ForeignKey(Freelancer, related_name="request" ,on_delete = models.CASCADE,null=True)
    customer=models.ForeignKey(Customer, related_name="customer1" ,on_delete = models.CASCADE,null=True)
    project=models.ForeignKey(Project, related_name="project" ,on_delete = models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # objects = ServiceManager()