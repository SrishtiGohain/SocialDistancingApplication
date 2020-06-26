import cv2
import tkinter as tk
from PIL import Image, ImageTk
import math


cap = cv2.VideoCapture(0)
global button_path
face_model = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

print("For this model initial calibration was done by taking width of object to be 17cm and the distance of 30cm away from camera 
      so as to calculate the focal length. And then this focal length was used for calculating distance between the object and camera.")

   
def show_frame():
    rgb = cv2.cvtColor(sdist(), cv2.COLOR_BGR2RGB)
    prevImg = Image.fromarray(rgb)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame)

def sdist():
    while True:    
      centroid = []
      person_in_contact=""
      status,photo = cap.read()
      face_cor = face_model.detectMultiScale(photo)
      font = cv2.FONT_HERSHEY_SIMPLEX
      org = (20, 80)
      fontScale = 1
      color = (255, 0, 0)
      thickness = 2
      centroid.clear()
      i = 1
      if len(face_cor) == 0:
          pass
      else:
          for (x,y,w,h) in face_cor:    
              x1 = x
              y1 = y
              x2 = x + w
              y2 = y + h
              
              centroid.append((int((x2+x1)/2), int((y2+y1)/2)))
            #distance was calculated using focal length. focal length = 400cm. Focal_length = (Pixcel_width x  Distance from camera) / Width of obejct . width =17cm distance=30cm, pixcel=200px
              
              cv2.rectangle(photo, (x1,y1), (x2,y2), [0,255,0], 3)
              cv2.putText(photo, f'Person: {i}', ((x1 -10), (y1-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
              i += 1
              
          for i in range(len(centroid)):
              for j in range(i+1, len(centroid)):
                  d = math.sqrt( ((centroid[j][1]-centroid[i][1])**2)+((centroid[j][0]-centroid[i][0])**2) )
                  dP = "{:.2f}".format(17*400/d) + " cm"
                  print("ID:",i+1,"- ID:",j+1,"=",dP)
                
                 
                  if (17*400/d) < 40 :
                      person_in_contact = "Person "+str(i+1)+" and Person "+str(j+1)
                      prr = "Follow social distancing "

                      cv2.putText(photo,person_in_contact,org,cv2.FONT_HERSHEY_SIMPLEX,fontScale, color, thickness,cv2.LINE_AA)
                      cv2.putText(photo,prr,(20,110),cv2.FONT_HERSHEY_SIMPLEX,fontScale, color, thickness,cv2.LINE_AA)
                      cv2.putText(photo,"!!ALERT!!!",(10,30),font,fontScale, [0,0,255], thickness,cv2.LINE_AA)
                      
          return photo
          
mainWindow = tk.Tk() 
mainWindow.resizable(width=False, height=False)
mainWindow.bind('<Escape>', lambda e: mainWindow.quit())
mainWindow.title("Social Distancing")
lmain = tk.Label(mainWindow, compound=tk.CENTER, anchor=tk.CENTER, relief=tk.RAISED)
lmain.pack()

show_frame()
mainWindow.mainloop()

cap.release()
