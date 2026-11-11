
import os
import hashlib
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from Front import*

global l_action
l_action=[]

def apply(box):
    l_action.clear()
    g=box.get()
    l_action.append(g)

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
    directory = Path(target_path)
    
    # Track how many files were moved
    moved_count = 0

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
            print(f"Could not move {item.name}: {e}")

    print(f"Clean-up complete! Organized {moved_count} files.")



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



def clean_duplicate_files():
    """
    Opens a folder selection dialog, finds duplicate files using MD5 hashes,
    keeps the first discovered instance, and deletes all other copies.
    """
    # 1. Open the system's native folder picker
    root = tk.Tk()
    root.withdraw()  # Hide the main blank Tkinter window
    
    target_directory = filedialog.askdirectory(title="Select Folder to Clean Duplicates From")
    
    # 2. Trigger an alert popup if no folder was chosen
    if not target_directory:
        messagebox.showwarning(
            title="No Selection", 
            message="No folder was selected! The scan has been cancelled."
        )
        return

    print(f"Scanning and cleaning directory: {target_directory}...\n")
    
    # 3. Track files using a dictionary: { file_hash: [list_of_filepaths] }
    hashes_dict = {}
    
    # 4. Walk through all files and subfolders to map hashes
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

    # 5. Iterate through mapped files and delete extra instances
    deleted_count = 0
    space_saved = 0
    
    for file_hash, paths in hashes_dict.items():
        if len(paths) > 1:
            # Keep the very first file found as the original copy
            original = paths[0]
            duplicates_to_remove = paths[1:]
            
            for dup_path in duplicates_to_remove:
                try:
                    # Get file size before deleting to track total storage saved
                    file_size = os.path.getsize(dup_path)
                    
                    # Permanently delete the duplicate file
                    os.remove(dup_path)
                    
                    deleted_count += 1
                    space_saved += file_size
                except Exception as e:
                    print(f"  ⚠️ Error deleting {dup_path}: {e}")
                    
    # 6. Show the final result in a top-layer popup window
    if deleted_count == 0:
        messagebox.showinfo(
            title="Clean-up Complete", 
            message="🎉 Success! No duplicate files were found."
        )
    else:
        mb_saved = space_saved / (1024 * 1024)
        messagebox.showinfo(
            title="Clean-up Successful", 
            message=f"🧹 Clean-up complete!\n\n• Removed {deleted_count} duplicate files.\n• Recovered {mb_saved:.2f} MB of storage space."
        )


