import unittest
from xml.etree.ElementTree import indent
from fileshear.scanner import scan_for_archival
from pathlib import Path
import tempfile
import time
from textwrap import indent
from io import StringIO
import sys
import os
import shutil
import re

class TestScanner(unittest.TestCase):
   def format_message(self, src, args, expected, actual, extra = ""):
      msg = f"In {src}:\n"
      if args is not None:
         msg += f"I passed \"{args}\""
      if expected is not None and actual is not None:
         msg += "\nI expected:\n"
         msg += indent(expected, "    ")
         msg += "\nBut I saw:\n"
         msg += indent(actual, "    ")
      if extra:
         msg += "\n" + extra
      return msg
   
   def setUp(self):
      # Create a temporary directory for testing
      self.test_dir = tempfile.mkdtemp()
      self.test_path = Path(self.test_dir)
      
   def tearDown(self):
      # Clean up the temporary directory
      shutil.rmtree(self.test_dir, ignore_errors=True)
   
   def test_whitelist_scanner(self):
      # Create test files
      filenames = ["file1.txt", "file2.txt", "file3.log", ".DS_Store"]
      for fname in filenames:
         (self.test_path / fname).touch()
      
      # Define keep list
      keep_list = ["file1.txt", "file3.log"]
      
      # Scan for archival
      class Args:
         command = "whitelist"
         dir = self.test_dir
         keep = keep_list
      
      args = Args()
      archive = scan_for_archival(args)
      
      # Expected files to archive
      expected_archive = {self.test_path / "file2.txt"}
      
      actual_archive = set(archive)
      
      msg = self.format_message(
         src="test_whitelist_scanner",
         args=f"keep={keep_list}",
         expected="\n".join(str(p) for p in expected_archive),
         actual="\n".join(str(p) for p in actual_archive)
      )
      
      self.assertEqual(expected_archive, actual_archive, msg)
      
   def test_whitelist_scanner_no_keep(self):
      # Create test files
      filenames = ["file1.txt", "file2.txt", "file3.log", ".DS_Store"]
      for fname in filenames:
         (self.test_path / fname).touch()
      
      # Define empty keep list
      keep_list = []
      
      # Scan for archival
      class Args:
         command = "whitelist"
         dir = self.test_dir
         keep = keep_list
      
      args = Args()
      archive = scan_for_archival(args)
      
      # Expected files to archive (all except .DS_Store)
      expected_archive = {self.test_path / "file1.txt",
                          self.test_path / "file2.txt",
                          self.test_path / "file3.log"}
      
      actual_archive = set(archive)
      
      msg = self.format_message(
         src="test_whitelist_scanner_no_keep",
         args=f"keep={keep_list}",
         expected="\n".join(str(p) for p in expected_archive),
         actual="\n".join(str(p) for p in actual_archive)
      )
      
      self.assertEqual(expected_archive, actual_archive, msg)
      
   def test_whitelist_scanner_all_keep(self):
      # Create test files
      filenames = ["file1.txt", "file2.txt", "file3.log", ".DS_Store"]
      for fname in filenames:
         (self.test_path / fname).touch()
      
      # Define keep list with all files
      keep_list = ["file1.txt", "file2.txt", "file3.log", ".DS_Store"]
      
      # Scan for archival
      class Args:
         command = "whitelist"
         dir = self.test_dir
         keep = keep_list
      
      args = Args()
      archive = scan_for_archival(args)
      
      # Expected files to archive (none)
      expected_archive = set()
      
      actual_archive = set(archive)
      
      msg = self.format_message(
         src="test_whitelist_scanner_all_keep",
         args=f"keep={keep_list}",
         expected="\n".join(str(p) for p in expected_archive),
         actual="\n".join(str(p) for p in actual_archive)
      )
      
      self.assertEqual(expected_archive, actual_archive, msg)
   
   def test_whitelist_scanner_non_file(self):
      # Create test files and a subdirectory
      filenames = ["file1.txt", "file2.txt"]
      for fname in filenames:
         (self.test_path / fname).touch()
      (self.test_path / "subdir").mkdir()
      
      # Define keep list
      keep_list = ["file1.txt"]
      
      # Scan for archival
      class Args:
         command = "whitelist"
         dir = self.test_dir
         keep = keep_list
      
      args = Args()
      archive = scan_for_archival(args)
      
      # Expected files to archive
      expected_archive = {self.test_path / "file2.txt"}
      
      actual_archive = set(archive)
      
      msg = self.format_message(
         src="test_whitelist_scanner_non_file",
         args=f"keep={keep_list}",
         expected="\n".join(str(p) for p in expected_archive),
         actual="\n".join(str(p) for p in actual_archive)
      )
      
      self.assertEqual(expected_archive, actual_archive, msg)
      
   def test_whitelist_scanner_empty_dir(self):
      # Scan for archival in empty directory
      class Args:
         command = "whitelist"
         dir = self.test_dir
         keep = []
      
      args = Args()
      archive = scan_for_archival(args)
      
      # Expected files to archive (none)
      expected_archive = set()
      
      actual_archive = set(archive)
      
      msg = self.format_message(
         src="test_whitelist_scanner_empty_dir",
         args="keep=[]",
         expected="\n".join(str(p) for p in expected_archive),
         actual="\n".join(str(p) for p in actual_archive)
      )
      
      self.assertEqual(expected_archive, actual_archive, msg)
      
   def test_whitelist_scanner_all_dsstore(self):
      # Create only .DS_Store files
      filenames = [".DS_Store", ".DS_Store"]
      for fname in filenames:
         (self.test_path / fname).touch()
      
      # Define empty keep list
      keep_list = []
      
      # Scan for archival
      class Args:
         command = "whitelist"
         dir = self.test_dir
         keep = keep_list
      
      args = Args()
      archive = scan_for_archival(args)
      
      # Expected files to archive (none)
      expected_archive = set()
      
      actual_archive = set(archive)
      
      msg = self.format_message(
         src="test_whitelist_scanner_all_dsstore",
         args=f"keep={keep_list}",
         expected="\n".join(str(p) for p in expected_archive),
         actual="\n".join(str(p) for p in actual_archive)
      )
      
      self.assertEqual(expected_archive, actual_archive, msg)
      
   def test_whitelist_scanner_similar_names(self):
      # Create test files with similar names
      filenames = ["file.txt", "file.txt.bak", "file.txt.old", ".DS_Store"]
      for fname in filenames:
         (self.test_path / fname).touch()
      
      # Define keep list
      keep_list = ["file.txt"]
      
      # Scan for archival
      class Args:
         command = "whitelist"
         dir = self.test_dir
         keep = keep_list
      
      args = Args()
      archive = scan_for_archival(args)
      
      # Expected files to archive
      expected_archive = {self.test_path / "file.txt.bak",
                          self.test_path / "file.txt.old"}
      
      actual_archive = set(archive)
      
      msg = self.format_message(
         src="test_whitelist_scanner_similar_names",
         args=f"keep={keep_list}",
         expected="\n".join(str(p) for p in expected_archive),
         actual="\n".join(str(p) for p in actual_archive)
      )
      
      self.assertEqual(expected_archive, actual_archive, msg)
   
   def test_whitelist_scanner_large_number_of_files(self):
      # Create a large number of test files
      num_files = 1000
      for i in range(num_files):
         (self.test_path / f"file{i}.txt").touch()
      
      # Define keep list for half the files
      keep_list = [f"file{i}.txt" for i in range(0, num_files, 2)]
      
      # Scan for archival
      class Args:
         command = "whitelist"
         dir = self.test_dir
         keep = keep_list
      
      args = Args()
      archive = scan_for_archival(args)
      
      # Expected files to archive (the other half)
      expected_archive = {self.test_path / f"file{i}.txt" for i in range(1, num_files, 2)}
      
      actual_archive = set(archive)
      
      msg = self.format_message(
         src="test_whitelist_scanner_large_number_of_files",
         args=f"keep=list of {len(keep_list)} files",
         expected="\n".join(str(p) for p in expected_archive),
         actual="\n".join(str(p) for p in actual_archive)
      )
      
      self.assertEqual(expected_archive, actual_archive, msg)
      
   def test_whitelist_scanner_special_characters(self):
      # Create test files with special characters
      filenames = ["file 1.txt", "file@2!.txt", "file#3$.log", ".DS_Store"]
      for fname in filenames:
         (self.test_path / fname).touch()
      
      # Define keep list
      keep_list = ["file 1.txt", "file#3$.log"]
      
      # Scan for archival
      class Args:
         command = "whitelist"
         dir = self.test_dir
         keep = keep_list
      
      args = Args()
      archive = scan_for_archival(args)
      
      # Expected files to archive
      expected_archive = {self.test_path / "file@2!.txt"}
      
      actual_archive = set(archive)
      
      msg = self.format_message(
         src="test_whitelist_scanner_special_characters",
         args=f"keep={keep_list}",
         expected="\n".join(str(p) for p in expected_archive),
         actual="\n".join(str(p) for p in actual_archive)
      )
      
      self.assertEqual(expected_archive, actual_archive, msg)
      
   def test_whitelist_scanner_nested_directories(self):
      # Create test files and nested directories
      (self.test_path / "subdir").mkdir()
      filenames = ["file1.txt", "subdir/file2.txt", "subdir/file3.log", ".DS_Store"]
      for fname in filenames:
         (self.test_path / fname).touch()
      
      # Define keep list
      keep_list = ["file1.txt", "file3.log"]
      
      # Scan for archival
      class Args:
         command = "whitelist"
         dir = self.test_dir
         keep = keep_list
      
      args = Args()
      archive = scan_for_archival(args)
      
      # Expected files to archive (only file2.txt, as others are in keep list or .DS_Store)
      expected_archive = {self.test_path / "subdir" / "file2.txt"}
      
      actual_archive = set(archive)
      
      msg = self.format_message(
         src="test_whitelist_scanner_nested_directories",
         args=f"keep={keep_list}",
         expected="\n".join(str(p) for p in expected_archive),
         actual="\n".join(str(p) for p in actual_archive)
      )
      
      self.assertEqual(expected_archive, actual_archive, msg)
      
   def test_whitelist_scanner_case_sensitivity(self):
      # Create test files with varying cases
      filenames = ["File1.txt", "file2.TXT", "FILE3.log", ".DS_Store"]
      for fname in filenames:
         (self.test_path / fname).touch()
      
      # Define keep list (case-sensitive)
      keep_list = ["File1.txt", "FILE3.log"]
      
      # Scan for archival
      class Args:
         command = "whitelist"
         dir = self.test_dir
         keep = keep_list
      
      args = Args()
      archive = scan_for_archival(args)
      
      # Expected files to archive
      expected_archive = {self.test_path / "file2.TXT"}
      
      actual_archive = set(archive)
      
      msg = self.format_message(
         src="test_whitelist_scanner_case_sensitivity",
         args=f"keep={keep_list}",
         expected="\n".join(str(p) for p in expected_archive),
         actual="\n".join(str(p) for p in actual_archive)
      )
      
      self.assertEqual(expected_archive, actual_archive, msg)
      
   def test_prune_versions_scanner_no_patterns(self):
      filenames = ["file_v1.txt", "file_v2.txt", "file_v3.txt"]
      for fname in filenames:
         time.sleep(1)  # Ensure different modification times
         (self.test_path / fname).touch()
      # Scan for archival
      class Args:
         command = "prune-versions"
         dir = self.test_dir
         base = ["file"]
         pattern = None
         strategy = "mtime"
      args = Args()
      archive = scan_for_archival(args)
      # Expected files to archive (all but the most recent)
      expected_archive = {self.test_path / "file_v1.txt",
                          self.test_path / "file_v2.txt"}
      actual_archive = set(archive)
      msg = self.format_message(
         src="test_prune_versions_scanner_no_patterns",
         args=f"base={args.base}, strategy={args.strategy}",
         expected="\n".join(str(p) for p in expected_archive),
         actual="\n".join(str(p) for p in actual_archive)
      )
      self.assertEqual(expected_archive, actual_archive, msg)
   
   def test_prune_versions_scanner_with_patterns(self):
      filenames = ["doc_1.0.txt", "doc_1.1.txt", "doc_2.0.txt"]
      for fname in filenames:
         time.sleep(1)  # Ensure different modification times
         (self.test_path / fname).touch()
      # Scan for archival
      class Args:
         command = "prune-versions"
         dir = self.test_dir
         base = []
         pattern = [r"(doc_)(\d+\.\d+)(\.txt)"]
         strategy = "mtime"
      args = Args()
      archive = scan_for_archival(args)
      # Expected files to archive (all but the most recent)
      expected_archive = {self.test_path / "doc_1.0.txt",
                          self.test_path / "doc_1.1.txt"}
      actual_archive = set(archive)
      msg = self.format_message(
         src="test_prune_versions_scanner_with_patterns",
         args=f"pattern={args.pattern}, strategy={args.strategy}",
         expected="\n".join(str(p) for p in expected_archive),
         actual="\n".join(str(p) for p in actual_archive)
      )
      self.assertEqual(expected_archive, actual_archive, msg)
      
   def test_prune_versions_scanner_semantic_strategy(self):
      filenames = ["app-1.0.0.bin", "app-1.0.1.bin", "app-1.1.0.bin"]
      for fname in filenames:
         time.sleep(1)  # Ensure different modification times
         (self.test_path / fname).touch()
      # Scan for archival
      class Args:
         command = "prune-versions"
         dir = self.test_dir
         base = []
         pattern = [r"(app-)(\d+\.\d+\.\d+)(\.bin)"]
         strategy = "semantic"
      args = Args()
      archive = scan_for_archival(args)
      # Expected files to archive (all but the most recent)
      expected_archive = {self.test_path / "app-1.0.0.bin",
                          self.test_path / "app-1.0.1.bin"}
      actual_archive = set(archive)
      msg = self.format_message(
         src="test_prune_versions_scanner_semantic_strategy",
         args=f"pattern={args.pattern}, strategy={args.strategy}",
         expected="\n".join(str(p) for p in expected_archive),
         actual="\n".join(str(p) for p in actual_archive)
      )
      self.assertEqual(expected_archive, actual_archive, msg)
   
   def test_prune_versions_scanner_no_versions(self):
      filenames = ["readme.txt", "config.yaml", "data.csv"]
      for fname in filenames:
         (self.test_path / fname).touch()
      # Scan for archival
      class Args:
         command = "prune-versions"
         dir = self.test_dir
         base = ["readme"]
         pattern = None
         strategy = "mtime"
      args = Args()
      archive = scan_for_archival(args)
      # Expected files to archive (none)
      expected_archive = set()
      actual_archive = set(archive)
      msg = self.format_message(
         src="test_prune_versions_scanner_no_versions",
         args=f"base={args.base}, strategy={args.strategy}",
         expected="\n".join(str(p) for p in expected_archive),
         actual="\n".join(str(p) for p in actual_archive)
      )
      self.assertEqual(expected_archive, actual_archive, msg)
      
   def test_prune_versions_scanner_mixed_files(self):
      filenames = ["img_v1.png", "img_v2.png", "doc.txt", "notes.md"]
      for fname in filenames:
         time.sleep(1)  # Ensure different modification times
         (self.test_path / fname).touch()
      # Scan for archival
      class Args:
         command = "prune-versions"
         dir = self.test_dir
         base = ["img"]
         pattern = None
         strategy = "mtime"
      args = Args()
      archive = scan_for_archival(args)
      # Expected files to archive (all but the most recent img)
      expected_archive = {self.test_path / "img_v1.png"}
      actual_archive = set(archive)
      msg = self.format_message(
         src="test_prune_versions_scanner_mixed_files",
         args=f"base={args.base}, strategy={args.strategy}",
         expected="\n".join(str(p) for p in expected_archive),
         actual="\n".join(str(p) for p in actual_archive)
      )
      self.assertEqual(expected_archive, actual_archive, msg)
      
   def test_prune_versions_scanner_empty_dir(self):
      # Scan for archival in empty directory
      class Args:
         command = "prune-versions"
         dir = self.test_dir
         base = ["file"]
         pattern = None
         strategy = "mtime"
      args = Args()
      archive = scan_for_archival(args)
      # Expected files to archive (none)
      expected_archive = set()
      actual_archive = set(archive)
      msg = self.format_message(
         src="test_prune_versions_scanner_empty_dir",
         args=f"base={args.base}, strategy={args.strategy}",
         expected="\n".join(str(p) for p in expected_archive),
         actual="\n".join(str(p) for p in actual_archive)
      )
      self.assertEqual(expected_archive, actual_archive, msg)
      
   def test_prune_versions_scanner_no_matching_files(self):
      filenames = ["unrelated1.txt", "unrelated2.log"]
      for fname in filenames:
         (self.test_path / fname).touch()
      # Scan for archival
      class Args:
         command = "prune-versions"
         dir = self.test_dir
         base = ["file"]
         pattern = None
         strategy = "mtime"
      args = Args()
      archive = scan_for_archival(args)
      # Expected files to archive (none)
      expected_archive = set()
      actual_archive = set(archive)
      msg = self.format_message(
         src="test_prune_versions_scanner_no_matching_files",
         args=f"base={args.base}, strategy={args.strategy}",
         expected="\n".join(str(p) for p in expected_archive),
         actual="\n".join(str(p) for p in actual_archive)
      )
      self.assertEqual(expected_archive, actual_archive, msg)
      
   def test_prune_versions_scanner_single_version(self):
      filenames = ["single_v1.txt"]
      for fname in filenames:
         (self.test_path / fname).touch()
      # Scan for archival
      class Args:
         command = "prune-versions"
         dir = self.test_dir
         base = ["single"]
         pattern = None
         strategy = "mtime"
      args = Args()
      archive = scan_for_archival(args)
      # Expected files to archive (none)
      expected_archive = set()
      actual_archive = set(archive)
      msg = self.format_message(
         src="test_prune_versions_scanner_single_version",
         args=f"base={args.base}, strategy={args.strategy}",
         expected="\n".join(str(p) for p in expected_archive),
         actual="\n".join(str(p) for p in actual_archive)
      )
      self.assertEqual(expected_archive, actual_archive, msg)
   
   def test_prune_versions_scanner_overlapping_patterns(self):
      filenames = ["data_v1.txt", "data_v2.txt", "data_final.txt"]
      for fname in filenames:
         time.sleep(1)  # Ensure different modification times
         (self.test_path / fname).touch()
      # Scan for archival
      class Args:
         command = "prune-versions"
         dir = self.test_dir
         base = []
         pattern = [r"(data_)(\S+)(\.txt)"]
         strategy = "mtime"
      args = Args()
      archive = scan_for_archival(args)
      # Expected files to archive (all but the most recent)
      expected_archive = {self.test_path / "data_v1.txt",
                          self.test_path / "data_v2.txt"}
      actual_archive = set(archive)
      msg = self.format_message(
         src="test_prune_versions_scanner_overlapping_patterns",
         args=f"pattern={args.pattern}, strategy={args.strategy}",
         expected="\n".join(str(p) for p in expected_archive),
         actual="\n".join(str(p) for p in actual_archive)
      )
      self.assertEqual(expected_archive, actual_archive, msg)
      
if __name__ == "__main__":
   unittest.main()
      