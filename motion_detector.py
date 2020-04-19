import cv2, time, pandas,os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
TOKEN = '1193023091:AAEl9eLOZ6Q0PdDRXF07TprHDXt9tEGuclo'
bot = telegram.Bot(TOKEN)
from datetime import datetime
import images 
import bot2
first_frame=None
status_list=[None,None]
times=[]
chat_id = 1266674916
#df=pandas.DataFrame(columns=["Start","End"])

video=cv2.VideoCapture(0)
currentframe=0
while True:
    check, frame = video.read()
    status=1
    timestamp = datetime.now()
    text = "Unoccupied"
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(31,31),0)

    if first_frame is None:
        first_frame=gray
        continue

    delta_frame=cv2.absdiff(first_frame,gray)
    thresh_frame=cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame=cv2.dilate(thresh_frame, None, iterations=2)

    (_,cnts,_)=cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status=1

        (x, y, w, h)=cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 3)
        text = "Occupied"


    # draw the text and timestamp on the frame
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,0.35, (0, 0, 255), 1)
    
    status_list.append(status)

    status_list=status_list[-2:]

    #Screenshot
    #if(text=="Occupied"):
        #cv2.imwrite("/home/aayushbangroo/Desktop/Motion-Detector/tasveer.jpg",frame)
           
    if status_list[-1]==1 and status_list[-2]==0:
        times.append(datetime.now())
    if status_list[-1]==0 and status_list[-2]==1:
        times.append(datetime.now())


    cv2.imshow("Gray Frame",gray)
    cv2.imshow("Delta Frame",delta_frame)
    cv2.imshow("Threshold Frame",thresh_frame)
    cv2.imshow("Color Frame",frame)

    key=cv2.waitKey(1)

    if key==ord('q'):
        if status==1:
            times.append(datetime.now())
        break
#Taking the image of the frame-----------------------------------------------------------------------
    while(True):
        if(text=="Occupied" and currentframe%200==0):
            name = 'images/'+str(currentframe) + '.jpg'
            cv2.imwrite(name,frame)
            currentframe += 1
            caption = images.caption_this_image(name)
            print(caption)
            bot2.tasveer(name,caption)
            break
        else:
            currentframe+=1
            break
#---------------------------------------------------------------------------------------------------------
#print(status_list)
#print(times)
print(currentframe)
video.release()
cv2.destroyAllWindows
