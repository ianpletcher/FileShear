import unittest
from fileshear.planner import plan_archive_operations
from pathlib import Path
import re
import tempfile
import os
import shutil

class TestPlanner(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Remove the temporary directory after tests
        shutil.rmtree(self.test_dir)

    def test_plan_archive_operations(self):
        # Create some dummy files to simulate archive candidates
        file_paths = [
            Path(self.test_dir) / "file1.txt",
            Path(self.test_dir) / "file2.txt",
            Path(self.test_dir) / "file3.txt"
        ]
        for file_path in file_paths:
            with open(file_path, 'w') as f:
                f.write("Dummy content")

        # Call the planner with the list of file paths
        plans = plan_archive_operations(file_paths)

        # Verify that the plans are as expected
        expected_plans = [f"Archive {file_path}" for file_path in file_paths]
        self.assertEqual(plans, expected_plans)

    def test_plan_archive_operations_no_candidates(self):
        # Call the planner with an empty list
        plans = plan_archive_operations([])

        # Verify that the planner indicates no files to archive
        self.assertEqual(plans, ["No files to archive."])
        
if __name__ == '__main__':
    unittest.main()