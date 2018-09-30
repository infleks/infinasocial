from django.shortcuts import render, HttpResponse, redirect
from app.models import User, Post, UpVotePost
import datetime as dt

alertredirect = '<script> alert("%s"); window.location="%s"; </script>'
posttypes = {'normal':1, 'activity':2, 'business':3}


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

    u = User.objects.get(pk=rq.session['user_id'])
    ps = Post.objects.filter(posttype=posttypes['normal']).order_by("-creationdatetime")

    postdicts = []

    for p in ps:
        tmp={}
        tmp['post'] = p
        tmp['upvotecount'] = len(UpVotePost.objects.filter(post=p.pk))
        tmp['creationdatetimestr'] =  dt.datetime.strftime(p.creationdatetime, "%d/%m/%Y %H:%M")
        tmp['likebuttoncolor'] = "black" if len(UpVotePost.objects.filter(user=u, post=p)) < 1 else "var(--cred)"
        tmp['commentcount'] = len(Post.objects.filter(connected=p.pk))
        postdicts.append(tmp)

    return render(rq, "index.html", {"posts":postdicts})

def sendpost(rq):
    if 'user_id' not in rq.session.keys():
        return redirect('/login')

    if rq.method != "POST":
        return redirect('/')

    u =  User.objects.get(pk=rq.session['user_id'])
    p = Post()
    p.user = u
    p.content = rq.POST['post']
    p.creationdatetime = dt.datetime.now()
    p.posttype = posttypes['normal']

    if 'connected' in rq.POST.keys():
        p.connected = Post.objects.get(pk=rq.POST['connected'])
        p.save()
        return redirect('/post/%d'% int(rq.POST['connected']))

    p.save()

    return redirect('/')

def upvotepost(rq, post_id):
    if 'user_id' not in rq.session.keys():
        return redirect('/login')

    postid = post_id
    try :
        user = User.objects.get(pk=rq.session['user_id'])
        post = Post.objects.get(pk=postid)
        uvp = UpVotePost.objects.filter(user=user, post=post)
        if ( len(uvp)>0 ) :
            uvp[0].delete()
            return HttpResponse("")

        uvp = UpVotePost()
        uvp.user = user
        uvp.post = post
        uvp.save()
    except Exception as e :
        print(e)

    return HttpResponse("")


def post(rq,post_id):
    if 'user_id' not in rq.session.keys():
        return redirect('/login')

    postid = post_id

    try :
        user = User.objects.get(pk=rq.session['user_id'])
        post = Post.objects.get(pk=postid)
        main={}

        main['post'] = post
        main['upvotecount'] = len(UpVotePost.objects.filter(post=post.pk))
        main['creationdatetimestr'] =  dt.datetime.strftime(post.creationdatetime, "%d/%m/%Y %H:%M")
        main['likebuttoncolor'] = "black" if len(UpVotePost.objects.filter(user=user, post=post)) < 1 else "var(--cred)"
        main['commentcount'] = len(Post.objects.filter(connected=post.pk))
        main['upvotes'] = UpVotePost.objects.filter(post=post.pk)

        comments = Post.objects.filter(connected=post).order_by("creationdatetime")

        commentdicts = []
        for p in comments:
            tmp={}
            tmp['post'] = p
            tmp['upvotecount'] = len(UpVotePost.objects.filter(post=p.pk))
            tmp['creationdatetimestr'] =  dt.datetime.strftime(p.creationdatetime, "%d/%m/%Y %H:%M")
            tmp['likebuttoncolor'] = "black" if len(UpVotePost.objects.filter(user=user, post=p)) < 1 else "var(--cred)"
            tmp['commentcount'] = len(Post.objects.filter(connected=p.pk))
            commentdicts.append(tmp)

        return render(rq, "post.html", {"p":main, "comments":commentdicts})
    except Exception as e :
        print(e)

    return HttpResponse(alertredirect % ("Aradığınız gönderi bulunamamıştır.", "/"))


def getNotifications(rq) :
    if 'user_id' not in rq.session.keys():
        return redirect('/login')

    user = User.objects.get(pk=rq.session['user_id'])
    upvotes = UpVotePost.getNotificationData(user)
    