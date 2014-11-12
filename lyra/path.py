import os


def get_wave_paths(music_root):
    paths = []
    for dirpath, dirname, filenames in os.walk(music_root):
        for filename in filenames:
            if not(filename.endswith('.wav') or filename.endswith('.wave')):
                continue
            filepath = os.path.join(dirpath, filename)
            paths.append(filepath)
    return paths
