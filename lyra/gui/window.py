import os
import time

from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.app import App
from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.listview import ListView, ListItemButton, SelectableView
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.listview import ListView
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout 
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup

from .spacer import HorizontalSpacer, VerticalSpacer
from ..ml import MLInterface


window_size = (500, 350)
Window.size = window_size


first_selection = 'first_selection'
load_data_file = 'load_data_file'
select_music_root = 'select_music_root'
search_music = 'search_music'
show_result = 'show_result'

HOME_DIR = os.path.expanduser('~')
CURRENT_DIR = os.getcwd()
DATA_DIR = os.path.join(HOME_DIR, '.lyra')

if not(os.path.exists(DATA_DIR)):
    os.mkdir(DATA_DIR)

#DEBUG
DEBUG = False
if(DEBUG):
    from kivy.core.text import LabelBase, DEFAULT_FONT
    from kivy.resources import resource_add_path
     

    DEBUG_DIR = os.path.abspath('./dataset/Music/KiminoShiranaiMonogatari')
    font_dir = os.path.join(HOME_DIR, '.fonts')

    resource_add_path(font_dir)
    LabelBase.register(DEFAULT_FONT, 'ipaexm.ttf')


class ChangeScreenButton(Button):
    def __init__(self, manager, destination, **kwargs):
        Button.__init__(self, **kwargs)
        self.manager = manager
        self.destination = destination

    def on_press(self):
        Button.on_press(self)
        self.manager.current = self.destination


class FirstSelectionScreen(Screen):
    def __init__(self, name, manager):
        Screen.__init__(self, name=name) 

        size_hint = (0.4, 0.1)
        size = (
            window_size[0]*size_hint[0],
            window_size[1]*size_hint[1]
        )

        center_x = (window_size[0]-size[0])/2
        
        analyze_new_button = ChangeScreenButton(
            manager=manager,
            destination=select_music_root,
            size_hint=size_hint,
            pos=(center_x, int(2*window_size[1]/3)-20),
            text="Analyze new"
        )
        
        load_data_button = ChangeScreenButton(
            manager=manager, 
            destination=load_data_file,
            size_hint=size_hint,
            pos=(center_x, int(window_size[1]/3)-20),
            text="Open a data file"
        )

        self.add_widget(analyze_new_button)
        self.add_widget(load_data_button)


class LoadDataFileScreen(Screen):
    def __init__(self, name, manager, music_engine):
        Screen.__init__(self, name=name)
        
        self.music_engine = music_engine

        layout = BoxLayout(orientation='vertical')

        self.filechooser = FileChooserListView(
            path=DATA_DIR,
            size_hint=(1.0, 0.7))
        self.filechooser.bind(selection=self.on_file_selected)
        
        self.explanation_window = Label(text='Select a data file', 
                                        size_hint=(1.0, 0.1))

        back_button = ChangeScreenButton(manager=manager,
                                         destination=first_selection,
                                         text="Back")

        self.load_button = Button(text="Load")
        self.load_button.bind(on_press=self.load)
        self.load_button.disabled = True 
        
        button_layout = BoxLayout(orientation='horizontal', 
                                  size_hint=(1.0, 0.2), 
                                  spacing=30,
                                  padding=(10, 10, 10, 10))
        button_layout.add_widget(back_button)
        button_layout.add_widget(self.load_button)
        
        layout.add_widget(self.filechooser)
        layout.add_widget(self.explanation_window)
        layout.add_widget(button_layout)

        self.add_widget(layout)

    def on_file_selected(self, path, selection):
        self.load_button.disabled = False

    def show_message(self, message):
        self.explanation_window.text = message

    def load(self, instance):
        selected_path = self.filechooser.selection[0] 
        if not(os.path.isfile(selected_path)):
            return

        try:
            self.music_engine.load(selected_path)
        except Exception:
            self.show_message(
                "The selected file is not following the Lyra's format.")
            return 

        self.manager.current = search_music


