from django.shortcuts import render, redirect
from citizens.deepface.detectors import FaceDetector
from citizens.models import Image, Notification
from deepface import DeepFace
import shutil
import math

from police.models import Register

cords = [[19.2308612109548, 72.828497842019], [19.216237795518, 72.8209724957716], [19.210185135899, 72.850724567154], [19.2297932218252, 72.8560620861978]]
location = ["Gorai", "Charkop", "Kandivali", "Borivali"]

def home(request):
    all_cases = Register.objects.all()
    return render(request, 'citizenshome.html', {"allCases": all_cases})

def scan(request):
    if request.method == "POST":
        Image.objects.all().delete()
        if 'image' in request.FILES:
            image = request.FILES['image']
            ins = Image(photo=image)
            ins.save()
            print("Successfully inserted")
        return redirect('uploaded')
    return render(request, 'scan.html')

def uploaded(request):
    img = Image.objects.all()
    return render(request, 'uploaded.html', {'img': img})

def find_matching_image(img_path):
    df = DeepFace.find(img_path=img_path, db_path="images/db/", enforce_detection=True, detector_backend= "mtcnn",model_name="VGG-Face",distance_metric="cosine")
    return df

def scanimage(request):
    image = Image.objects.last()
    img_path = image.photo.path
    
    try:
        # Use DeepFace to check if faces are present in the image
        df = find_matching_image(img_path)
        print(df)
        if df["VGG-Face_cosine"][0] < 0.3:
            match_found = df.shape[0]
        else:
            match_found = 0
        print("Match found", match_found)

        match = False
        identity = ""
        closest_police_station = ""

        if match_found > 0:
            identity = str(df['identity'][0])
            print("Match Image", identity)

            match = True
            if request.method == "POST":
                latitude = float(request.POST['latitude'])
                longitude = float(request.POST['longitude'])
                closest_police_station = min_distance(latitude, longitude)
                send_notification(identity, latitude, longitude, closest_police_station)

        shutil.rmtree("D:/FindX/images/images")

        return render(request, 'results.html', {'match': match, 'identity': identity, 'closestPoliceStation': closest_police_station})
    except Exception as e:
        # Handle exceptions that might arise during the DeepFace process
        print("Error:", str(e))
        return render(request, 'results.html', {'error_message': str(e)})

def min_distance(lat, lon):
    min_distance = 9999999999999
    min_index = 0
    closest_police_station = ""
    
    for i in range(len(cords)):
        dist = distance(lat, lon, cords[i][0], cords[i][1], "K")
        
        if dist < min_distance:
            min_distance = dist
            min_index = i
    
    closest_police_station = location[min_index]
    return closest_police_station

def distance(lat1, lon1, lat2, lon2, unit):
    radlat1 = math.pi * float(lat1) / 180
    radlat2 = math.pi * float(lat2) / 180
    theta = float(lon1) - float(lon2)
    radtheta = math.pi * theta / 180
    dist = math.sin(radlat1) * math.sin(radlat2) + math.cos(radlat1) * math.cos(radlat2) * math.cos(radtheta)
    
    if dist > 1:
        dist = 1
    
    dist = math.acos(dist)
    dist = dist * 180 / math.pi
    dist = dist * 60 * 1.1515
    
    if unit == "K":
        dist = dist * 1.609344
    if unit == "N":
        dist = dist * 0.8684
    
    return dist
def send_notification(identity, latitude, longitude, closest_police_station):
    all_cases = Register.objects.all()
    
    for case in all_cases:
        if identity in case.image.url:  # Check if the identity is present in the image URL
            notify = Notification()
            notify.image = case.image
            notify.latitude = latitude
            notify.longitude = longitude
            notify.case_name = case.name
            notify.govid = case.govID
            notify.rootPoliceStation = case.policeStation
            notify.closestPoliceStation = closest_police_station
            notify.save()
            print("Notification sent successfully!")
            break
