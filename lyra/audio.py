import os

from subprocess import call


home = os.path.expanduser("~")
fifo = os.path.join(home, '.player-control')


class Player(object):
    def __init__(self, filepath):
        if not(os.path.exists(fifo)):
            call(['mkfifo', fifo])

        self.filepath = filepath

    def play(self):
        c = 'mplayer -slave -input file={}'.format(fifo)
        c = c.split(' ')
        c += [self.filepath]
        call(c)
    
    def pause(self):
        c = 'echo "pause" > {}'.format(fifo)
        call(c.split(' '))

    def quit(self):
        c = 'echo "quit" > {}'.format(fifo)
        call(c.split(' '))
