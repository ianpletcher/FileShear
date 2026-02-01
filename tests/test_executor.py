import unittest
from fileshear.executor import execute_archival
import tempfile
from pathlib import Path
import os
import shutil

class TestExecuteArchival(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
        
        # Create some test files
        (self.test_path / "file1.txt").write_text("This is file 1")
        (self.test_path / "file2.txt").write_text("This is file 2")
        (self.test_path / "file3.log").write_text("This is file 3")
        
        # Create a mock archive object
        self.archive = [Path(self.test_path / "file1.txt"), Path(self.test_path / "file2.txt")]
        
        # Mock args object
        self.args = type('Args', (object,), {})()
        self.args.dryrun = False
        self.args.archive_dir = None
        self.args.dir = str(self.test_path)
        self.args.verbose = True
        self.args.confirm = False

    def tearDown(self):
        # Remove the temporary directory after the test
        shutil.rmtree(self.test_dir)

    def test_execute_archival(self):
        # Execute archival
        execute_archival(self.archive, self.args)
        
        # Check that files were archived (moved)
        for file in self.archive:
            self.assertFalse(file.exists(), f"{file} should have been archived.")
        
        # Check that files were deleted
        for file in self.archive:
            self.assertFalse(file.exists(), f"{file} should have been deleted.")
            
    def test_execute_archival_dry_run(self):
        # Set dry run to True
        self.args.dryrun = True
        
        # Execute archival
        execute_archival(self.archive, self.args)
        
        # Check that files were not moved or deleted
        for file in self.archive:
            self.assertTrue(file.exists(), f"{file} should not have been archived in dry run.")
        
        for file in self.archive:
            self.assertTrue(file.exists(), f"{file} should not have been deleted in dry run.")
            
if __name__ == '__main__':
    unittest.main()