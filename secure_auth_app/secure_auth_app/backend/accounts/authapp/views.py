import pyotp, qrcode
from io import BytesIO
from base64 import b64encode
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import User
from ..serializers import RegisterSerializer, LoginSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered'}, status=201)
        return Response(serializer.errors, status=400)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            if user.mfa_enabled:
                return Response({'mfa_required': True, 'user': user.username})
            return Response({'message': 'Login successful'})
        return Response(serializer.errors, status=400)

class MFASetupView(APIView):
    def get(self, request):
        username = request.GET.get('username')
        user = User.objects.get(username=username)
        if not user.mfa_secret:
            secret = pyotp.random_base32()
            user.mfa_secret = secret
            user.save()
        else:
            secret = user.mfa_secret

        otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(name=user.username, issuer_name="MFAApp")
        qr = qrcode.make(otp_uri)
        buf = BytesIO()
        qr.save(buf)
        image_b64 = b64encode(buf.getvalue()).decode('utf-8')
        return Response({'qr_code': image_b64})

class MFAVerifyView(APIView):
    def post(self, request):
        username = request.data.get('username')
        code = request.data.get('code')
        user = User.objects.get(username=username)
        totp = pyotp.TOTP(user.mfa_secret)
        if totp.verify(code):
            user.mfa_enabled = True
            user.save()
            return Response({'message': 'MFA verified'})
        return Response({'error': 'Invalid code'}, status=400)
