from django.shortcuts import render

# Create your views here.
def index(request):
    data = {}
    data['page'] = 'home'
    return render(request, 'UserFrontend/index.html', data)

def login(request):
    data = {}
    data['page'] = 'login'
    return render(request, 'UserFrontend/login.html', data)


def register(request):
    data = {}
    data['page'] = 'login'
    return render(request, 'UserFrontend/register.html', data)


def forgot_password(request):
    data = {}
    data['page'] = 'login'
    return render(request, 'UserFrontend/forgot-password.html', data)


def reset_password(request, code):
    data = {}
    data['page'] = 'login'
    data['code'] = code
    return render(request, 'UserFrontend/reset-password.html', data)


def change_password(request):
    data = {}
    data['page'] = 'login'
    return render(request, 'UserFrontend/change-password.html', data)


def logout(request):
    return render(request, 'UserFrontend/logout.html')


def verify_mail(request, code):
    return render(request, 'UserFrontend/verify.html', {'code': code})


def aboutUs(request):
    data = {}
    data['page'] = 'about_us'
    return render(request, 'UserFrontend/about.html', data)


def gallery(request):
    data = {}
    data['page'] = 'gallery'
    return render(request, 'UserFrontend/gallery.html', data)


def requestPickUp(request):
    data = {}
    data['page'] = 'request_pickup'
    return render(request, 'UserFrontend/request-pickup.html', data)


def raiseIssue(request, code):
    data = {}
    data['page'] = 'raise_issue'
    data['request_id'] = code
    return render(request, 'UserFrontend/raise-an-issue.html', data)


def contact(request):
    data = {}
    data['page'] = 'contact'
    return render(request, 'UserFrontend/contact.html', data)


def my_requests(request):
    data = {}
    data['page'] = 'my_requests'
    return render(request, 'UserFrontend/my-requests.html', data)
