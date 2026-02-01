import argparse
from . import __version__

def build_parser():
    parser = argparse.ArgumentParser(prog="fileshear")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--dir", required=True)
    common.add_argument("--dryrun", action="store_true")
    common.add_argument("--archive-dir")
    common.add_argument("--confirm", action="store_true")
    common.add_argument("--verbose", action="store_true")
    
    whitelist = subparsers.add_parser("whitelist", parents=[common])
    whitelist.add_argument("--keep", nargs="*", help="Filenames to keep (not archive)")
    
    prune = subparsers.add_parser("prune-versions",parents=[common])
    prune.add_argument("base", nargs="*", help = "Base filenames to identify versioned files")
    prune.add_argument("--pattern", nargs="+", help="Regex patterns to identify versioned files. Enter as '(base)(version)(ext)'.")
    prune.add_argument("--strategy",choices=["mtime","semantic"],default="mtime")

    undo = subparsers.add_parser("undo", parents=[common])
    
    return parser

def parse_args(args=None):
    parser = build_parser()
    return parser.parse_args(args)
