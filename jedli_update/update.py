import datetime
import os
import shutil
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
update_dir = os.path.join(current_dir, "exe.win-amd64-3.4")
main_dir = os.path.dirname(current_dir) # one level up
modules_dir = os.path.join(main_dir, "modules")
static_dir = os.path.join(main_dir, r"settings/static_files")
documentation_dir = os.path.join(main_dir, r"documentation")
backup_dir = os.path.join(current_dir, "backup_{:%Y-%m-%d}".format(datetime.date.today()))

##not_affected_folders_list = [os.path.join(main_dir, "checklists"),
##                             os.path.join(main_dir, "jedli_update"),
##                             os.path.join(main_dir, "search_results"),
##                             os.path.join(main_dir, "settings/saved_searches"),
##                             os.path.join(main_dir, "settings/source_selections"),
##                             os.path.join(main_dir, "settings/user_preferences"),
##                             os.path.join(main_dir, "tcl"),
##                             os.path.join(main_dir, "texts"),
##                             os.path.join(main_dir, "tk")]

not_affected_folders_list = ["checklists",
                             "jedli_update", 
                             "search_results",
                             "settings\\saved_searches",
                             "settings\\source_selections",
                             "settings\\user_preferences",
##                             "tcl",
##                             "tk",
                             "texts",
                             ]



def move_files(root, src, dst, not_affected_folders_list, remove=True):
    """Move all files in the root folder,
    which is a descendant of the src folder,
    to the corresponding folder in the dst folder.
    Exclude folders not affected by the update.
    This function is used both for the backup
    and the rollback of the backup.
    If remove is set to False, a copy will be kept in the original folder
    """
    print("root", root)
    for el in os.listdir(root):
        print("el", el)
        el_pth = os.path.join(root, el)
        if os.path.isdir(el_pth):
            if el_pth in not_affected_folders_list:
                print(el_pth, "will not be backed up")
            else:
                move_to_pth = el_pth.replace(src, dst)
                
                if not os.path.exists(move_to_pth):
                    os.makedirs(move_to_pth)
                    print("making folder", move_to_pth)
                move_files(el_pth, src, dst, not_affected_folders_list)
        else:
            move_to_pth = el_pth.replace(src, dst)
            if not os.path.exists(os.path.dirname(move_to_pth)):
                os.makedirs(os.path.dirname(move_to_pth))
            
            if remove:
                os.rename(el_pth, move_to_pth)
                print(el_pth, ">>", move_to_pth)
            else:
                print(el_pth, ">", move_to_pth)
                shutil.copy(el_pth, move_to_pth)

   

def delete_updated_files(root, not_affected_folders_list):
    empty = False
    removed_elements = 0
    original_len = len(os.listdir(root))
    print("root", root)
    for el in os.listdir(root):
        print("el", el)
        el_pth = os.path.join(root, el)
        print("el_pth", el_pth)
        if os.path.isdir(el_pth):
            if el_pth in not_affected_folders_list:
                print(el_pth, "will not be deleted")
            else:
                r = delete_updated_files(el_pth, not_affected_folders_list)
                if r:
                    removed_elements += 1
        else:
            removed_elements += 1
            print("removed", el_pth)
            os.remove(el_pth)

    if removed_elements == original_len:
        empty = True
        print("removing", root)
    else:
        print("removed {} elements of {}".format(removed_elements, original_len))

    try:
        os.rmdir(root)
    except OSError:
        print(root, "not empty")                
    return empty                

def safetycheck(main_dir):
    """Make sure the update folder is in the right folder,
    by checking if the main_dir directory contains a 'text' folder.
    If not, ask the user to manually locate the jedli_main.exe file
    (which is located in the main_dir)"""
    if "texts" in os.listdir(main_dir):
        return main_dir
    else:
        print("The update folder is not in the expected folder.")
##        print("Put the update folder in the main jedli folder")
##        print("(on the same level as the modules folder)")
        print("Select the jedli_main.exe file in the popup window")
        from tkinter.filedialog import askopenfilename
        from tkinter import Tk
        root = Tk()
        root.withdraw()
        main_dir = askopenfilename(title="Select the Jedli_main.exe file in the main Jedli folder (not the update folder)",
                               initialdir=main_dir, filetypes = [("executable files", ".exe")])
        main_dir = safetycheck(os.path.dirname(main_dir))
    return main_dir
         
def update(main_dir, backup_dir, update_dir, not_affected_folders_list):
    """Carry out the update"""
    main_dir = safetycheck(main_dir)
    if main_dir:
        print("Moving the original files from the affected folders to the backup folder")
        not_affected_folders_list1 = [os.path.join(main_dir, x) for x in not_affected_folders_list]
        move_files(main_dir, main_dir, backup_dir, not_affected_folders_list1)
        print("---"*10)
        print("Copying the update files to the relevant folders")
        not_affected_folders_list2 = [os.path.join(update_dir, x) for x in not_affected_folders_list]
        move_files(update_dir, update_dir, main_dir, not_affected_folders_list2, remove=False)
    else:
        print("Jedli was not able to carry out the update.")
    print("Finished installing the updates.")
    print("In case you encounter difficulties with the update,")
    print("you can roll back the update by clicking the rollback_update.py file")
    input('Press ENTER to exit ')


def rollback_update(main_dir, backup_dir, not_affected_folders_list):
    """delete the updated files
    and put the original files back in place"""
    main_dir = safetycheck(main_dir)
    if main_dir:

        if os.path.isdir(backup_dir):
            # 1. delete the updated files from the affected folders
            not_affected_folders_list1 = [os.path.join(main_dir, x) for x in not_affected_folders_list]
            print(not_affected_folders_list1)
            delete_updated_files(main_dir, not_affected_folders_list1)
            print("---"*10)
            # 2. move the files from the backup folder back to the main folder
            not_affected_folders_list2 = [os.path.join(update_dir, x) for x in not_affected_folders_list]
            move_files(backup_dir, backup_dir, main_dir, not_affected_folders_list2, remove=False)
        else:
            print(backup_dir)
            print("no backup directory found from which to restore Jedli's pre-update state")
    print("finished rolling back the updates.")
    input('Press ENTER to exit')


    
    


##sys.path.append(modules_dir)
##import jedli_global
##try:
##    if jedli_global.version != "1.2":
##        update()
##    else:
##        print("Jedli is up to date: version 1.2")
##except:
##    update()


if __name__ == "__main__":
    update(main_dir, backup_dir, update_dir, not_affected_folders_list)
