from kivy.uix.filechooser import FileChooserListView
from kivy.lang import Builder


Builder.load_string("""
<FileChooserDialog>:
    BoxLayout:
        orientation: "vertical"
        <FileChooser>:
            id: filechooser
        BoxLayout:
            size_hint_y: None
            height: 30
            Button:
                text: "cancel"
                on_release: root.cancel()
            Button:
                text: "load"
                on_release: root.load()
""")


class FileChooserDialog(BoxLayout):
    pass


class FileChooser(FileChooserListView):
    def __init__(self, on_selected_listener):
        """
        Parameters
        ----------
        on_selected_listener: function object
            on_selected_listener(path_to_selected_file) is called 
            when a file selected.
        """

        self.on_selected_listener = on_selected_listener 
        FileChooserListView.__init__(self)
        self.bind(selection=self.on_selected)

    def on_selected(self, obj, path):
        path = path[0]  # path is given as a list
        self.on_selected_listener(path)
