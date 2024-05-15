from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from popups import create_popup
from src.ui.audio_booth import AudioBooth
from src.ui.user_service import UserService


class FaceAuthenticationApp(App):

    def __init__(self, user_service: UserService):
        super().__init__()
        self.photo_booth: AudioBooth = AudioBooth()
        self.user_service: UserService = user_service
        self.nickname_input: TextInput = TextInput()

    def build(self):
        # Adjust the window size for demonstration purposes
        Window.size = (800, 600)

        # Main layout
        main_layout = BoxLayout(orientation='horizontal', padding=10, spacing=10)

        # Left layout for login/register
        left_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Nickname input field
        self.nickname_input = TextInput(hint_text='Enter your nickname', size_hint=(1, 0.2))
        left_layout.add_widget(self.nickname_input)

        # Login button
        login_button = Button(text='Login', size_hint=(1, 0.2), on_press=self._login_user)
        # Implement login function
        left_layout.add_widget(login_button)

        # Register button
        register_button = Button(text='Register', size_hint=(1, 0.2), on_press=self._register_user)
        # Implement register function
        left_layout.add_widget(register_button)

        # Add left layout to main layout
        main_layout.add_widget(left_layout)

        self.photo_booth = AudioBooth(orientation='vertical', padding=10, spacing=10)

        # Add right layout to main layout
        main_layout.add_widget(self.photo_booth)

        return main_layout

    def _register_user(self, _):
        if not self.__verify_authentication_data():
            return
        self.user_service.register_user(self.nickname_input.text, self.photo_booth.get_audio_path())
        create_popup("Info", "User Registered").open()

    def _login_user(self, _):
        if not self.__verify_authentication_data():
            return
        login_result = self.user_service.login_user(self.nickname_input.text, self.photo_booth.get_audio_path())
        if login_result:
            create_popup("Info", "Login Successful").open()
        else:
            create_popup("Info", "Login Failed").open()

    def __verify_authentication_data(self) -> bool:
        if not self.photo_booth.audio_recorded:
            create_popup("Error", "Take a picture first").open()
            return False
        if len(self.nickname_input.text) == 0:
            create_popup("Error", "Please enter your nickname").open()
            return False
        return True

    def on_stop(self):
        self.photo_booth.release_audio_resources()


if __name__ == '__main__':
    FaceAuthenticationApp(user_service=UserService()).run()
