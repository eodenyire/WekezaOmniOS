Rule 5 — Everything Must Be Observable

Systems software must produce logs.

Add structured logging.

logs/

teleport.log
capture.log
restore.log

Example log:

[2026-03-07 18:21:09]
Process 1821 checkpoint created
Snapshot size: 123MB

Logging will save you during debugging.
