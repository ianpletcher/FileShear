import sys
from cli import parse_args
from scanner import scan_for_archival
from planner import plan_archive_operations

def main():
    """
    Calls validate_args to ensure correctness of cli arguments. 
    Passes validated arguments to logic routines in other files.
    """
    try:
        args = parse_args()
        validate_args(args)
        print(f"Validated args {args}")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    archive = scan_for_archival(args)
    plans = plan_archive_operations(archive)
    print("Planned archive operations:")
    for plan in plans:
        print(plan)
    
    
    
def validate_args(args):
    """
    Validates command-line arguments based on the selected command.
    Returns True if validation passes.
    
    :param args: Parsed command-line arguments
    :raises ValueError: If validation fails
    """
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
