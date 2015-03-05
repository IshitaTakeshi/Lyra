from kivy.app import App
from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.listview import ListView, ListItemButton
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.listview import ListView
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView


from spacer import HorizontalSpacer, VerticalSpacer


window_size = (500, 350)
Window.size = window_size


first_selection = 'first_selection'
select_data_file = 'select_data_file'
select_music_root = 'select_music_root'
select_query = 'select_query'
show_result = 'result'


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


class SelectDataFileScreen(Screen):
    def __init__(self, name, manager):
        Screen.__init__(self, name=name)

        file_chooser = FileChooserListView(load=self.load_file) 

        button_layout = BoxLayout(orientation='horizontal', 
                                  size_hint=(1.0, 0.3), 
                                  spacing=30,
                                  padding=(10, 10, 10, 10))

        self.back_button = ChangeScreenButton(
            manager=manager,
            destination=first_selection,
            text="Back"
        )
        
        self.analyze_button = Button(
            text="Analyze"
        )
        self.analyze_button.bind(on_press=self.analyze)

        self.next_button = ChangeScreenButton(
            manager=manager, 
            destination=select_query,
            text="Next"
        )
        self.next_button.disabled = True

        button_layout.add_widget(self.back_button)
        button_layout.add_widget(self.analyze_button)
        button_layout.add_widget(self.next_button)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(file_chooser)
        layout.add_widget(button_layout)

        self.add_widget(layout)

    def analyze(self, instance):
        self.next_button.disabled = False

    def load_file(self, path, filepath):
        self.filepath = filepath[0]


class SelectQueryScreen(Screen):
    def __init__(self, name, manager):
        Screen.__init__(self, name=name)

        file_chooser = FileChooserListView(load=self.load_file) 


        button_layout = BoxLayout(orientation='horizontal', 
                                  size_hint=(1.0, 0.3), 
                                  spacing=30,
                                  padding=(10, 10, 10, 10))

        back_button = ChangeScreenButton(
            manager=manager,
            destination=first_selection,
            text="Back"
        )
       
        search_button = ChangeScreenButton(
            destination=show_result,
            manager=manager,
            text="Search",
        )

        spacer = HorizontalSpacer()

        button_layout.add_widget(back_button)
        button_layout.add_widget(search_button)
        button_layout.add_widget(spacer)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(file_chooser)
        layout.add_widget(button_layout)

        self.add_widget(layout)
    
    def load_file(self, path, filepath):
        self.filepath = filepath[0]


class PlayButton(Button):
    def __init__(self, music_title, **kwargs):
        Button.__init__(self, **kwargs)
        
        self.sound = SoundLoader.load(music_title)
        self.is_playing = False

    def play(self):
        self.sound.play()

    def stop(self):
        self.sound.stop()

    def on_press(self):
        Button.on_press(self)

        if(is_playing):
            self.stop()
        else:
            self.play()

        self.is_playing = not self.is_playing


class MusicRow(SelectableView, FloatLayout):
    def __init__(self, **kwargs):
        FloatLayout.__init__(self, **kwargs)

        layout = BoxLayout(orientation='horizontal')

        title_string = os.path.basename(filepath)
        title = Label(text=title_string)

        play_button = Button(
            text="play"
        )
        play_button.bind(self.play)

        layout.add_widget(title)
        layout.add_widget(play_button)

        self.add_widget(layout)


class ResultScreen(Screen):
    def __init__(self, name, manager):
        Screen.__init__(self, name=name) 

        list_item_args_converter = \
                lambda row_index, rec: {'text': rec['text'],
                                        'is_selected': rec['is_selected'],
                                        'size_hint_y': None,
                                        'height': 20}

        from fixtures import integers_dict

        dict_adapter = DictAdapter(sorted_keys=[str(i) for i in range(100)],
                                   data=integers_dict,
                                   args_converter=list_item_args_converter,
                                   cls=MusicRow)
        list_view = ListView(adapter=dict_adapter)

        back_button = ChangeScreenButton(
            manager=manager,
            destination=select_query,
            text="Search by a different song"
        )
        
        back_home_button = ChangeScreenButton(
            manager=manager,
            destination=select_query,
            text="Back to home"
        )

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
    def build(self):
        manager = ScreenManager()
        manager.add_widget(FirstSelectionScreen(first_selection, manager))
        manager.add_widget(SelectDataFileScreen(select_data_file, manager))
        manager.add_widget(SelectQueryScreen(select_query, manager))
        manager.add_widget(ResultScreen(show_result, manager))
        return manager

MainApp().run()
