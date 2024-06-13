def sum(*args):
    n = 0
    for i in args:
        n+=i
    return n

def minus(*args):
    n = args[0]
    for i in args[1:]:
        n-=i
    return n