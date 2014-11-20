import sys
import os
import glob


import tkinter
from tkinter import WORD, LEFT, RIGHT, BOTH, END, RAISED
from tkinter import filedialog
from tkinter.ttk import Frame, Button, Style

from similarity import search_k_nearest
from extractor import Extractor
from featuresio import load_json, dump_json
from audio import Player
import utils


jsondir = 'jsonfiles'
icon_dir = 'music_icons'
#icon_play = os.path.join(icon_dir, 'circle_play.gif')
#icon_stop = os.path.join(icon_dir, 'circle_stop.gif')
#icon_pause = os.path.join(icon_dir, 'circle_pause.gif')


def search(query_filepath):
    dicts = []
    jsonpaths = os.path.join(jsondir, '*.json')
    for path in glob.glob(jsonpaths):
        dicts.append(load_json(path)) 
    path_feature_map = utils.merge_multiple_dicts(dicts)

    query_vector = path_feature_map[query_filepath]
    k_nearest = search_k_nearest(path_feature_map, query_vector)
    return k_nearest


class MusicBar(Frame):
    def __init__(self, parent, music_filepath):
        Frame.__init__(self, parent)
        self.player = Player(music_filepath)
        
        title = os.path.basename(music_filepath) 

        label = tkinter.Label(self, text=title, width=30)
        label.pack(side=LEFT)

        padx = 10
        #image = tkinter.PhotoImage(file=icon_play)
        play_button = Button(self, text="Play")#image=image)
        play_button.pack(side=LEFT, padx=padx)
        play_button.bind("<Button-1>", self.play)
        
        #image = tkinter.PhotoImage(file=icon_pause)
        pause_button = Button(self, text="Pause")#image=image)
        pause_button.pack(side=LEFT, padx=padx)
        pause_button.bind("<Button-1>", self.pause)
        
        #image = tkinter.PhotoImage(file=icon_stop)
        stop_button = Button(self, text="Stop")#image=image)
        stop_button.pack(side=LEFT, padx=padx)
        stop_button.bind("<Button-1>", self.stop)
 
        #MusicBar(self, music_filepath)

    def play(self, event):
        self.player.play()

    def stop(self, event):
        self.player.quit()

    def pause(self, event):
        self.player.pause()


class MusicList(tkinter.Toplevel):
    def __init__(self, parent):
        tkinter.Toplevel.__init__(self, parent)
    
    def append(self, music_filepath):
        bar = MusicBar(self, music_filepath)
        bar.pack()



class MainFrame(Frame): 
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent 

        self.music_root = ''
        self.query_path = ''
        self.extractor = Extractor(n_frames=40, 
                                   n_blocks=100, 
                                   learning_rate=0.00053,
                                   verbose=True)

        self.style = Style()
        self.style.theme_use("default")
        
        padx = 2
        pady = 2

        root_select_button = Button(self, text="Select a directory")
        root_select_button.pack(fill=tkinter.X, padx=padx, pady=pady)
        root_select_button.bind("<Button-1>", self.set_music_root)

        analyze_button = Button(self, text="Analyze")
        analyze_button.pack(fill=tkinter.X, padx=padx, pady=pady)
        analyze_button.bind("<Button-1>", self.analyze)

        query_select_button = Button(self, text="Select a file")
        query_select_button.pack(fill=tkinter.X, padx=padx, pady=pady)
        query_select_button.bind("<Button-1>", self.set_query_path)

        search_button = Button(self, text="Search similar songs")
        search_button.pack(fill=tkinter.X, padx=padx, pady=pady)
        search_button.bind("<Button-1>", self.search_music)
 
        self.pack(fill=BOTH, expand=1)

    def set_music_root(self, event):
        self.music_root = filedialog.askdirectory()

    def analyze(self, event):
        if(self.music_root == ''):
            #TODO show error dialog 
            print("Set a music directory first")
            return

        print("Analyzing")
        path_feature_map, error = self.extractor.extract(self.music_root)

        print("Saving")
        filename = os.path.basename(self.music_root)
        jsonpath = os.path.join(jsondir, '{}.json'.format(filename))

        dump_json(path_feature_map, jsonpath)

    def set_query_path(self, event):
        self.query_path = filedialog.askopenfilename(initialdir=self.music_root)

    def search_music(self, event):
        if(self.query_path == ''):
            #TODO show error dialog 
            print("Set a music file first")
            return
    
        k_nearest = search(self.query_path)

        music_list = MusicList(self)
        for path, vector in k_nearest:
            music_list.append(path)

def main(): 
    root = tkinter.Tk()
    app = MainFrame(root)
    root.mainloop()  


if __name__ == '__main__':
    main()
