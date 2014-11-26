import os
import time

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
select_data_file = 'select_data_file'
select_music_root = 'select_music_root'
select_query = 'select_query'
show_result = 'show_result'


#DEBUG
DEBUG = True
if(DEBUG):
    from kivy.core.text import LabelBase, DEFAULT_FONT
    from kivy.resources import resource_add_path
     

    DEBUG_DIR = \
        './dataset/Music/KiminoShiranaiMonogatari'
    home = os.path.expanduser('~')
    font_dir = os.path.join(home, '.fonts')

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

        analyze_new_button = ChangeScreenButton(
            manager=manager,
            destination=select_music_root,
            size_hint=size_hint,
            pos=((window_size[0]-size[0])/2, 200),
            text="Analyze new"
        )
        
        load_data_button = ChangeScreenButton(
            manager=manager, 
            destination=select_data_file,
            size_hint=size_hint,
            pos=((window_size[0]-size[0])/2, 100),
            text="Open a data file"
        )

        self.add_widget(analyze_new_button)
        self.add_widget(load_data_button)


class SelectMusicRootScreen(Screen):
    def __init__(self, name, manager, music_engine):
        Screen.__init__(self, name=name)
        self.music_engine = music_engine

        if(DEBUG):
            self.filechooser = FileChooserListView(path=DEBUG_DIR)
        else:
            home_directory = os.path.expanduser('~')
            self.filechooser = FileChooserListView(path=home_directory)

        self.explanation_window = Label(text='Select a music file', 
                                        size_hint=(1.0, 0.2))

        button_layout = BoxLayout(orientation='horizontal', 
                                  size_hint=(1.0, 0.3), 
                                  spacing=30,
                                  padding=(10, 10, 10, 10))

        self.back_button = ChangeScreenButton(manager=manager,
                                              destination=first_selection,
                                              text="Back")

        self.select_button = Button(text="Select")

        self.analyze_button = Button(text="Analyze")

        self.next_button = ChangeScreenButton(manager=manager, 
                                              destination=select_query,
                                              text="Next")
        self.next_button.disabled = True
        self.analyze_button.disabled = True
        
        self.select_button.bind(on_press=self.select)
        self.analyze_button.bind(on_press=self.analyze)

        button_layout.add_widget(self.back_button)
        button_layout.add_widget(self.select_button)
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
            "(this takes a few minute).".format(selected_directory))

        self.music_engine.set_music_root(selected_directory)
        self.analyze_button.disabled = False

    def analyze(self, instance):
        self.show_message("Aanalyzing...")

        self.music_engine.extract_features()
        
        self.next_button.disabled = False 
        self.show_message("Finished")


class PlayButton(Button):
    def __init__(self, sound_path, **kwargs):
        Button.__init__(self, **kwargs)
        
        self.bind(on_press=self.play)
        self.sound = SoundLoader.load(sound_path)
        self.is_playing = False

    def play(self):
        pass
        #self.sound.play()

    def stop(self):
        pass
        #self.sound.stop()

    def on_press(self):
        Button.on_press(self)

        if(self.is_playing):
            self.stop()
        else:
            self.play()

        self.is_playing = not self.is_playing


class MusicRow(SelectableView, BoxLayout):
    def __init__(self, sound_path, **kwargs):
        BoxLayout.__init__(self, **kwargs)
        SelectableView.__init__(self, **kwargs)

        layout = BoxLayout(orientation='horizontal')

        title = os.path.basename(sound_path)
        title_label = Label(text=title, size_hint=(0.8, 1.0))

        play_button = PlayButton(sound_path=sound_path, 
                                 text="Play", size_hint=(0.2, 1.0))

        layout.add_widget(title_label)
        layout.add_widget(play_button)

        self.add_widget(layout)


class ResultWindow(BoxLayout):
    def __init__(self, sound_path_list):
        BoxLayout.__init__(self, orientation='vertical')

        sound_directory = {}
        for i, path in enumerate(sound_path_list):
            key = str(i)
            sound_directory[key] = path 

        sorted_keys = [str(i) for i in range(len(sound_path_list))]

        dict_adapter = DictAdapter(sorted_keys=sorted_keys, 
                                   data=sound_directory, 
                                   args_converter=self.list_item_args_converter,
                                   cls=MusicRow)

        list_view = ListView(adapter=dict_adapter)
        self.close_button = Button(text="Close", size_hint=(1.0, 0.1))
        self.add_widget(list_view)
        self.add_widget(self.close_button)
    
    def list_item_args_converter(self, row_index, record): 
        return {'size_hint_y': None, 'height': 25, 
                'sound_path': record[row_index]}
    
    def bind_to_close(self, on_press):
        self.close_button.bind(on_press=on_press)

    
