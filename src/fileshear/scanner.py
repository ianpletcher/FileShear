from pathlib import Path
import re
from .undo import undo_archival


def scan_for_archival(args):
    """
    Entry point for scanner.
    Returns a list of Path objects representing files to be archived.
    
    :param args: Parsed command-line arguments
    :return: List of Path objects to archive
    """
    
    root = Path(args.dir)
    archive_candidates = []

    if args.command == "whitelist":
        archive_candidates = _scan_whitelist(root, args.keep)
        print(f"Keep list: {args.keep}")

    elif args.command == "prune-versions":
        if args.pattern:
            archive_candidates = _scan_prune_versions(
                root=root,
                patterns=(args.pattern),
                strategy=args.strategy,
            )
        else:
            base = args.base
            patterns = []
            for b in base:
                esc_base = re.escape(b)
                pattern = f"({esc_base})"
                print("Generated pattern:", pattern)
                patterns.append(pattern)
            
            archive_candidates = _scan_prune_versions(
                root=root,
                patterns=patterns,
                strategy=args.strategy,
            )
    return archive_candidates


def _scan_whitelist(root: Path, keep_list):
    """
    Archive all files in root that are NOT in the keep list.
    
    :param root: Directory to scan
    :param keep_list: List of filenames to keep
    :return: List of Path objects to archive
    """
    # Normalize keep list to filenames for comparison
    keep_set = set(keep_list)
    keep_set.add(".DS_Store")  # Always keep .DS_Store files
    archive = []

    for child in root.iterdir():
        if child.is_dir():
            sub_archives = _scan_whitelist(child, keep_list)
            archive.extend(sub_archives)
            continue
        
        if not child.is_file():
            continue

        if child.name not in keep_set:
            archive.append(child)

    return archive


def _scan_prune_versions(root: Path, patterns: list, strategy: str):
    """
    Identify versioned files matching a regex pattern and
    archive all but the most recent version per group.
    
    :param root: Directory to scan
    :param pattern: Regex pattern with capture groups for version families
    :param strategy: Strategy for determining most recent version ("mtime" or "semantic")
    :return: List of Path objects to archive
    """
    regexes = [re.compile(p) for p in patterns]
    version_groups = {}
    archive = []
    
    for regex in regexes:
        version_groups.clear()
        for child in root.iterdir():
            if not child.is_file():
                continue

            match = regex.match(child.name)
            if not match:
                continue

            # Expect at least one capture group to define the version family
            try:
                group_key = match.group(1)
            except IndexError:
                raise ValueError(
                    "Regex pattern must include at least one capture group "
                    "to identify version families."
                )

            version_groups.setdefault(group_key, []).append(child)
            
        for files in version_groups.values():
            if len(files) <= 1:
                continue
            
            if strategy == "mtime":
                files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                if ".DS_Store" in [f.name for f in files]:
                    files.sort(key=lambda p: p.name == ".DS_Store")

            elif strategy == "semantic":
                files.sort(
                    key=lambda p: [
                        int(part) for part in re.findall(r"\d+", p.name)
                    ],
                    reverse=True,
                )

            # Keep the first (most recent), archive the rest
            archive.extend(files[1:])

    return archive
