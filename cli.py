import argparse

def build_parser():
    parser = argparse.ArgumentParser(prog="fileshear")
    subparsers = parser.add_subparsers(dest="command",required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--dir", required=True)
    common.add_argument("--dryrun", action="store_true")
    common.add_argument("--archive-dir")
    common.add_argument("--confirm", action="store_true")
    common.add_argument("--verbose", action="store_true")
    
    whitelist = subparsers.add_parser("whitelist", parents=[common])
    whitelist.add_argument("--keep", nargs="+",required=True)
    
    prune = subparsers.add_parser("prune-versions",parents=[common])
    prune.add_argument("--pattern",required=True)
    prune.add_argument("--strategy",choices=["mtime","semantic"],default="mtime")
    
    return parser

def parse_args(args=None):
    parser = build_parser()
    return parser.parse_args(args)