class SelectMusicRootScreen(Screen):
    def __init__(self, name, manager, music_engine):
        Screen.__init__(self, name=name)
        self.music_engine = music_engine

        if(DEBUG):
            self.filechooser = FileChooserListView(path=DEBUG_DIR)
        else:
            self.filechooser = FileChooserListView(path=HOME_DIR)

        self.explanation_window = Label(text='Select a music file', 
                                        size_hint=(1.0, 0.2))

        button_layout = BoxLayout(orientation='horizontal', 
                                  size_hint=(1.0, 0.3), 
                                  spacing=30,
                                  padding=(10, 10, 10, 10))

        back_button = ChangeScreenButton(manager=manager,
                                              destination=first_selection,
                                              text="Back")

        select_button = Button(text="Select")

        self.analyze_button = Button(text="Analyze")

        self.next_button = ChangeScreenButton(manager=manager, 
                                              destination=search_music,
                                              text="Next")
        self.next_button.disabled = True
        self.analyze_button.disabled = True
        
        select_button.bind(on_press=self.select)
        self.analyze_button.bind(on_press=self.analyze)

        button_layout.add_widget(back_button)
        button_layout.add_widget(select_button)
        button_layout.add_widget(self.analyze_button)
        button_layout.add_widget(self.next_button)

        #TODO add a message popup to show when selecting not directory
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.filechooser)
        layout.add_widget(self.explanation_window)
        layout.add_widget(button_layout)

        self.add_widget(layout)
   
    def show_message(self, message):
        self.explanation_window.text = message

    def select(self, instance):
        selected_directory = self.filechooser.path

        if not(os.path.isdir(selected_directory)):
            self.show_message("Select a directory, not a file.")
            self.analyze_button.disabled = True
            return

        self.show_message(
            "'{}' is selected.\n"\
            "Click [Analyze] to analyze music "\
            "(this takes a few minute)".format(selected_directory))

        self.music_engine.set_music_root(selected_directory)
        self.analyze_button.disabled = False

    def analyze(self, instance):
        self.show_message("Aanalyzing...")

        try:
            self.music_engine.extract_features()
        except:
            self.show_message("No wav music found. Choose another directory.")
            return
        
        self.next_button.disabled = False 
        self.show_message("Finished")


#FIXME the logic is dirty
class SaveFeaturesWindow(BoxLayout):
    def __init__(self, music_engine):
        BoxLayout.__init__(self, orientation='vertical')

        self.music_engine = music_engine

        #Called to close this window
        self.close = None

        self.filechooser = FileChooserListView(
            path=DATA_DIR,
            size_hint=(1.0, 0.8))
        self.filechooser.bind(selection=self.on_file_selected)

        self.text_input = TextInput(size_hint=(1.0, 0.1))

        self.cancel_button = Button(text="Cancel", size_hint=(0.2, 1.0))

        save_button = Button(text="Save", size_hint=(0.2, 1.0))
        save_button.bind(on_press=self.save)

        button_layout = BoxLayout(orientation="horizontal", 
                                  size_hint=(1.0, 0.1))
        button_layout.add_widget(HorizontalSpacer())
        button_layout.add_widget(self.cancel_button)
        button_layout.add_widget(save_button)

        self.add_widget(self.filechooser)
        self.add_widget(self.text_input)
        self.add_widget(button_layout)
    
    #TODO
    def on_file_selected(self, path, selection):
        print("file selected: {}".format(self.filechooser.selection))
        selected_path = self.filechooser.selection[0]
        filename = os.path.basename(selected_path)
        self.text_input.text = filename

    def save(self, instance): 
        print("current_path:{}".format(self.filechooser.path))
        current_path = self.filechooser.path
        filename = self.text_input.text
        filepath = os.path.join(current_path, filename)

        if not(os.access(os.path.dirname(filepath), os.W_OK)):
            print("Invalid filename: {}".format(filename))
            return

        if(os.path.exists(filepath)):
            #TODO ask if overwrite
            pass

        print("filepath:{}".format(filepath))
        self.music_engine.save(filepath)
        
        self.close()

    def bind_to_close(self, on_press):
        self.close = on_press
        self.cancel_button.bind(on_press=self.close)


class PlayButton(Button):
    def __init__(self, sound_path, **kwargs):
        Button.__init__(self, **kwargs)
        self.text = "Play"
        self.bind(on_press=self.change_sound_state)
        self.sound = SoundLoader.load(sound_path)
        self.is_playing = False

    def play(self):
        self.sound.play()

    def stop(self):
        self.sound.stop()

    def change_sound_state(self, instance):
        Button.on_press(self)

        if(self.is_playing):
            self.stop()
            self.text = "Play"
        else:
            self.play()
            self.text = "Stop"

        self.is_playing = not self.is_playing


class MusicRow(SelectableView, BoxLayout):
    def __init__(self, sound_path, **kwargs):
        BoxLayout.__init__(self, **kwargs)
        SelectableView.__init__(self, **kwargs)

        layout = BoxLayout(orientation='horizontal')
        title = os.path.basename(sound_path)
        title_label = Label(text=title, size_hint=(0.8, 1.0))

        play_button = PlayButton(sound_path=sound_path, 
                                 size_hint=(0.2, 1.0))

        layout.add_widget(title_label)
        layout.add_widget(play_button)

        self.add_widget(layout)


