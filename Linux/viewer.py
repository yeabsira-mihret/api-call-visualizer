# Usage: python3 viewer.py <pid>
import sys
import os
if len(sys.argv) != 2:
    print("Usage: viewer.py <pid>")
    sys.exit(1)
pid = sys.argv[1]
path = f"/tmp/apilog_{pid}.log"
if not os.path.exists(path):
    print("Log not found:", path)
    sys.exit(1)
with open(path, "r", errors="ignore") as f:
    print(f"API Call Sequence for PID {pid}:")
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) >= 2:
            token = parts[1]
            fn = token.split('(')[0]
            print(fn)
        else:
            print(line)
