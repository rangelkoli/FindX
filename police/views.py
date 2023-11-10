from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from police.models import Register,Posts
from citizens.models import Notification
# Create your views here.
def policehome(request):
    allCases = Register.objects.all()
    return render(request,'policehome.html',{"allCases":allCases})

def dashboard(request):
    allCases = Register.objects.all()
    return render(request,'dashboard.html',{"allCases":allCases})

def reportPDF(request,slug):
    reg = Register.objects.filter(slug = slug).first()
    name = reg.name
    age = reg.age
    address = reg.address
    city = reg.city
    zip = reg.zip
    state = reg.state
    aadhar = reg.govID
    height = reg.height
    hairType = reg.hairType
    hairColor = reg.hairColor
    skinTone = reg.skinTone
    physique = reg.physique
    reward = reg.reward
    permanent = reg.permanent
    dispute = reg.dispute

    template_path = 'reportPDF.html'
    permanent = reg.permanent
    context = {'name': name, 'age': age, 'address': address,'city': city, 'zip':zip, 'state': state, 'aadhar': aadhar, 'height':height, 'hairType':hairType, 'hairColor':hairColor, 'physique':physique, 'reward':reward, 'skinTone':skinTone, 'permanent': permanent, 'dsipute':dispute }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response,)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username= username, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            print("Success!")
            return redirect("/police/home")
        else:
            return redirect('/police')
    else:
        return render(request, 'policelogin.html')
    
def logout(request):
   auth.logout(request)
   return redirect('/police')


def register(request):
    if request.method == 'POST':
        register = Register()
        name = request.POST.get('name')
        age = request.POST.get('age')
        govID = request.POST.get('govID')
        height = request.POST.get('height')
        address = request.POST.get('address')
        lastLoc = request.POST.get('lastLoc')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        dob = request.POST.get('dob')
        gender  = request.POST.get('gender')
        skinTone = request.POST.get('skinTone')
        hairType = request.POST.get('hairType')
        eyeColor = request.POST.get('eyeColor')
        hairColor = request.POST.get('hairColor')
        clothes = request.POST.get('clothes')
        physique = request.POST.get('physique')
        permanent = request.POST.get('permanent')
        dispute = request.POST.get('dispute')
        reward = request.POST.get('reward')
        nameSus = request.POST.get('nameSus')
        ageSus = request.POST.get('ageSus')
        relation = request.POST.get('relation')
        reason = request.POST.get('reason')
        image = request.FILES.get('image')
        imageDoc = request.FILES.get('imageDoc')
        policeStation = request.POST.get('policeStation')
         
        register.name = name
        register.age = age
        register.govID  = govID 
        register.height= height
        register.address = address
        register.lastLoc = lastLoc
        register.city  = city 
        register.state  = state 
        register.zip = zip
        register.dob = dob
        register.gender = gender
        register.skinTone = skinTone
        register.hairType= hairType
        register.eyeColor = eyeColor
        register.hairColor = hairColor
        register.clothes = clothes
        register.physique = physique
        register.permanent = permanent
        register.dispute = dispute
        register.reward = reward
        register.nameSus = nameSus
        register.ageSus = ageSus
        register.relation = relation 
        register.reason = reason
        register.image = image
        register.imageDoc = imageDoc
        register.policeStation = policeStation
        register.save()
        return HttpResponse("Successfully Regitered")
    else:
        return render(request , 'register.html')

def search(request):
    query = request.GET['query']
    allCases = Register.objects.filter(name__icontains=query)
    params = {'allCases' : allCases}
    return render(request , 'search.html', params)

def dashDetail(request, slug):
    reg = Register.objects.filter(slug = slug).first()
    case_status = ""
    rootpolice = 0
    len_case_status = 6
    print(request.user)
    if reg.policeStation == str(request.user):
        rootpolice = 1
    print(rootpolice)
    if request.method == "POST":
        case_status = request.POST.get('radio')
        len_case_status = len(case_status)
        reg.case_status = case_status
        reg.save()
        redirect('dashDetail/<str:slug>')
        print("Status updated")
    context = {'reg': reg,'case_status':case_status,'rootpolice':rootpolice,'len_case_status':len_case_status}
    return render(request,'dashDetail.html', context)
    
def update_status(request,slug):
    reg = Register.objects.filter(slug = slug).first()
    if request.method == "POST":
        case_status = request.POST.get('status')
        print(case_status)
        reg.save()
    return render(request,'dashDetail.html')
    
def notifications(request):
    allNotification = Notification.objects.all()
    notify = []
    notifyroot = []
    notify_exists = 0
    for notification in allNotification:

        if notification.closestPoliceStation == str(request.user) or notification.rootPoliceStation == str(request.user):
            notify.append(notification)
            print(notify)
            
   
    notify_exists = len(notify)
    return render(request,'notification.html',{'notify':notify,'notify_exists':notify_exists})


def posts(request,slug):
    allPosts = Posts.objects.filter(receiverPolice = slug)
    print(allPosts)
    receiver = slug
    print(receiver)
    if request.method == "POST":
        post = request.POST.get('post-text')
        sender = request.user
        print(sender)
        posts = Posts()
        posts.message = post
        posts.senderPolice = sender
        posts.receiverPolice = receiver
        posts.save()
        print("Posts Saved successfully!")
        return render(request,'posts.html',{'allPosts':allPosts,'receiver':receiver})


    return render(request,'posts.html',{'allPosts':allPosts,'receiver':receiver})