from django.db import models
from autoslug import AutoSlugField




class Register(models.Model):
    case_status = models.CharField(max_length=20,default='Active')
    name = models.CharField(max_length=50, null=True)
    age = models.IntegerField(default=0, null=True)
    height = models.IntegerField(default=0, null=True)
    govID = models.CharField(max_length=50, primary_key=True)
    dob = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=250, null=True)
    lastLoc = models.CharField(max_length=250, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    zip = models.CharField(max_length = 100, null=True)
    gender = models.CharField(max_length=255, null=True)
    policeStation = models.CharField(max_length=255, null=True)
    hairColor = models.CharField(max_length=255, null=True)
    hairType = models.CharField(max_length=255, null=True)
    skinTone = models.CharField(max_length=255, null=True)
    eyeColor = models.CharField(max_length=255, null=True)
    clothes = models.CharField(max_length=255, null=True)
    physique = models.CharField(max_length=255, null=True)
    permanent = models.CharField(max_length=255, null=True)
    dispute = models.CharField(max_length=255, null=True)
    reward = models.CharField(max_length=255, null=True)
    nameSus = models.CharField(max_length=255, null=True)
    ageSus = models.CharField(max_length=255, null=True)
    relation = models.CharField(max_length=255, null=True)
    reason = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to="db/", null=True)
    imageDoc = models.ImageField(upload_to="imagesDoc/", null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    slug = AutoSlugField(populate_from='govID')
    def __str__(self):
                return 'This is ' +self.name
    

    
class Posts(models.Model):
    senderPolice = models.CharField(max_length=255)
    receiverPolice = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    govid = models.CharField(max_length=255)
    