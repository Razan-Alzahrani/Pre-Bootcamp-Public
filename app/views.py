from django.shortcuts import render , redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'index.html')



# ====================================================
#                sp register and login
# ===================================================
def sp_register(request):
    errors = Freelancer.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect("/")
    else:
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        phone_no= request.POST['phone']
        email = request.POST["email"]
        category = request.POST['category']
        password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = Freelancer.objects.create(fname=fname,lname=lname,phone_no=phone_no, email=email,category=category, password=password)
        request.session['uid'] = user.id
        request.session['fname'] = user.fname

        return redirect("/")

def login_page(request):
    return render(request, 'index.html')

def login(request):
    errors = Freelancer.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/login_page')
    else:
        user = Freelancer.objects.get(email=request.POST['email'])
        request.session['uid'] = user.id
        request.session['fname'] = user.fname

        return redirect('/freelancer')
# ====================================================
#                sp page
# ===================================================
def freelancer(request):

    context = {
        # 'this_user': Freelancer.objects.get(id=request.session['loged_in']),
        'all_users' : Freelancer.objects.all(),
        'all_projects': Project.objects.all(),
        'all_request': Request.objects.all()

    }
    return render(request, 'freelancer.html',context)

def approved(request,id):
    req=Request.objects.get(id=id)
    # return redirect(f'/freelancer/{req.id}')
    return redirect('/customer')

def edit_account(request,id):
    context={
        "this_user":Freelancer.objects.get(id=id),
    }
    return render(request,'edit_fre_acc.html',context)

def updated_account(request,id):
    this_user = Freelancer.objects.get(id=id)

    this_user.fname=request.POST['f_name']
    this_user.lname=request.POST['l_name']
    this_user.phone_no=request.POST['phone']
    this_user.email=request.POST['Email']
    this_user.save()

    return redirect('/freelancer')
# ====================================================
#                Costumer register and login
# ===================================================
def costumer_register(request):
    errors = Customer.objects.register_validator(request.POST)
    if len(errors) > 0 :
        for key , val in errors.items():
            messages.error(request, val)
        return redirect('/')
    else:
        pwd_hash = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
        user1 = Customer.objects.create(
            fname = request.POST['fname'],
            lname = request.POST['lname'],
            phone_no= request.POST['phone'],
            email = request.POST['email'],
            password = pwd_hash)
        request.session['uid'] = user1.id
        request.session['fname'] = user1.fname

        return redirect('/')
def login_customer(request):
    errors = Customer.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/login_page')
    else:
        user = Customer.objects.get(email=request.POST['email'])
        request.session['uid'] = user.id
        request.session['fname'] = user.fname

        return redirect('/customer')
# ====================================================
#                costumer page
# ===================================================
def customer(request):
    context = {
        'all_users' : Customer.objects.all(),
        'all_freelancer' : Freelancer.objects.all(),
        'all_projects': Project.objects.all(),
        'all_req': Request.objects.all()


    }
    return render(request,'customer.html',context)

# ====================================================
#                logout
# ===================================================
def logout(request):
    request.session.clear()
    return redirect('/')

def add_proj(request):
    context={
        'all_project':Project.objects.all()
    }
    return render(request,'add_proj.html',context)

def create_proj(request):
    this_user = Customer.objects.get(id=request.session['uid'])
    project=Project.objects.all()
    Project.objects.create(
        proj_name=request.POST['proj'],
        start_date=request.POST['date'],
        deadline=request.POST['Edate'],
        discription=request.POST['desc'],
        customer=Customer.objects.get(id=request.session['uid'])
        )
    return redirect('/customer')

def accept_req(request):
    context={
        'all_request':Request.objects.all()
    }
    return render(request,'accept_req.html',context)

def create_req(request):
    this_user = Freelancer.objects.get(id=request.session['uid'])
    Request.objects.create(
        request=request.POST['request'],
        offer_from=Freelancer.objects.get(id=request.session['uid'])

        )
    return redirect('/customer')

def delete(request,id):
    this_proj=Project.objects.get(id=id)
    this_proj.delete()
    return redirect('/customer')

def view(request,id):
    context={
        # 'freelancer':Freelancer.objects.all(),
        'request':Request.objects.get(id=id)
    }
    return render(request,'view.html',context)