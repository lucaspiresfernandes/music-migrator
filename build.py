import os

ytMusicApiLocalePath = 'C:/Python311/Lib/site-packages/ytmusicapi/locales;ytmusicapi/locales'

os.system(
    f'python -m PyInstaller --onefile ./migrator.py --add-data "{ytMusicApiLocalePath}"')
