# FileShear

FileShear is a Python-based automation tool designed to safely perform bulk file cleanup operations according to user-defined rules. It targets workflows where directories accumulate many redundant or outdated file versions and manual cleanup becomes time-consuming and error-prone.

* Primary goal: Reduce manual effort and risk by **automatically** identifying files to archive or delete while enforcing **strict safety guarantees**.

## Modes Of Operation

* Whitelist Mode: A user specifies files in the working directory they'd like to keep, then the rest are deleted.

* Version Pruning: A user specifies a base filename or pattern, then all matches except the **most recent** version are deleted.

* Deletes based on _last modified_ timestamp by default, users can instead specify a "version pattern" to bias with.

* Note: Users can opt for relocation to an archive directory instead of deletion.

## Safety Guarantees

This program:

* Communicates the modifications that will be made by a user's input **before** execution.

* Requests user confirmation.

* Moves files to a new "ShearArchive" directory inside working directory.

* User can then choose to hard delete relocated files.

* Conforms to rigid directory boundaries (never recursing outside the specified root).

## Installation
```bash
pip install fileshear
```

or

```bash
pip3 install fileshear
```

## Example Usages

### Version Pruning
```bash
fileshear prune-versions --dir /Users/Documents/Resumes resume 
```

This command performs version pruning with file timestamps on files that start with "resume" in Users/Documents/Resumes.

```bash
fileshear prune-versions --dir /Users/Documents/ report essay grocerylist
```
This command performs version pruning with file timestamps on files that start with "report", "essay", or "grocerylist" in Users/Documents/.

```bash
fileshear prune-versions --dir /Users/Documents --pattern (report_)(\d)(.txt)
```
This command performs version pruning with file timestamps on files that follow the user-provided regular expression pattern.


### Whitelist
```bash
fileshear whitelist --dir /Users/Documents --keep report_v3.txt essay_v2.txt
```
This command performs whitelist archival on the directory, keeping only the files proceeded by the --keep flag.

### Undo
```bash
fileshear undo --dir /Users/Documents
```
This command undoes a previous archival in Users/Documents.
Note: the dir flag **_must_** also be used in this mode

### Additional Flags:

#### Confirm
```bash
fileshear prune-versions --dir /Users/Documents report --confirm
```
Skips user confirmation and takes archival actions immediately.

#### Verbose:
```bash
fileshear prune-versions --dir /Users/Documents report --verbose
```

Prints confirmation of archival to terminal.

#### Dry Run
```bash
fileshear whitelist --dir /Users/Documents --keep report_v2.txt --dryrun
```
Prints planned archival operations.
