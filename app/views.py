from django.shortcuts import render, HttpResponse, redirect
from app.models import User

alertredirect = '<script> alert("%s"); window.location="%s"; </script>'

def login(rq):
    if rq.method == "POST":
        ps = rq.POST
        u = User.checkUser(ps['email'], ps['password'])

        if u == None:
            return HttpResponse(alertredirect % ('Yanlış email veya şifre girdiniz', '/login') )
        
        rq.session['user_id'] = u.pk
        return redirect('/')

    return render(rq, "login.html", {})

def logout(rq):
    if 'user_id' in rq.session.keys():
        del rq.session['user_id']
    
    return redirect('/login')

def signup(rq):
    if rq.method == "POST":
        ps = rq.POST
        u = User()
        u.name = ps['name']
        u.surname = ps['surname']
        u.birthdate = ps['birthdate']
        u.email = ps['email']
        u.password = ps['password']
        
        try:
            u.save()
            return HttpResponse(alertredirect % ('Emailini kontrol et', '/login'))
        except Exception as e:
            return HttpResponse(alertredirect % ('Aynı email ile birden fazla kayıt oluşturulamaz', '/signup'))

    return render(rq, 'signup.html', {})

def forgotpassword(rq):
    if rq.method == "POST":
        # mail processes
        return HttpResponse(alertredirect % ('Emailini kontrol et', '/login'))
        
    return render(rq, 'forgotpassword.html', {})


def index(rq):
    if 'user_id' not in rq.session.keys():
        return redirect('/login')
    return render(rq, "index.html", {})