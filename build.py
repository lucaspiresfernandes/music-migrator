import os


ytMusicApiLocalePath = str(
    f'C:/Python311/Lib/site-packages/ytmusicapi/locales{os.pathsep}ytmusicapi/locales')

os.system(
    f'python -m PyInstaller --onefile ./migrator.py --add-data "{ytMusicApiLocalePath}"')
