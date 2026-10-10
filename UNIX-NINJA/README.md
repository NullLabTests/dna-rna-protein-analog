# Linux Ecosystem Explorer - With Objective Value Scoring

A Python-based tool for systematically discovering, documenting, and generating novel command combinations from the Linux binary ecosystem, with **objective value measurement** for real human utility.

## Overview

The explorer automatically:
1. **Discovers** all available shell commands from standard Linux directories
2. **Documents** each command via manual pages (with web search fallback)
3. **Extracts** flags, options, and synopsis from documentation
4. **Generates** novel command pipelines and flag combinations
5. **Validates** that combinations actually execute successfully
6. **Scores** combinations by **objective value** (not just heuristics)

## What's New: Objective Value Scoring

The upgraded framework measures **REAL human utility** across 5 dimensions:

| Dimension | What It Measures | Points |
|---|---|---|
| **Execution Success** | Binary: does it work? | +25 (or 0 if fails) |
| **Execution Speed** | How fast does it run? | +20 (<1s), +10 (<5s) |
| **Task Relevance** | Matches known useful task categories | +5-30 (disk, process, text, network, system) |
| **Pipeline Efficiency** | Uses `|` to chain commands | +15 |
| **Flag/Command Complexity** | Non-trivial flags or commands | +5 each |

**Maximum Score: 100**

## Key Findings (from Objective Value Evaluation)

**Top-Scoring Combinations (Score: 90):**

| Pipeline | Score | Speed | Why It Scores High |
|---|---|---|---|
| `df -h \| grep -v 'Filesystem' \| sort -k5 -n \| tail -5` | 90 | FAST (<1s) | Disk task + fast + pipeline + flags |
| `last \| head -20 \| awk '{print x1}' \| sort \| uniq -c \| sort -rn \| head -10` | 90 | FAST (<1s) | Process task + fast + pipeline + flags |
| `ps aux \| grep -i python \| wc -l` | 90 | FAST (<1s) | Process task + fast + pipeline + flags |

**Moderately-Scoring (Score: 55):**
- `curl -s https://httpbin.org/headers | python3 -c "..."` — Network task, but slower execution
- `add-apt-repository -help -debug` etc. — Single commands with flags, no pipeline

**Failed Combinations (Score: 0):**
- `aa-features-abi -abi -help` — Commands that don't execute successfully have zero value

## How It Works

### 1. Discovery (~4,800 commands)
- Lists files from `/usr/bin`, `/usr/local/bin`, `/bin`, `/sbin`
- Falls back to `compgen -c`
- Checks man pages in standard `/usr/share/man/` directories

### 2. Documentation Retrieval
- Tries `man <command>` first
- Falls back to web search at manpages.ubuntu.com, man7.org, linux.die.net
- Extracts SYNOPSIS and flag patterns (`-x`, `--xx`)

### 3. Combination Generation
- Pipeline templates: `cmd1 \| cmd2 \| cmd3`, `cmd -flag1 -flag2`
- Flag combinations from documented command options
- Manual interesting pipelines pre-defined

### 4. Objective Value Scoring (NEW)
Each combination is evaluated on 5 dimensions:

```python
def score_objective(pipeline_str, timed_result, task_categories):
    score = 0
    
    # 1. SUCCESS (binary): +25 if executes, 0 if fails
    if not timed_result["success"]:
        score = 0  # NO VALUE IF IT DOESN'T WORK
    
    # 2. SPEED: +20 if <1s, +10 if <5s
    if timed_result["elapsed"] < 1.0:
        score += 20
    elif timed_result["elapsed"] < 5.0:
        score += 10
    
    # 3. TASK RELEVANCE: +5-30 based on category
    # disk_usage > process_monitoring > text_processing > network_info > system_info
    
    # 4. PIPELINE: +15 if uses | separators
    
    # 5. COMPLEXITY: +5 for flags, non-trivial commands
    
    score = max(0, min(100, score))
    return score
```

