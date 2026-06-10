import io
from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.shortcuts import redirect, render
from django.utils.timezone import now

from PIL import Image

from ..forms.auth import ChangeEmailForm, EmailLoginForm, ProfileForm, RegistrationForm
from ..models import LoginAttempt

User = get_user_model()
_signer = TimestampSigner()

MAX_ATTEMPTS = 5
LOCKOUT_MINUTES = 15


def _get_client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '127.0.0.1')


def _failed_attempts(ip):
    cutoff = now() - timedelta(minutes=LOCKOUT_MINUTES)
    return LoginAttempt.objects.filter(ip=ip, success=False, timestamp__gte=cutoff).count()


def _lockout_remaining_minutes(ip):
    cutoff = now() - timedelta(minutes=LOCKOUT_MINUTES)
    oldest = (
        LoginAttempt.objects
        .filter(ip=ip, success=False, timestamp__gte=cutoff)
        .order_by('timestamp')
        .first()
    )
    if oldest:
        unlock_at = oldest.timestamp + timedelta(minutes=LOCKOUT_MINUTES)
        diff = unlock_at - now()
        return max(1, int(diff.total_seconds() // 60))
    return 0


def _send_verification_email(request, user):
    token = _signer.sign(str(user.pk))
    verify_url = request.build_absolute_uri(f'/mundial/verify-email/{token}/')
    send_mail(
        subject='Verifica tu email — Quiniela Mundial 2026',
        message=(
            f'Hola {user.full_name},\n\n'
            f'Verifica tu cuenta haciendo clic en el siguiente enlace:\n\n'
            f'{verify_url}\n\n'
            f'Este enlace expira en 24 horas.\n\n'
            f'Si no creaste esta cuenta, ignora este mensaje.'
        ),
        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@quiniela.com'),
        recipient_list=[user.email],
        fail_silently=False,
    )


def register_view(request):
    if request.user.is_authenticated:
        return redirect('mundial:dashboard')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                email=form.cleaned_data['email'],
                full_name=form.cleaned_data['full_name'],
                password=form.cleaned_data['password'],
            )
            try:
                _send_verification_email(request, user)
                messages.success(
                    request,
                    'Cuenta creada exitosamente. Revisa tu correo para verificar tu cuenta.'
                )
            except Exception:
                messages.warning(
                    request,
                    'Cuenta creada. Hubo un problema al enviar el correo de verificación.'
                )
            return redirect('mundial:login')
    else:
        form = RegistrationForm()

    return render(request, 'mundial/auth/register.html', {'form': form})


def verify_email_view(request, token):
    try:
        user_id = _signer.unsign(token, max_age=86400)
        user = User.objects.get(pk=user_id)
        if not user.is_verified:
            user.is_verified = True
            user.save(update_fields=['is_verified'])
        messages.success(request, '¡Email verificado! Ya puedes participar en la quiniela.')
        login(request, user, backend='mundial.backends.EmailAuthBackend')
        return redirect('mundial:dashboard')
    except SignatureExpired:
        return render(request, 'mundial/auth/verify_email_expired.html')
    except (BadSignature, User.DoesNotExist):
        messages.error(request, 'Enlace de verificación inválido.')
        return redirect('mundial:login')


def resend_verification_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').lower().strip()
        try:
            user = User.objects.get(email=email, is_verified=False)
            _send_verification_email(request, user)
        except User.DoesNotExist:
            pass
        messages.info(
            request,
            'Si el correo existe y no está verificado, recibirás un enlace de verificación.'
        )
        return redirect('mundial:login')
    return render(request, 'mundial/auth/resend_verification.html')


def verify_email_notice_view(request):
    return render(request, 'mundial/auth/verify_email_notice.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('mundial:dashboard')

    ip = _get_client_ip(request)
    attempts = _failed_attempts(ip)
    locked = attempts >= MAX_ATTEMPTS

    if request.method == 'POST' and not locked:
        form = EmailLoginForm(request, data=request.POST)
        email = request.POST.get('email', '').lower().strip()

        if form.is_valid():
            user = form.get_user()
            LoginAttempt.objects.create(user=user, ip=ip, success=True)
            login(request, user)
            messages.success(request, f'Bienvenido, {user.get_short_name()}.')
            next_url = request.GET.get('next', 'mundial:dashboard')
            return redirect(next_url)
        else:
            try:
                failed_user = User.objects.get(email=email)
            except User.DoesNotExist:
                failed_user = None
            LoginAttempt.objects.create(user=failed_user, ip=ip, success=False)
            attempts = _failed_attempts(ip)
            locked = attempts >= MAX_ATTEMPTS
            if locked:
                remaining = _lockout_remaining_minutes(ip)
                messages.error(
                    request,
                    f'Cuenta bloqueada por demasiados intentos fallidos. '
                    f'Intenta de nuevo en {remaining} minuto(s).'
                )
    else:
        form = EmailLoginForm(request)

    return render(request, 'mundial/auth/login.html', {
        'form': form,
        'locked': locked,
        'lockout_remaining': _lockout_remaining_minutes(ip) if locked else 0,
    })


def logout_view(request):
    logout(request)
    messages.info(request, 'Sesión cerrada.')
    return redirect('mundial:login')


@login_required(login_url='mundial:login')
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            obj = form.save(commit=False)
            if 'avatar' in request.FILES:
                try:
                    img_file = request.FILES['avatar']
                    img = Image.open(img_file).convert('RGB')
                    img.thumbnail((200, 200), Image.LANCZOS)
                    buf = io.BytesIO()
                    img.save(buf, format='JPEG', quality=85)
                    buf.seek(0)
                    obj.avatar = ContentFile(buf.read(), name=f'avatar_{user.pk}.jpg')
                except Exception:
                    messages.error(request, 'No se pudo procesar la imagen.')
                    return redirect('mundial:profile')
            obj.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('mundial:profile')
    else:
        form = ProfileForm(instance=user)

    return render(request, 'mundial/auth/profile.html', {'form': form})


@login_required(login_url='mundial:login')
def change_email_view(request):
    user = request.user

    if request.method == 'POST':
        form = ChangeEmailForm(user, request.POST)
        if form.is_valid():
            user.email = form.cleaned_data['new_email']
            user.is_verified = False
            user.save(update_fields=['email', 'is_verified'])
            _send_verification_email(request, user)
            logout(request)
            messages.info(
                request,
                'Tu correo fue actualizado. Verifica el nuevo correo para continuar.'
            )
            return redirect('mundial:login')
    else:
        form = ChangeEmailForm(user)

    return render(request, 'mundial/auth/change_email.html', {'form': form})
