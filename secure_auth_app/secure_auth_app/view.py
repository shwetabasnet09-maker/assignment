import qrcode
import pyotp
from io import BytesIO
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .backend import UserProfile 
from .utils import generate_otp_secret  


def generate_qr(request):
    user = request.user
    otp_secret = user.userprofile.otp_secret
    totp = pyotp.TOTP(otp_secret)
    uri = totp.provisioning_uri(name=user.username, issuer_name="MyDjangoApp")

    qr = qrcode.make(uri)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    return HttpResponse(buffer.getvalue(), content_type='image/png')



def mfa_setup(request):
    user = request.user
    if not user.userprofile.otp_secret:
        user.userprofile.otp_secret = generate_otp_secret()
        user.userprofile.save()
    
    return render(request, 'mfa_setup.html') 



def mfa_verify(request):
    if request.method == 'POST':
        code = request.POST.get('otp')
        user = request.user
        totp = pyotp.TOTP(user.userprofile.otp_secret)
        
        if totp.verify(code):
            request.session['mfa_authenticated'] = True
            return redirect('dashboard')  # Replace with your dashboard view name
        else:
            return render(request, 'mfa_verify.html', {'error': 'Invalid code'})
    
    return render(request, 'mfa_verify.html')



def mfa_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('mfa_authenticated'):
            return redirect('mfa_verify')
        return view_func(request, *args, **kwargs)
    return wrapper



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['mfa_authenticated'] = False  # this is for user to make them eaiser Reset MFA session
            return redirect('mfa_verify')  # Redirect to MFA verification for data base to verify it
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')
