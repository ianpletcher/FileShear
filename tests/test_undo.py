import unittest
from fileshear.undo import undo_archival
import os
from pathlib import Path
import tempfile
import shutil

class TestUndoArchival(unittest.TestCase):
    def format_message(self, original_files, archived_files, restored_files, expected_restored_files):
        msg = f"Original files: {original_files}\n"
        msg += f"Archived files: {archived_files}\n"
        msg += f"Restored files: {restored_files}\n"
        msg += f"Expected restored files: {expected_restored_files}\n"
        return msg
    
    def test_undo_archival(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            archive_dir = root / "ShearArchive_2024-01-01"
            archive_dir.mkdir()
            
            original_files = ["file1.txt", "file2.txt", "file3.txt"]
            for filename in original_files:
                (root / filename).touch()
            
            # Simulate archival by moving files to archive directory
            archived_files = []
            for filename in original_files:
                src = root / filename
                dest = archive_dir / filename
                os.rename(src, dest)
                archived_files.append(dest)
            
            # Prepare args mock
            class Args:
                dryrun = False
                verbose = True
                confirm = False
            
            args = Args()
            
            # Perform undo archival
            undo_archival(root, args)
            
            # Check that files are restored
            restored_files = [str(root / filename) for filename in original_files]
            expected_restored_files = [str(root / filename) for filename in original_files]
            
            for filepath in restored_files:
                self.assertTrue(Path(filepath).exists(),
                                self.format_message(original_files, archived_files, restored_files, expected_restored_files))
            
            # Check that archive directory is removed
            self.assertFalse(archive_dir.exists(),
                             self.format_message(original_files, archived_files, restored_files, expected_restored_files))
            
    def test_undo_archival_dryrun(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            archive_dir = root / "ShearArchive_2024-01-01"
            archive_dir.mkdir()
            
            original_files = ["file1.txt", "file2.txt"]
            for filename in original_files:
                (root / filename).touch()
            
            # Simulate archival by moving files to archive directory
            for filename in original_files:
                src = root / filename
                dest = archive_dir / filename
                os.rename(src, dest)
            
            # Prepare args mock
            class Args:
                dryrun = True
                verbose = False
                confirm = False
            
            args = Args()
            
            # Perform undo archival
            undo_archival(root, args)
            
            # Check that files are NOT restored
            for filename in original_files:
                self.assertFalse((root / filename).exists(),
                                 f"File {filename} should not be restored in dry run.")
            
            # Check that archive directory still exists
            self.assertTrue(archive_dir.exists(),
                            "Archive directory should still exist in dry run.")
            
if __name__ == "__main__":
    unittest.main()