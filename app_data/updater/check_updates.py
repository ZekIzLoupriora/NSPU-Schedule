import zipfile
import tempfile
import os
import shutil
import filecmp
import sys
import requests
import json


#* Removing and replacing old files (with some exceptions to user data) *#
#* All user data must be specified in EXCLUDED_FILES & EXCLUDED_FOLDERS *#
def update_app(source_dir, destination_dir, EXCLUDED_FILES = None, EXCLUDED_FOLDERS = None):

    if not EXCLUDED_FILES:
        EXCLUDED_FILES = [
            "notes.txt",
            ]

    if not EXCLUDED_FOLDERS:
        EXCLUDED_FOLDERS = [
            "app_data\\updater",
            "user_data",
            ]

    #* Create a temporary directory to download and unzip source to *#
    with tempfile.TemporaryDirectory(dir=os.getcwd()) as tmp:

        #* Check if repo has any updates (if hash has changed) *#
        #commit_data = requests.get("https://api.github.com/repos/ZekIzLoupriora/NSPU-Schedule/commits",
        #                           headers={
        #                               "Accept": "application/vnd.github+json",
        #                               "Authorization": "Bearer YOUR_TOKEN"
        #                            })
        commit_data = requests.get("https://api.github.com/repos/ZekIzLoupriora/NSPU-Schedule/commits")
        last_commit_hash = commit_data.json()[0]["sha"]

        #* Get commit hash from the last app update *#
        if os.path.exists("last_update.json"):
            with open("last_update.json", "r") as f:
                data = json.load(f)
            old_commit_hash = data["last_commit_hash"]
        else:
            with open("last_update.json", "w") as f:
                json.dump({"last_commit_hash": ""}, f)
            old_commit_hash = ""

        #* Compare the two *#
        if last_commit_hash == old_commit_hash:
            print("There are no updates available!")
            sys.exit(0)
            
        
        #* Get last built source from GitHub *#
        response = requests.get('https://github.com/ZekIzLoupriora/NSPU-Schedule/archive/refs/heads/main.zip')
        with open(f"{tmp}/main.zip", "wb") as f:
            f.write(response.content)
        
        #* Extracting an archive to a temporary directory *# 
        with zipfile.ZipFile(f"{tmp}/main.zip", "r") as zip_ref:
            zip_ref.extractall(tmp)


        root_src_dir = f"{tmp}/{source_dir}"
        root_dst_dir = destination_dir

        #* Replacing old files with the new ones *#
        for src_dir, dirs, files in os.walk(root_src_dir):
            dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
                
            for file_ in files:
                if file_ not in EXCLUDED_FILES:
                    src_file = os.path.join(src_dir, file_)
                    dst_file = os.path.join(dst_dir, file_)

                    #* Replacing old files with the new ones *#
                    if os.path.exists(dst_file):
                        #* If files aren't equal *#
                        if not filecmp.cmp(src_file, dst_file):
                            try:
                                os.remove(dst_file)
                            except PermissionError as exc:
                                os.chmod(dst_file, stat.S_IWUSR)
                                os.remove(dst_file)

                            shutil.copy(src_file, dst_dir)
                            
                    #* Adding new files *#
                    else:
                        shutil.copy(src_file, dst_dir)


        #* Replace old hash value with the new one *#
        with open("last_update.json", "r+") as f:
            data = json.load(f)
            data["last_commit_hash"] = last_commit_hash
            #* Clearing the file for new data #*
            f.truncate(0)
            f.seek(0)
            json.dump(data, f)

                
update_app(source_dir = "NSPU-Schedule-main", destination_dir = "../../../main")