#Builder.load_string('''
#[MusicRow@SelectableView+BoxLayout]:
#    index: ctx.index
#    fruit_name: ctx.text
#    size_hint_y: ctx.size_hint_y
#    height: ctx.height
#    <MusicRow>:
#        sound_path: ctx.text
#''')

#TODO wrap message
class SelectQueryScreen(Screen):
    def __init__(self, name, manager, music_engine):
        Screen.__init__(self, name=name)

        self.music_engine = music_engine

        if(DEBUG):
            self.filechooser = FileChooserListView(path=DEBUG_DIR)
        else:
            home_directory = os.path.expanduser('~')
            self.filechooser = FileChooserListView(path=home_directory)

        self.explanation_window = Label(text='Select a music file', 
                                        size_hint=(1.0, 0.2))

        back_button = ChangeScreenButton(manager=manager,
                                         destination=first_selection,
                                         text="Back")
        
        select_button = Button(text="Select")
        select_button.bind(on_press=self.select)

        self.search_button = Button(text="Search")
        self.search_button.bind(on_press=self.search)
        self.search_button.disabled = True

        button_layout = BoxLayout(orientation='horizontal', 
                                  size_hint=(1.0, 0.3), 
                                  spacing=30,
                                  padding=(10, 10, 10, 10))

        back_home_button = ChangeScreenButton(manager=manager,
                                              destination=first_selection,
                                              text="Back to home")

        button_layout.add_widget(back_button)
        button_layout.add_widget(select_button)
        button_layout.add_widget(self.search_button)
        button_layout.add_widget(back_home_button)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.filechooser)
        layout.add_widget(self.explanation_window)
        layout.add_widget(button_layout)

        self.add_widget(layout)
    
    def show_message(self, message):
        self.explanation_window.text = message
    
    def select(self, instance):
        if(len(self.filechooser.selection) == 0):
            self.show_message("Select a file, not a directory.")
            self.search_button.disabled = True
            return
 
        selected_path = self.filechooser.selection[0]
        self.music_engine.set_query(selected_path)
        print("selected query:{}".format(self.music_engine.query_filepath))
        self.search_button.disabled = False
        self.show_message("'{}' is selected.".format(selected_path))

    def search(self, instance):
        k_nearest = self.music_engine.search()
        sound_path_list = [os.path.basename(path) for path, _ in k_nearest]

        result_window = ResultWindow(sound_path_list)
        popup = Popup(title="Music list", content=result_window)
        result_window.bind_to_close(on_press=popup.dismiss)
        popup.open()






class ResultScreen(Screen):
    def __init__(self, name, manager, music_engine):
        Screen.__init__(self, name=name) 
        list_item_args_converter = \
                lambda row_index, rec: {'text': rec['text'],
                                        'is_selected': rec['is_selected'],
                                        'size_hint_y': None,
                                        'height': 25}

        from .fixtures import integers_dict
        dict_adapter = DictAdapter(sorted_keys=[str(i) for i in range(100)],
                                   data=integers_dict,
                                   args_converter=list_item_args_converter,
                                   template='MusicRow')
        list_view = ListView(adapter=dict_adapter)


        button_layout = BoxLayout(orientation='horizontal', 
                                  size_hint=(1.0, 0.2),
                                  spacing=30,
                                  padding=(10, 10, 10, 10))
        button_layout.add_widget(back_button)
        #button_layout.add_widget(HorizontalSpacer())
        button_layout.add_widget(back_home_button)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(list_view)
        layout.add_widget(VerticalSpacer(size_hint=(1.0, 0.1)))
        layout.add_widget(button_layout)

        self.add_widget(layout)

    def list_item_args_converter(self, row_index, record):
        d = {
            'text': record['name'], 
            'size_hint_y': None, 
            'height': 25
        }
        return d


class MainApp(App):
    def __init__(self, **kwargs):
        App.__init__(self, **kwargs)
        self.music_engine = MLInterface()

    def build(self):
        manager = ScreenManager()
        
        manager.add_widget(
            FirstSelectionScreen(first_selection, manager))
        
        manager.add_widget(
            SelectMusicRootScreen(select_music_root, manager, 
                                  self.music_engine))

        manager.add_widget(
            SelectQueryScreen(select_query, manager, self.music_engine))
        
        #manager.add_widget(
        #    ResultScreen(show_result, manager, self.music_engine))
        return manager


def run_gui():
    MainApp().run()