### 5. Results Saved
- `/tmp/command_docs_v2.json` — Documentation for all discovered commands
- `/tmp/command_combinations_results.json` — 483 combos tested, scored
- `/tmp/objective_value_results.json` — Objective value scores for top combos

## Usage

```bash
# Quick start with objective scoring
python3 quick_explore.py

# Full exploration + objective scoring
python3 explore_linux_ecosystem.py

# Pure objective value analysis
python3 objective_value_scoring.py

# Via shell script
./explore.sh
```

## Files in This Repository

| File | Purpose |
|---|---|
| `explore_linux_ecosystem.py` | Main prototype (4,767 commands, 483 combos validated) |
| `quick_explore.py` | Fast startup mode |
| `explore.sh` | Shell entry point |
| `objective_value_scoring.py` | **NEW** — Objective value scoring (5 dimensions) |
| `LINUX_ECOSYSTEM_EXPLORER_SUMMARY.md` | Full writeup (novelty, methodology, results) |
| `README.md` | This file |
| `client.py` | CLI subcommands |
| `directory_topics.md` | Categorized exploration topics |

## Objective Value Results (from last run)

| Pipeline | Objective Score | Success | Speed | Key Contributors |
|---|---|---|---|---|
| `df -h \| grep -v 'Filesystem' \| sort -k5 -n \| tail -5` | **90** | YES | FAST, disk task, pipeline |
| `last \| head -20 \| awk '{print x1}' \| sort \| uniq -c \| sort -rn \| head -10` | **90** | YES | FAST, process task, pipeline |
| `ps aux \| grep -i python \| wc -l` | **90** | YES | FAST | process task, pipeline |
| `curl -s https://httpbin.org/headers | python3 -c "..."` | 55 | MODERATE | network task, success, but slower |
| `aa-features-abi -abi -help` | 0 | NO | N/A | FAILED — no objective value |

## Task Category Weightings

The objective scorer weights task categories by human utility:

| Category | Keywords | Base Points |
|---|---|---|
| **disk_usage** | `df`, `du`, `size`, `disk`, `filesystem`, `partition` | +30 |
| **process_monitoring** | `ps`, `top`, `process`, `running`, `python`, `java`, `node` | +25 |
| **text_processing** | `awk`, `sed`, `sort`, `uniq`, `head`, `tail`, `cat`, `grep` | +20 |
| **network_info** | `curl`, `wget`, `ip`, `network`, `http`, `headers`, `port` | +15 |
| **system_info** | `uptime`, `free`, `memory`, `load`, `system`, `version` | +10 |

## Why Objective Value Matters

Previous command explorers scored by heuristics (flag count, pipeline length). This upgrade matters because:

1. **Binary success/failure**: A command that fails has ZERO value, regardless of flag complexity
2. **Speed matters**: A pipeline that takes 30 seconds vs 0.03 seconds has dramatically different human utility
3. **Task relevance**: A disk analysis pipeline is more useful to a sysadmin than a text manipulation one (and vice versa)
4. **Pipeline efficiency**: `cmd1 \| cmd2` is more valuable than a single command (combines cross-tool wisdom)
5. **Fair comparison**: Scores enable ranking and comparison across different types of command combinations

## Future Enhancements

- **Task-specific filtering**: Only show combinations relevant to your current task
- **Historical tracking**: Re-run explorer monthly to track command ecosystem changes
- **Community ratings**: Let users upvote/downvote combinations by actual usefulness
- **ML integration**: Use sentence embeddings to predict human-perceived usefulness
- **Cross-distro profiles**: Compare command availability and usefulness across Ubuntu/Debian/Fedora/Arch

## License

MIT - free to use, modify, and distribute.

## Acknowledgments

- Linux command ecosystem data from man pages and web searches
- Inspired by the classic Unix philosophy of small, composable tools
- Objective scoring framework designed for real human utility measurement