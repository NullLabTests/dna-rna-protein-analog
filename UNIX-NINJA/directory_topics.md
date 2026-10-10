# Directory Topics: Linux Command Exploration

## Overview
This directory contains topics, themes, and categorized explorations of the Linux command ecosystem discovered by the Linux Ecosystem Explorer.

## Command Categories Discovered

Based on the 4,767 commands explored, commands naturally fall into these categories:

### 1. Text Processing
- `grep`, `sed`, `awk`, `sort`, `uniq`, `head`, `tail`, `cat`, `less`
- Pipelines: `cat file | grep pattern | sort | uniq`

### 2. File System & Disk
- `ls`, `find`, `locate`, `df`, `du`, `du -sh`
- Disk analysis: `df -h | grep -v 'Filesystem' | sort -k5 -n | tail -5`

### 3. Process Management
- `ps`, `top`, `last`, `who`, `w`
- Process analysis: `ps aux | grep python | wc -l`

### 4. Network & Download
- `curl`, `wget`, `ping`, `ssh`, `nc`
- Network info: `curl -s https://httpbin.org/headers`

### 5. AppArmor/Security
- `aa-enabled`, `aa-exec`, `aa-features-abi`, `aa-status`
- Security: `aa-features-abi -abi -help`

### 6. Archive & Compression
- `tar`, `gzip`, `bzip2`, `xz`, `7z`, `7za`, `7zr`
- Archiving: `rsync -avzP /source/ /dest/`

### 7. Development & Compilation
- `gcc`, `g++`, `cc`, `as`, `ld`
- Compilation: `gcc -o output input.c`

### 8. Volume Management
- `xorriso`, `osirrox`, `udisks`, `pmount`
- ISO operations: `xorriso -as cdrecord -msinfo /dev/cdrom`

### 9. Python/Ecosystem
- `python3`, `pip`, `virtualenv`, `py.test`
- Python: `python3 -c "print('hello')"`

### 10. System Administration
- `systemctl`, `service`, `init`, `shutdown`
- Services: `systemctl status apache2`

## Pipeline Templates Explored

| Template | Example | Score |
|---|---|---|
| `cmd1 | cmd2 | cmd3` | `df -h | grep -v 'Filesystem' | sort -k5 -n | tail -5` | 60 |
| `cmd -flag1 -flag2` | `aa-features-abi -abi -help` | 44 |
| `find ... | head -n` | `find / -name '*.log' -size +1M -exec head -20 {} \\;` | 35 |
| `ps aux | grep pattern` | `ps aux | grep -i python | wc -l` | 57 |
| `curl -s URL | process` | `curl -s https://httpbin.org/headers | python3 -c "..."` | 57 |

## Top-Performing Combinations

| Rank | Pipeline | Description | Score |
|---|---|---|---|
| 1 | `df -h \| grep -v 'Filesystem' \| sort -k5 -n \| tail -5` | Top 5 filesystem mounts | 60 |
| 2 | `last \| head -20 \| awk '{print x1}' \| sort \| uniq -c \| sort -rn \| head -10` | Top 10 login usernames | 59 |
| 3 | `curl -s https://httpbin.org/headers | python3 -c "import sys,json; print(json.dumps(json.load(sys.stdin), indent=2))"` | Fetch + pretty-print HTTP headers | 57 |
| 4 | `ps aux \| grep -i python \| wc -l` | Count running Python processes | 57 |
| 5 | `aa-features-abi -abi -help` | AppArmor feature flags help | 44 |

## Discovery Gaps

Commands without manual pages (category examples):
- **LLVM tools**: `llvm-lto-21`, `llvm-cxxdump-21` — compiler infrastructure
- **Python args**: `activate-global-python-argcomplete` — Python argument completion
- **Custom apps**: `airscan-discover`, `animate-im7` — scanner/graphics tools
- **Filesystem**: `mft`, `dbus-send` — specialized utilities

## Themes & Patterns

### Cross-Tool Pipelines
Combining commands from different categories produces the highest-scoring results:
- `df` (disk) + `grep` (filter) + `sort` (order) + `tail` (select) = disk analysis
- `last` (login) + `awk` (extract) + `sort` (order) + `uniq` (count) + `sort` (rank) + `head` (top N) = user analysis

### Flag Combinations
Using multiple flags from the same command:
- `aa-features-abi -abi -help` — two flags from AppArmor tool
- `rsync -avzP` — three flags for archive sync with progress
- `curl -L -O -C -` — resume + location + remote

### Single-Command Depth
Some commands have 20+ documented flags, enabling rich combinations:
- `mpv` — 300+ video player flags
- `gcc/g++` — 20+ compilation flags
- `openvpn` — 20+ configuration flags

## Next Exploration Themes

1. **Cross-distro comparison**: Run on Debian, Fedora, Arch, Ubuntu — compare command availability
2. **Semantic grouping**: Use embeddings to cluster commands by function/behavior
3. **Workflow patterns**: Analyze .bashrc, .profile for common command combinations
4. **Rare command discovery**: Find commands documented on <1% of systems
5. **Historical tracking**: Re-run explorer monthly to track command ecosystem changes

## Related Topics

- [Linux Command Guide](https://linux.die.net/man_pages/)
- [Bash Pipelines](https://tldp.org/LDP/abs/html/)
- [AppArmor Documentation](https://wiki.debian.org/AppArmor)
- [GNU Coreutils](https://www.gnu.org/software/coreutils/)