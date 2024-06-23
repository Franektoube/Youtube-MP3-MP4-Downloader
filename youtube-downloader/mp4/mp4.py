import os
import sys
import tkinter as tk
from tkinter import filedialog
from pytube import YouTube

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

def download_video(url, download_path):
    try:
        yt = YouTube(url)
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        video_file = video_stream.download(output_path=download_path)
        print(f"Pobrano video: {yt.title}")
    except Exception as e:
        print(f"Błąd przy pobieraniu video {url}: {e}")

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
            download_video(url, download_directory)

    print("Pobieranie zakończone.")

if __name__ == "__main__":
    main()
