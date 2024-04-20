import eel
import os
from tkinter import filedialog, Tk
import dreamcore

eel.init('web')


@eel.expose
def select_folder():
    dialog_root = Tk()
    dialog_root.attributes("-topmost", True)
    selected_files = []
    acceptable_formats = ['mp3']
    folder_path = filedialog.askdirectory()
    dialog_root.withdraw()

    for root, dirs, files in os.walk(folder_path):
        root_path = root
        for file in files:
            if any(file.endswith(fmt) for fmt in acceptable_formats):
                selected_files.append(file)
        break

    print("processing:")
    print(selected_files)
    return selected_files, root_path


@eel.expose
def process_selected_files(selected_files, root):
    results = []
    for file in selected_files:
        file_path = os.path.join(root, file)
        features = dreamcore.analyze(file_path)
        score = dreamcore.assess(features)
        results.append((file, score))
    return results


eel.start('index.html')
