from django.http import HttpResponse


def login(request):
    html = "<html><body>It is now.</body></html>"
    return HttpResponse(html)


def register(request):
    pass


def register_school(request):
    pass


def register_teacher(request):
    pass


def register_parent(request):
    pass


def register_student(request):
    pass