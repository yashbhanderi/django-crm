from django.shortcuts import redirect
from django.http import Http404

# def group_required(*groups):

#     def decorator(function):
#         def wrapper(request, *args, **kwargs):
#             # if request.user.groups.filter(
#             #     name__in=[group for group in groups]
#             # ).exists():
#             #     return function(request, *args, **kwargs)
#             # raise Http404
#             group = None
#             if request.user.groups.exists():
#                 group = request.user.groups.all()[0].name

#             if group == 'customer':
#                 return redirect('user_page')

#             elif group == 'admin':
#                 return function(request, *args, **kwargs)

#         return wrapper

#     return decorator

from functools import wraps

def group_required(*groups):
    def inner(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):
            if request.user.groups.filter(name__in=groups).exists():
                return view_func(request, *args, **kwargs)
            else:
                return redirect('user_page')
        return wrapper_func
    return inner