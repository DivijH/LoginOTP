from django.shortcuts import render, redirect
from django.views import View
from login.models import Account
import hashlib
import random
from twilio.rest import Client

# Create your views here.

otp = 0

def encrypt(password):
    '''
    Function responsible for converting the password into a hash for saving
    
    @params
    password : String containing the password to be encrypted

    @return
    String containing the hash value of the password
    '''
    return hashlib.sha256(password.encode()).hexdigest()


def generate_otp():
    '''
    Function responsible for generating a four digit OTP

    @return
    4 digit integer representing the OTP
    '''
    return random.randint(1000, 9999)


class LoginView(View):
    '''
    Class representing the login page
    '''

    def get(self, request):
        '''
        Function handling the GET request
        '''
        return render(request, 'login/login.html')

    def post(self, request):
        '''
        Function handling the POST request
        '''
        data = request.POST
        email = data.get('email')
        password = encrypt(data.get('password'))

        # Checking if any field is empty
        if not email or not password:
            return render(request, 'login/login.html', {'error' : 'error'})

        # Check if the email and password is correct 
        try:

            # Checking for email
            account = Account.objects.filter(email=email)[0]
            name = account.first_name + ' ' + account.last_name
            
            # Check if the password is correct
            if account.password == password:
                return render(request, 'login/index.html', {'name' : name})
            else:
                raise Exception()
        except:
            return render(request, 'login/login.html', {'error' : 'error'})
        

class RegisterView(View):
    '''
    Class representing the Register Page
    '''

    def get(self, request):
        '''
        Function handling the GET request
        '''
        return render(request, 'login/register.html')

    def post(self, request):
        '''
        Function handling the POST request
        '''
        data = request.POST
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone')
        
        # Checking if any field is empty
        if not first_name or not last_name or not email or not password or not phone:
            return render(request, 'login/register.html', {'error' : 'error'})

        # Check if email already exists in the database
        try:
            email = Account.objects.filter(email=email)[0].email
        except:

            # Sending the OTP to the mobile number
            global otp
            otp = generate_otp()
            print(phone, otp)
            client = Client('<YOUR ACCOUNT SID>','<YOUR ACCOUNT AUTH TOKEN')
            client.messages.create(to=str(phone), from_='<YOUR ACCOUNT PHONE NUMBER >', body='One Time Password: '+str(otp))
            
            return render(request, 'login/otp.html', {
                'first_name' : first_name,
                'last_name' : last_name,
                'email' : email,
                'password' : password,
                'phone' : phone
            })
        
        return render(request, 'login/register.html', {'error' : 'error'})
        

class OTPView(View):
    '''
    Class representing the OTP Page
    '''
    
    def get(self, request):
        '''
        Function handling the GET request
        '''
        return render(request, '404.html', {'error' : '403. Can\'t access'})

    def post(self, request):
        '''
        Function handling the POST request
        '''
        data = request.POST
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        email = data.get('email')
        password = encrypt(data.get('password'))
        phone = data.get('phone')
        code = data.get('code')

        # Checking if the OTP entered is correct
        if int(code)==otp:
            account = Account(first_name=first_name, last_name=last_name, email=email, password=password, phone=phone)
            account.save()
            return redirect('/')
        else:
            return render(request, 'login/otp.html', {
                'first_name' : first_name,
                'last_name' : last_name,
                'email' : email,
                'password' : password,
                'phone' : phone,
                'error' : 'error'
            })
