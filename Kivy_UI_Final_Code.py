from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton, MDRaisedButton, MDFlatButton
from kivy.uix.image import Image,AsyncImage
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.core.window import Window
from kivymd.uix.label import MDLabel,MDIcon
from kivymd.font_definitions import theme_font_styles
from kivy.uix.popup import Popup
from kivy.uix.video import Video
import cv2
import imutils
import os
import time
import numpy as np


def Check(a,  b):
    dist = ((a[0] - b[0]) ** 2 + 550 / ((a[1] + b[1]) / 2) * (a[1] - b[1]) ** 2) ** 0.5
    calibration = (a[1] + b[1]) / 2       
    if 0 < dist < 0.25 * calibration:
        return True
    else:
        return False

def Setup(yolo):
    global net, ln, LABELS
    weights = os.path.sep.join([yolo, "yolov3.weights"])
    config = os.path.sep.join([yolo, "yolov3.cfg"])
    labelsPath = os.path.sep.join([yolo, "coco.names"])
    LABELS = open(labelsPath).read().strip().split("\n")  
    net = cv2.dnn.readNetFromDarknet(config, weights)
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

def ImageProcess(image):
    global processedImg, count
    (H, W) = (None, None)
    frame = image.copy()
    if W is None or H is None:
        (H, W) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    starttime = time.time()
    layerOutputs = net.forward(ln)
    stoptime = time.time()
    print("Video is Getting Processed at {:.4f} seconds per frame".format((stoptime-starttime))) 
    confidences = []
    outline = []
    
    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            maxi_class = np.argmax(scores)
            confidence = scores[maxi_class]
            if LABELS[maxi_class] == "person":
                if confidence > 0.5:
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))
                    outline.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))

    box_line = cv2.dnn.NMSBoxes(outline, confidences, 0.5, 0.3)

    if len(box_line) > 0:
        flat_box = box_line.flatten()
        pairs = []
        center = []
        status = [] 
        for i in flat_box:
            (x, y) = (outline[i][0], outline[i][1])
            (w, h) = (outline[i][2], outline[i][3])
            center.append([int(x + w / 2), int(y + h / 2)])
            status.append(False)

        for i in range(len(center)):
            for j in range(len(center)):
                close = Check(center[i], center[j])

                if close:
                    pairs.append([center[i], center[j]])
                    status[i] = True
                    status[j] = True
        index = 0

        for i in flat_box:
            (x, y) = (outline[i][0], outline[i][1])
            (w, h) = (outline[i][2], outline[i][3])
            if status[index] == True:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 150), 2)
            elif status[index] == False:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            index += 1
        for h in pairs:
            cv2.line(frame, tuple(h[0]), tuple(h[1]), (0, 0, 255), 2)
            count +=1
    processedImg = frame.copy()

Window.size=(360,600)
class Social_DistancingApp(MDApp):

    def build(self):
        layout = MDBoxLayout(orientation='vertical', spacing=20, padding=30)

        titlelabel= MDLabel(text="SmartSocial", halign="center", theme_text_color="ContrastParentBackground",
                        font_style="H3")
        label = MDLabel(text="Social Distance Monitoring App", halign="center", theme_text_color="Hint",
                        font_style="H4")
        sublabel = MDLabel(text="Welcome!", halign="center", theme_text_color="Secondary",
                        font_style="H5")
        label1 = MDLabel(text="Choose your source", halign="center", theme_text_color="Secondary",
                        font_style="Body1")
        label2 = MDLabel(text="#StayHomeStaySafe", halign="center", theme_text_color="Error",
                        font_style="Body2")
        img = AsyncImage(source='https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/SARS-CoV-2_without_background.png/597px-SARS-CoV-2_without_background.png',pos_hint={'center_x': 0.5, 'center_y': 0.2})
        btn1 = MDRaisedButton(text='Open Mobile Camera',
                                     pos_hint={'center_x': 0.5, 'center_y': 0.7}, on_press=self.on_button_press)
        btn2 = MDRaisedButton(text='Open CCTV',
                                     pos_hint={'center_x': 0.5, 'center_y': 0.8}, on_press=self.on_button_press)
        btn3 = MDRaisedButton(text='Load a Recorded Video',
                                     pos_hint={'center_x': 0.5, 'center_y': 0.9}, on_press=self.on_button_press)
        layout.add_widget(img)
        layout.add_widget(titlelabel)
        layout.add_widget(label)
        layout.add_widget(sublabel)
        layout.add_widget(label1)
        layout.add_widget(btn1)
        layout.add_widget(btn2)
        layout.add_widget(btn3)
        layout.add_widget(label2)
        return layout
    
    def on_button_press(self, instance):
        button_text = instance.text

        if button_text == "Open Mobile Camera":
            frameno = 0
            yolo = "yolo-coco/"
            cap = cv2.VideoCapture(0) 
            time1 = time.time()
            while(True):

                ret, frame = cap.read()
                if not ret:
                    break
                current_img = frame.copy()
                frameno += 1
                Setup(yolo)
                if(frameno%2 == 0 or frameno == 1):
                    ImageProcess(current_img)
                    Frame = processedImg
                    cv2.imshow('frame', Frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            time2 = time.time()

            cap.release() 
            cv2.destroyAllWindows()
        elif button_text == "Open CCTV":
            popup = Popup(title ="You Have Chosen To Open CCTV", size_hint =(None, None), size =(200, 200))
            popup.open()
            closeButton = MDFlatButton(text = "Close")
            popup.add_widget(closeButton)
            closeButton.bind(on_press = popup.dismiss)
        else:
            cap = cv2.VideoCapture('output_1.mp4') 
            while(cap.isOpened()): 
                ret, frame = cap.read() 
                if ret == True: 
                    cv2.imshow('Frame', frame) 
                    if cv2.waitKey(25) & 0xFF == ord('q'): 
                        break
                else:  
                    break

            cap.release() 
            cv2.destroyAllWindows() 

Social_DistancingApp().run()

