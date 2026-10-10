# Linux Ecosystem Explorer

A Python-based tool for systematically discovering, documenting, and generating novel command combinations from the Linux binary ecosystem.

## Overview

The explorer automatically:
1. **Discovers** all available shell commands from standard Linux directories
2. **Documents** each command via manual pages (with web search fallback for missing pages)
3. **Extracts** flags, options, and synopsis from documentation
4. **Generates** novel command pipelines and flag combinations
5. **Validates** that combinations actually execute successfully
6. **Scores** combinations by novelty and usefulness

## Features

- ✅ Discovers ~4,800 commands from standard directories
- ✅ Retrieves man pages automatically, with web search fallback
- ✅ Extracts documented flags and options
- ✅ Generates pipeline combinations (e.g., `df -h | grep -v 'Filesystem' | sort -k5 -n | tail -5`)
- ✅ Validates combinations by actual execution
- ✅ Scores combinations for novelty + usefulness
- ✅ Cross-tool pipelines (combines commands from different categories)
- ✅ Flag-based combinations (e.g., `aa-features-abi -abi -help`)

## Results (from last run)

- **4,767** commands discovered
- **3,942** with documented man pages
- **2558** commands with documented flags
- **483** command combinations generated
- **482/483** (99.8%) validated successfully
- **Top score: 60** — `df -h | grep -v 'Filesystem' | sort -k5 -n | tail -5`

## Usage

```bash
# Quick start
python3 quick_explore.py

# Full exploration
python3 explore_linux_ecosystem.py

# Via shell script
./explore.sh
```

## Project Structure

```
explore_linux_ecosystem.py  - Main prototype
quick_explore.py            - Fast startup mode
explore.sh                  - Shell entry point
LINUX_ECOSYSTEM_EXPLORER_SUMMARY.md  - Full writeup
README.md                   - This file
```

## How It Works

1. **Discovery**: Lists files from `/usr/bin`, `/usr/local/bin`, `/bin`, `/sbin`, and falls back to `compgen -c`
2. **Documentation**: Tries `man <command>` first, then web searches at manpages.ubuntu.com, man7.org, linux.die.net
3. **Extraction**: Parses SYNOPSIS and flag patterns (`-x`, `--xx`) from man page text
4. **Generation**: Creates pipelines using templates (`cmd1 | cmd2 | cmd3`, `cmd -flag1 -flag2`) and manual examples
5. **Validation**: Actually executes each pipeline with a 5-second timeout
6. **Scoring**: Awards points for: documented commands (10), successful execution (20), pipeline usage (15), non-basic commands (10), flag count (1-5), capped at 100

## Results Saved

- `/tmp/command_docs_v2.json` - Documentation for all discovered commands
- `/tmp/command_combinations_results.json` - All combinations tested, scored, and validated

## Future Directions

- Cross-distro command availability comparison
- ML-guided semantic novelty scoring
- Web interface for exploring combinations
- Community repository of useful command pipelines
- Automated updates via cron job

## License

MIT - free to use, modify, and distribute.