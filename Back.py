
import os
import hashlib
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
global o
o=[]
global l_action
l_action=[]
global l_path
l_path=[]

def slect(entry):
    entry.delete(0,tk.END)
    z=select_directory()
    entry.insert(0, str(z))

def apply(combobox,entry):
    l_action.clear()
    g=combobox.get()
    l_action.append(g)

    l_path.clear()
    g=entry.get()
    l_path.append(g)

def show_native_popups():
    # Create the root window and hide it immediately
    # This prevents an empty background panel from appearing on your screen
    root = tk.Tk()
    root.withdraw()
    
    # 1. Informational Popup Window
    messagebox.showinfo(
        title="Operation Successful",
        message="🎉 Your process completed without any errors!"
    )
    
    # 2. Warning Alert Popup Window
    messagebox.showwarning(
        title="Action Required",
        message="⚠️ No directory was selected. Please choose a folder."
    )
    
    # 3. Error Popup Window
    messagebox.showerror(
        title="System Error",
        message="❌ Critical Error: Unable to access system files."
    )

def clean_and_organize_directory(target_path):
    if not target_path:
            messagebox.showwarning(
                title="No Selection",
                message="No folder was selected! The scan has been cancelled."
            )
            return []
    directory = Path(target_path)
    
    # Track how many files were moved
    moved_count = 0
    directory_count=1

    for item in directory.iterdir():
        # Skip directories to avoid organizing already-sorted folders
        if item.is_dir():
            continue
            
        # Get the file extension (e.g., '.pdf', '.png') without the dot, in uppercase
        file_ext = item.suffix.strip('.').upper()
        
        # If the file has no extension, group it into an 'UNKNOWN' folder
        if not file_ext:
            file_ext = "UNKNOWN"
            
        # Define the target subfolder path (e.g., ./Documents/PDF)
        destination_folder = directory / file_ext
        
        # Create the subfolder if it doesn't exist yet
        destination_folder.mkdir(exist_ok=True)
        
        # Move the file into the new subfolder
        try:
            shutil.move(str(item), str(destination_folder / item.name))
            moved_count += 1
        except Exception as e:
            messagebox.showerror(
                            title="Error",
                            message=(f"Could not move {item.name}: {e}")
                        )
    messagebox.showinfo(
                title="Sorting Complete",
                message="🎉 Success! All Files were Sorted."
            )
    return moved_count


def delete_files(file_paths: list[str | Path]) -> None:
    """Deletes a list of files safely and shows a single summary pop-up alert."""
    # Create a hidden root window so only the pop-up box appears
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)  # Keeps pop-ups on top of other windows

    try:
        if not file_paths:
            messagebox.showwarning("Warning", "NOOOOOOOO")
            return

        deleted = []
        skipped = []
        errors = []

        for path in file_paths:
            file = Path(path)
            try:
                file.unlink(missing_ok=True)
                deleted.append(str(file))
            except IsADirectoryError:
                skipped.append(f"{file} (is a directory, not a file)")
            except PermissionError:
                errors.append(f"{file} (permission denied)")
            except Exception as e:
                errors.append(f"{file} ({e})")

        # Build the single summary message
        summary_lines = []
        if deleted:
            summary_lines.append("Deleted:\n" + "\n".join(f"• {f}" for f in deleted))
        if skipped:
            summary_lines.append("Skipped:\n" + "\n".join(f"• {f}" for f in skipped))
        if errors:
            summary_lines.append("Errors:\n" + "\n".join(f"• {f}" for f in errors))

        summary_message = "\n\n".join(summary_lines)

        # Show one final pop-up based on whether any errors/warnings occurred
        if errors:
            messagebox.showerror("Deletion Complete (with errors)", summary_message)
        elif skipped:
            messagebox.showwarning("Deletion Complete (with warnings)", summary_message)
        else:
            messagebox.showinfo("Success", summary_message)

    finally:
        # Clean up the hidden window when finished
        root.destroy()


def select_directory():
    # Create a hidden root window to prevent an empty GUI window from flashing
    root = tk.Tk()
    root.withdraw()

    # Open the directory browser dialog
    directory_path = filedialog.askdirectory(
        title="Select a Folder/Directory"
    )

    if directory_path:
        return directory_path
    else:
        print("No folder was selected.")
        return None

def The_Sorter(x,path):
    for widget in x.winfo_children():
            widget.destroy()
    a=clean_and_organize_directory(path)
    moved_count_label=tk.Label(x,text=(f"No.of Files moved {a}"))
    moved_count_label.pack()
    

def scan(listbox, target_directory):
    o.clear()
    o.extend(find_duplicate_files(target_directory))
    for item in o:
        listbox.insert(tk.END, item)




def find_duplicate_files(target_directory):
    if not target_directory:
        messagebox.showwarning(
            title="No Selection",
            message="No folder was selected! The scan has been cancelled."
        )
        return []

    print(f"Scanning directory for duplicates: {target_directory}...\n")

    # Track files using a dictionary: { file_hash: [list_of_filepaths] }
    hashes_dict = {}

    # Walk through all files and subfolders to map hashes
    for root_dir, _, files in os.walk(target_directory):
        for file in files:
            full_path = os.path.join(root_dir, file)
            if not os.path.exists(full_path):
                continue

            try:
                # Read file in chunks to keep memory usage low
                hasher = hashlib.md5()
                with open(full_path, 'rb') as f:
                    while chunk := f.read(8192):
                        hasher.update(chunk)
                file_hash = hasher.hexdigest()

                if file_hash in hashes_dict:
                    hashes_dict[file_hash].append(full_path)
                else:
                    hashes_dict[file_hash] = [full_path]

            except (PermissionError, FileNotFoundError):
                continue

    # Collect all extra duplicate instances into a list
    duplicate_files = []
    wasted_space = 0

    for file_hash, paths in hashes_dict.items():
        if len(paths) > 1:
            # Skip paths[0] (the original) and grab all extra copies
            duplicates = paths[1:]
            duplicate_files.extend(duplicates)

            # Calculate wasted space without deleting anything
            for dup_path in duplicates:
                try:
                    wasted_space += os.path.getsize(dup_path)
                except OSError:
                    pass

    # Show the final result in a popup window
    if not duplicate_files:
        messagebox.showinfo(
            title="Scan Complete",
            message="🎉 Success! No duplicate files were found."
        )
    else:
        mb_wasted = wasted_space / (1024 * 1024)
        messagebox.showinfo(
            title="Scan Complete",
            message=f"🔍 Scan complete!\n\n• Found {len(duplicate_files)} duplicate files.\n• Taking up {mb_wasted:.2f} MB of extra space."
        )

    return duplicate_files



