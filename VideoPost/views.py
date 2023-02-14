import re
from django.shortcuts import render
from django.contrib import messages
from VideoPost.forms import inputLink
from pytube import YouTube
import os ,requests,threading,json
from . import views
from qabasat_post import settings
from django.http import HttpResponseRedirect
counter:int = 0

#create a view to handle download request 
def mainView (request):
    print(request.headers["User-Agent"])
    print(settings.BASE_DIR)
    m = re.search(r'\((.*)\)(.*)',request.headers["User-Agent"])
    if m :
        browserName=m.groups()
    print('\n',f'Request From : {browserName}')
    form =inputLink()
    link=""
    fileNames=[]
    if request.method=='POST':
        form=inputLink(request.POST)
        if form.is_valid():
            views.counter +=1
            link = form.cleaned_data['link']
            path = os.path.join(settings.BASE_DIR,"VideoPost/videos")
            fileNames=os.listdir(path)
            downloadThread=threading.Thread(target=views.downloadYT,args=(link,views.counter))
            downloadThread.start()
            messages.add_message(request,messages.INFO,"Working on " + str(link))
            return HttpResponseRedirect('')

    
    context={
        "browser":browserName,
        "link":link,
        "form":form
        }
    
    return render(request,"mainView.html",context)

def downloadYT(link:str,counter:int)->bool:
    SAVE_PATH=os.path.join(settings.BASE_DIR,"VideoPost/videos")
    finish=False
    # fileNames = []
    # fileSizes = {}
    file:str=""
    try:
        yt=YouTube(link)
    except:
        print("Error!")
    
    d_video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1]
    
    try:
        file="vid"+str(counter)+".mp4"
        d_video.download(SAVE_PATH,filename=file)
        # fileNames.append(name)
        # fileSizes[name.replace(".mp4","")]=os.path.getsize(SAVE_PATH+"/"+name)
        finish=True
    except Exception as e:
        print(e.format())
    
    
    
    if finish :
            # for file in fileNames:  
            print(f'uploading {file} to Qabasat . . . ')
            #QabasatMinNoor Facebook Page Id
            page_id="102596824731677"
            credentials = read_creds(os.path.join(settings.BASE_DIR,'VideoPost/credentials.json'))
            access_token=credentials['access_token']
            url=f'https://graph-video.facebook.com/{page_id}/videos?access_token={access_token}'
            path=os.path.join(settings.BASE_DIR,"VideoPost/videos/"+file)
            files={'file':open(path,'rb')}
            flag=requests.post(url, files=files).text
            os.remove(path)
            print (flag)
            # print (fileSizes)
            # print(*fileNames)
            print("All Done ")
        
    return finish
        


        
def read_creds(fileName):
        with open(fileName) as f :
                credentials=json.load(f)
        return credentials