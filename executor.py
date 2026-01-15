import os
from pathlib import Path
from datetime import datetime

def execute_archival(archive, args):
    """
    Executes the archival of files based on the provided archive list and arguments.
    
    :param archive: List of Path objects to be archived
    :param args: Parsed command-line arguments
    """
    for file_path in archive:
        if args.dryrun:
            print(f"[Dry Run] Would archive: {file_path}")
        else:
            dir_name = "ShearArchive" + datetime.now().strftime("_%Y-%m-%d")
            archive_dir = Path(args.archive_dir) if args.archive_dir else Path(args.dir) / dir_name
            archive_dir.mkdir(parents=True, exist_ok=True)
            target_path = archive_dir / file_path.name
            os.rename(file_path, target_path)
            if args.verbose:
                print(f"Archived {file_path} to {target_path}")
            if args.confirm:
                print(f"Confirmed archival of {file_path}")
    if not archive:
        print("No files to archive.")
    