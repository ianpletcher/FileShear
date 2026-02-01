import unittest
from fileshear.main import validate_args
from fileshear.cli import parse_args
from pathlib import Path
import re
import tempfile
import os
import shutil

class TestCLI(unittest.TestCase):
    def format_message(self, args, expected_message, actual_message=None):
        msg = f"I passed {args}"
        if expected_message is not None:
            msg += f"\nExpected error message: {expected_message}"
        if actual_message is not None:
            msg += f"\nActual error message: {actual_message}"
        return msg
    
    def test_invalid_whitelist_args(self):
        args_list = [
            ["whitelist", "--dir", "/some/dir"],
            ["whitelist", "--dir", "/some/dir", "--keep"],
        ]
        expected_message = "At least one --keep pattern must be specified for whitelist command."

        for args in args_list:
            parsed_args = parse_args(args)
            with self.assertRaises(ValueError) as context:
                validate_args(parsed_args)
            actual_message = str(context.exception)
            self.assertEqual(expected_message, actual_message,
                             self.format_message(args, expected_message, actual_message))
            
    def test_invalid_prune_versions_args(self):
        args_list = [
            ["prune-versions", "--dir", "/some/dir"],
        ]
        expected_message = "Either base filenames or --pattern must be specified for prune-versions command."

        for args in args_list:
            parsed_args = parse_args(args)
            with self.assertRaises(ValueError) as context:
                validate_args(parsed_args)
            actual_message = str(context.exception)
            self.assertEqual(expected_message, actual_message,
                             self.format_message(args, expected_message, actual_message))
    
    def test_valid_whitelist_args(self):
        args = ["whitelist", "--dir", "/some/dir", "--keep", "file1.txt", "file2.txt"]
        parsed_args = parse_args(args)
        try:
            validate_args(parsed_args)
        except ValueError as e:
            self.fail(f"validate_args raised ValueError unexpectedly: {e}")
            
    def test_valid_prune_versions_args(self):
        args_variants = [
            ["prune-versions", "--dir", "/some/dir", "basefile1", "basefile2"],
            ["prune-versions", "--dir", "/some/dir", "--pattern", r"(basefile)(\d+)(\.txt)"],
        ]
        for args in args_variants:
            parsed_args = parse_args(args)
            try:
                validate_args(parsed_args)
            except ValueError as e:
                self.fail(f"validate_args raised ValueError unexpectedly for args {args}: {e}")

if __name__ == "__main__":
    unittest.main()