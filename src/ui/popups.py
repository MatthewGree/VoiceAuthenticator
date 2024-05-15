from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup


def create_popup(title: str, message: str) -> Popup:
    layout = GridLayout(cols=1, padding=10)
    label = Label(text=message)
    close_button = Button(text='Close')
    layout.add_widget(label)
    layout.add_widget(close_button)
    popup = Popup(title=title, content=layout, background_color=(1, 0, 0, 1))
    close_button.bind(on_press=popup.dismiss)
    return popup
