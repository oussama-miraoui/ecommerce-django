from django.http import HttpResponse
from django.shortcuts import redirect


def anonyme_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin:
            return view_func(request, *args, **kwargs)
        elif request.user.is_authenticated and request.user.is_client:
            return redirect('Forbiden')
        else:
            return redirect('adminLogin')

    return wrapper_func