class ResultWindow(BoxLayout):
    def __init__(self, sound_path_list):
        BoxLayout.__init__(self, orientation='vertical')

        sound_directory = {}
        sorted_keys = []
        for i, path in enumerate(sound_path_list):
            key = str(i)
            sound_directory[key] = path 
            sorted_keys.append(key)

        dict_adapter = DictAdapter(sorted_keys=sorted_keys, 
                                   data=sound_directory, 
                                   args_converter=self.list_item_args_converter,
                                   cls=MusicRow)

        list_view = ListView(adapter=dict_adapter)
        self.close_button = Button(text="Close", size_hint=(1.0, 0.1))
        self.add_widget(list_view)
        self.add_widget(self.close_button)
    
    def list_item_args_converter(self, row_index, sound_path): 
        return {'size_hint_y': None, 'height': 25, 
                'sound_path': sound_path}
    
    def bind_to_close(self, on_press):
        self.close_button.bind(on_press=on_press)


#TODO wrap message
class SearchScreen(Screen):
    def __init__(self, name, manager, music_engine):
        Screen.__init__(self, name=name)

        self.music_engine = music_engine

        self.filechooser = FileChooserListView(path=music_engine.music_root)

        self.explanation_window = Label(text='Select a music file', 
                                        size_hint=(1.0, 0.2))

        back_button = ChangeScreenButton(manager=manager,
                                         destination=select_music_root,
                                         text="Back")
        
        select_music_button = Button(text="Select")
        select_music_button.bind(on_press=self.select_music)

        self.search_button = Button(text="Search")
        self.search_button.bind(on_press=self.search)
        self.search_button.disabled = True

        save_features_button = Button(text="Save analyzation result")
        save_features_button.bind(on_press=self.save_features)

        button_layout = BoxLayout(orientation='horizontal', 
                                  size_hint=(1.0, 0.3), 
                                  spacing=30,
                                  padding=(10, 10, 10, 10))

        back_home_button = ChangeScreenButton(manager=manager,
                                              destination=first_selection,
                                              text="Back to home")

        button_layout.add_widget(back_button)
        button_layout.add_widget(select_music_button)
        button_layout.add_widget(self.search_button)
        button_layout.add_widget(save_features_button)
        button_layout.add_widget(back_home_button)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.filechooser)
        layout.add_widget(self.explanation_window)
        layout.add_widget(button_layout)

        self.add_widget(layout)
    
    def on_enter(self):
        self.filechooser.path = self.music_engine.music_root

    def show_message(self, message):
        self.explanation_window.text = message
    
    def select_music(self, instance):
        if(len(self.filechooser.selection) == 0):
            self.show_message("Select a file, not a directory.")
            self.search_button.disabled = True
            return
 
        selected_path = self.filechooser.selection[0]
        self.music_engine.set_query(selected_path)
        print("selected query: {}".format(self.music_engine.query_filepath))
        self.search_button.disabled = False
        self.show_message("'{}' is selected.".format(selected_path))

    def search(self, instance):
        k_nearest = self.music_engine.search()
        sound_path_list = [path for path, _ in k_nearest]

        result_window = ResultWindow(sound_path_list)
        popup = Popup(title="Music list", content=result_window)
        result_window.bind_to_close(on_press=popup.dismiss)
        popup.open()

    def save_features(self, instance):
        save_window = SaveFeaturesWindow(self.music_engine)
        popup = Popup(title="Save features", content=save_window)
        save_window.bind_to_close(on_press=popup.dismiss)
        popup.open()


class MainApp(App):
    def __init__(self, **kwargs):
        App.__init__(self, **kwargs)
        self.music_engine = MLInterface()

    def build(self):
        manager = ScreenManager()
        
        manager.add_widget(
            FirstSelectionScreen(first_selection, manager))
        
        manager.add_widget(
            LoadDataFileScreen(load_data_file, manager, self.music_engine))

        manager.add_widget(
            SelectMusicRootScreen(select_music_root, manager, 
                                  self.music_engine))

        manager.add_widget(
            SearchScreen(search_music, manager, self.music_engine))
        
        #manager.add_widget(
        #    ResultScreen(show_result, manager, self.music_engine))
        return manager


def run_gui():
    MainApp().run()
