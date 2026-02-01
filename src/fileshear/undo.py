import os
from pathlib import Path
import re

def undo_archival(root, args):
    """
    Undoes archival operations by moving files from the archive directory
    back to their original location.
    
    :param root: Root directory where archival was performed
    :param args: Parsed command-line arguments
    """
    archive_pattern = "ShearArchive" + "_" + re.compile(r"\d{4}-\d{2}-\d{2}").pattern
    archive_path = None
    for child in root.iterdir():
        if child.is_dir() and re.match(archive_pattern, child.name):
            archive_path = child
            break
    if not archive_path:
        print("No archive directory found to undo.")
        return
    
    for archived_file in archive_path.iterdir():
        original_path = root / archived_file.name
        if args.dryrun:
            print(f"[Dry Run] Would restore: {archived_file} to {original_path}")
        else:
            os.rename(archived_file, original_path)
            if args.verbose:
                print(f"Restored {archived_file} to {original_path}")
            elif args.confirm:
                print(f"Confirmed restoration of {archived_file}")
    if not any(archive_path.iterdir()):
        archive_path.rmdir()
        if args.verbose:
            print(f"Removed empty archive directory: {archive_path}")