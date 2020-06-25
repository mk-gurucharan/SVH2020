from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton, MDRaisedButton
from kivy.uix.image import Image,AsyncImage
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel,MDIcon
from kivymd.font_definitions import theme_font_styles
from kivy.uix.popup import Popup

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
            popup = Popup(title ="You Have Chosen To Open Mobile Camera", size_hint =(None, None), size =(200, 200))
            popup.open()
            closeButton = MDRectangleFlatButton(text = "Close")
            popup.add_widget(closeButton)
            closeButton.bind(on_press = popup.dismiss)
        elif button_text == "Open CCTV":
            popup = Popup(title ="You Have Chosen To Open CCTV", size_hint =(None, None), size =(200, 200))
            popup.open()
            closeButton = MDRectangleFlatButton(text = "Close")
            popup.add_widget(closeButton)
            closeButton.bind(on_press = popup.dismiss)
        else:
            popup = Popup(title ="You Have Chosen To Load a Recorded Video", size_hint =(None, None), size =(200, 200))
            popup.open()
            closeButton = MDRectangleFlatButton(text = "Close")
            popup.add_widget(closeButton)
            closeButton.bind(on_press = popup.dismiss)
    

Social_DistancingApp().run()

