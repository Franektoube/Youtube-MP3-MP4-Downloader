import os
import sys
import tkinter as tk
from tkinter import filedialog
from pytube import YouTube
from moviepy.editor import *

def select_txt_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Wybierz plik txt", filetypes=[("Text files", "*.txt")])
    return file_path

def select_drive():
    drives = get_available_drives()
    root = tk.Tk()
    root.withdraw()
    drive = filedialog.askdirectory(title="Wybierz dysk do zapisu")
    return drive

def get_available_drives():
    drives = []
    for drive in range(65, 91):
        drive_letter = chr(drive)
        if os.path.exists(f"{drive_letter}:\\"):
            drives.append(f"{drive_letter}:")
    return drives

def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def download_and_convert(url, download_path):
    try:
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path=download_path)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        audioclip = AudioFileClip(out_file)
        audioclip.write_audiofile(new_file)
        audioclip.close()
        os.remove(out_file)
        print(f"Pobrano i skonwertowano: {yt.title}")
    except Exception as e:
        print(f"Błąd przy pobieraniu {url}: {e}")

def main():
    txt_file = select_txt_file()
    if not txt_file:
        print("Nie wybrano pliku txt. Zamykanie programu.")
        sys.exit()

    selected_drive = select_drive()
    download_directory = os.path.join(selected_drive, "youtube-download")
    create_directory_if_not_exists(download_directory)

    with open(txt_file, 'r') as file:
        urls = file.readlines()

    for url in urls:
        url = url.strip()
        if url:
            download_and_convert(url, download_directory)

    print("Pobieranie i konwersja zakończone.")

if __name__ == "__main__":
    main()
