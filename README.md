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
* Moves files to trash (or archive directory if specified) instead of hard deletion.
 *  User can then choose to hard delete relocated files.
* Conforms to rigid directory boundaries (never recursing outside the specified root).




