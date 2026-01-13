import sys
from cli import parse_args

def main():
    try:
        args = parse_args()
        validate_args(args)
        print(f"Parsed arguments: {args}")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    
def validate_args(args):
    if args.command == "whitelist":
        if not args.keep or len(args.keep) == 0:
            raise ValueError("At least one --keep pattern must be specified for whitelist command.")
    elif args.command == "prune-versions":
        if not args.pattern:
            raise ValueError("--pattern is required for prune-versions command.")
        if args.strategy not in ["mtime", "semantic"]:
            raise ValueError("--strategy must be either 'mtime' or 'semantic'.")
    else:
        raise ValueError(f"Unknown command: {args.command}")
    return True

if __name__ == "__main__":
    main()
