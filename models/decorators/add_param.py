
def add_param(func):
    func.__is_param__ = True
    return func