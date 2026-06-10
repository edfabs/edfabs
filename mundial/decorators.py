from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def role_required(role):
    """Protege vistas de admin: @role_required('ADMIN')"""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('mundial:login')
            if request.user.role != role:
                messages.error(request, 'No tienes permiso para acceder a esta sección.')
                return redirect('mundial:dashboard')
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


def verified_required(view_func):
    """Requiere que el usuario tenga email verificado."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('mundial:login')
        if not request.user.is_verified:
            messages.warning(
                request,
                'Debes verificar tu correo electrónico para acceder a esta sección.'
            )
            return redirect('mundial:verify_email_notice')
        return view_func(request, *args, **kwargs)
    return _wrapped
