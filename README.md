# API Call Visualizer

[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-blue)](https://github.com/yourname/api-call-visualizer)

> Cross-platform runtime API/function call tracer and visualizer for reverse-engineering and malware analysis learning.  
> Provides a lightweight LD_PRELOAD hook for Linux and an IAT-hooking DLL + injector for Windows. Designed as an **educational, offline** toolkit for dynamic analysis.

---

## Table of Contents

- [Overview](#overview)  
- [Why this project](#why-this-project)  
- [Features](#features)  
- [Architecture](#architecture)  
- [Quickstart — Linux (LD_PRELOAD)](#quickstart--linux-ld_preload)  
- [Quickstart — Windows (IAT hook + Injector)](#quickstart--windows-iat-hook--injector)  
- [Log format & interpretation](#log-format--interpretation)  
- [Security & safe use](#security--safe-use)  

---

## Overview

`API Call Visualizer` helps you observe the runtime behavior of binaries by intercepting commonly used file, network, and I/O functions, logging timestamped events for analysis and visualization.

This repository contains two platform-specific implementations:

- **Linux**: `hook.so` — a shared library that uses `LD_PRELOAD` to override libc functions (e.g., `open`, `read`, `write`, `connect`, `send`, `recv`) and logs activity to `/tmp/apilog_<pid>.log`.
- **Windows**: `hookdll.dll` + `injector.exe` — a DLL that performs basic IAT patching to intercept imports and an injector that launches a suspended process and injects the DLL. Logs are written to `C:\Temp\apilog_<pid>.log`.

> This is an educational prototype designed to be simple to build, extend, and analyze. It is **not** production-grade monitoring software.

---

## Why this project

- Demonstrates practical dynamic analysis techniques used in reverse engineering:
  - `LD_PRELOAD` hooking on Linux (userland function interception)
  - IAT patching and remote DLL injection on Windows (basic process instrumentation)
- Lightweight: logs human-readable, timestamped events suitable for building visualizers or feeding into analysis pipelines.
- Modular and extensible: add more hooks, integrate a real-time collector, or export graph outputs (DOT/JSON).

---

## Features

- Cross-platform prototypes:
  - Linux: `hook.so` (LD_PRELOAD) to trace libc-level calls
  - Windows: `hookdll.dll` (IAT patching) + `injector.exe`
- Logs: timestamped lines with function name, args preview, return values
- Simple viewer utilities (Linux: `viewer.py`, Windows: `viewer.exe`) to extract and print call sequences
- Safe demo program included for testing (non-malicious)
- Designed for RE learning, demos, and classroom use

---

## Architecture

| Target Process | <----> | Hook (SO/DLL) |
| (runs binary) | | - intercepts APIs |

| Log File |
| /tmp/apilog_<pid>.log (Linux) |
| C:\Temp\apilog_<pid>.log (Win)|

| Viewer / Visualizer |

---

## Quickstart — Linux (LD_PRELOAD)

1. Place `hook.so` and `viewer.py` in the same folder as your target program.
2. Run target with hook:

```bash
LD_PRELOAD=$PWD/hook.so /full/path/to/target_binary [args...]
```
3. Find PID:

```bash
pgrep -n target_binary
```
4. View log:

```bash
tail -f /tmp/apilog_<pid>.log
python3 viewer.py <pid>
```
## Quickstart — Windows (IAT hook + Injector)

1. Copy injector.exe, hookdll.dll, and viewer.exe to Windows (use VM).

2. Ensure C:\Temp exists:
```bash
mkdir C:\Temp
```
3. Run injector:
```bash
injector.exe "C:\path\to\target.exe" "C:\full\path\to\hookdll.dll"
```
4. View log:
```bash
type C:\Temp\apilog_<pid>.log
viewer.exe <pid>
```
---
| Function | Purpose (RE)                              |
| -------- | ----------------------------------------- |
| open     | File reads/writes (persistence, payloads) |
| read     | File read data                            |
| write    | File write data                           |
| connect  | Network connections (C2, exfil)           |
| send     | Sent network data (preview logged)        |
| recv     | Received network data (preview logged)    |

---
## Log format & interpretation

Logs are plain text, one event per line. Example (Linux)

```bash
1599999999.123 hook.so loaded (pid=12345)
1599999999.130 open('/tmp/apicv_test.txt', 577) = 3
1599999999.131 write(fd=3, size=21) = 21
1599999999.200 connect(sockfd=3, addr=127.0.0.1:8080) = 0
1599999999.201 send(sockfd=3, len=80, preview='GET / HTTP/1.0\r\nHost: localhost\r\n\r\n') = 80
```
---
## Screenshot
<img width="1366" height="768" alt="Screenshot_2025-09-26_22_13_53" src="https://github.com/user-attachments/assets/af59d696-f67e-48ed-8309-36e2a4608a76" />

## Security & safe use

Do not run unknown malware on your host. Use an isolated VM (VirtualBox / VMware) with snapshots and no shared folders.

Use the tool on benign programs or in controlled lab environments.

This project is educational; it does not guarantee complete coverage of kernel syscalls, inline syscalls, or statically linked binaries.

Logs may include sensitive information handle logs with care.

## Disclaimer

⚠️ **Important:**  
- This software is provided for **educational and research purposes only**.  
- Do **not** use it to run, analyze, or manipulate malware on a live host. Always use an **isolated VM or sandbox**.  
- The author is **not responsible for any damage or legal issues** resulting from misuse.  
- Only use the binaries in controlled, safe environments.

---
## Author

Yeabsira Mihret

Mechanical Engineering @ ASTU | Reverse Engineering student @ INSA

[LinkedIn](https://www.linkedin.com/in/yeabsira-mihret) | [GitHub](https://github.com/yeabsira-mihret)
