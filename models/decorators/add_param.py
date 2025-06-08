# import functools

# def add_param(func=None, *, have_default_values=False, default_values=None):
#     if default_values is None:
#         default_values = {}

#     def decorator(f):
#         @functools.wraps(f)
#         def wrapper(*args, **kwargs):
#             return f(*args, **kwargs)

#         wrapper.__is_param__ = True
#         wrapper.__have_default_values__ = have_default_values
#         if have_default_values:
#             wrapper.__default_values__ = default_values

#         return wrapper

#     if func is None:
#         return decorator
#     else:
#         return decorator(func)
    
def add_param(func):
    func.__is_param__ = True
    return func