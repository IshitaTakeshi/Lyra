from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.popup import Popup
from ..ml import MLInterface 

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.

Builder.load_string("""  
<FirstSelectionScreen>:
    BoxLayout:
        Button:
            text: 'Analyze new'
            on_press: root.manager.current = 'select_music_root'
        Button:
            text: 'Open'
            on_press: root.manager.current = 'select_data_file'


<SelectMusicRootScreen>:
    BoxLayout:
        Button:
            id: root_select_button
            text: 'Select a directory your favorite music is in'
            on_press: root.manager.current = 'analyze_music'
        Button:
            text: 'Back'
            on_press: root.manager.current = 'first_selection'


<AnalyzeMusicScreen>:
    BoxLayout:
        Button:
            id: analyze_music
            text: 'Analyze'
            on_press: root.manager.current = 'select_query'
        Button:
            text: 'Back'
            on_press: root.manager.current = 'select_music_root'


<SelectDataFileScreen>:
    id: select_data_file
    BoxLayout:
        Button:
            id: select_data_file
            text: 'Select a data file'
            on_press: root.manager.current = 'load_data_file'
        FileChooserListView:
            id: filechooser
            on_selection: select_data_file.selected(filechooser.selection)
        Button:
            text: 'Back'
            on_press: root.manager.current = 'first_selection'


<LoadDataFileScreen>:
    BoxLayout:
        Button:
            id: load_data_file
            text: 'Load'
            on_press: root.manager.current = 'select_query'
        Button:
            text: 'Back'
            on_press: root.manager.current = 'select_data_file'


<SelectQueryScreen>:
    BoxLayout:
        Button:
            id: select_query
            text: 'Select your favorite music'
            on_press: root.manager.current = 'search'
        Button:
            text: 'Back'
            on_press: root.manager.current = root.manager.previous()


<SearchScreen>:
    BoxLayout:
        Button:
            id: search
            text: 'Search'
        Button:
            text: 'Back'
            on_press: root.manager.current = 'select_query'
""")


class FirstSelectionScreen(Screen):
    def __init__(self, ml_interface, name):
        Screen.__init__(self, name=name)
        self.ml_interface = ml_interface

class SelectMusicRootScreen(Screen):
    def __init__(self, ml_interface, name):
        Screen.__init__(self, name=name)
        self.ml_interface = ml_interface

class AnalyzeMusicScreen(Screen):
    def __init__(self, ml_interface, name):
        Screen.__init__(self, name=name)
        self.ml_interface = ml_interface


class LoadDialog(FloatLayout):
    def __init__(self, ml_interface, name):
        Screen.__init__(self, name=name)
        self.ml_interface = ml_interface


class SelectDataFileScreen(Screen):
    def __init__(self, ml_interface, name):
        Screen.__init__(self, name=name)
        self.ml_interface = ml_interface

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self.popup = Popup(title="Load file", content=content)
        self.popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            print(stream.read())


class LoadDataFileScreen(Screen):
    def __init__(self, ml_interface, name):
        Screen.__init__(self, name=name)
        self.ml_interface = ml_interface

    def show_load(self):
        from filechooser import FileChooserDialog
        content = FileChooserDialog(load=self.load, cancel=self.dismiss_popup)
        self.popup = Popup(title="Load a data file", content=content, 
                           size_hint=(0.9, 0.9))
        self.popup.open()
    
    def dismiss_popup(self):
        self.popup.dismiss()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as f:
            self.text_input.text = stream.read()


class SelectQueryScreen(Screen):
    def __init__(self, ml_interface, name):
        Screen.__init__(self, name=name)
        self.ml_interface = ml_interface


class SearchScreen(Screen):
    def __init__(self, ml_interface, name):
        Screen.__init__(self, name=name)
        self.ml_interface = ml_interface


class LyraApp(App):
    def build(self):
        ml_interface = MLInterface()
        manager = ScreenManager()

        manager.add_widget(
            FirstSelectionScreen(ml_interface, name='first_selection'))

        manager.add_widget(
            SelectMusicRootScreen(ml_interface, name='select_music_root'))

        manager.add_widget(
            AnalyzeMusicScreen(ml_interface, name='analyze_music'))

        manager.add_widget(
            SelectDataFileScreen(ml_interface, name='select_data_file'))

        manager.add_widget(
            LoadDataFileScreen(ml_interface, name='load_data_file'))

        manager.add_widget(
            SelectQueryScreen(ml_interface, name='select_query'))

        manager.add_widget(
            SearchScreen(ml_interface, name='search'))

        return manager


def run_gui():
    LyraApp().run()
