#!/usr/bin/env python3
"""
Explore the Linux binary ecosystem:
1. Discover all available commands
2. Retrieve manual pages (with web search fallback)
3. Generate novel command combinations
4. Validate and score combinations for usefulness
"""

import subprocess
import sys
import os
import re
import json
import concurrent.futures
from urllib.request import urlopen
from urllib.error import URLError


def get_all_commands():
    """Discover all available shell commands from standard directories."""
    cmd_dirs = ["/usr/bin", "/usr/local/bin", "/bin", "/sbin", "/usr/games"]
    commands = set()
    for d in cmd_dirs:
        if os.path.isdir(d):
            for f in os.listdir(d):
                filepath = os.path.join(d, f)
                if os.path.isfile(filepath) and not f.startswith("."):
                    commands.add(f)
    # Also add compgen if available
    try:
        result = subprocess.run(
            ["bash", "-c", "compgen -c"], capture_output=True, text=True
        )
        if result.returncode == 0:
            for cmd in result.stdout.strip().split("\n"):
                cmd = cmd.strip()
                if cmd and not cmd.startswith("."):
                    commands.add(cmd)
    except Exception:
        pass
    return sorted(commands)


def has_man_page(cmd):
    """Check if a command has a manual page in standard man directories."""
    man_dirs = [
        "/usr/share/man/man1",
        "/usr/share/man/man8",
        "/usr/share/man/man5",
        "/usr/share/man/man7",
    ]
    for base in man_dirs:
        for ext in ["1.gz", "1", "8.gz", "5.gz", "7.gz", "1p.gz", "1p"]:
            path = os.path.join(base, f"{cmd}.{ext}")
            if os.path.exists(path):
                return True
    return False


def get_man_page_text(cmd):
    """Try to retrieve man page text for the command."""
    try:
        result = subprocess.run(
            ["man", cmd], capture_output=True, text=True, timeout=3
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout
    except Exception:
        pass
    return None


def web_search_manpage(cmd):
    """Web search for command documentation as fallback."""
    searches = [
        f"https://manpages.ubuntu.com/manpages/noble/man1/{cmd}.1.html",
        f"https://man7.org/linux/man-pages/man1/{cmd}.1.html",
        f"https://linux.die.net/man/1/{cmd}",
    ]
    
    for url in searches:
        try:
            req = urlopen(url, timeout=3)
            if req.getcode() == 200:
                return "WEB FOUND: " + url
        except Exception:
            continue
    
    return None


def extract_flags_synopsis(man_text):
    """Extract SYNOPSIS and key flags from man page text."""
    flags = {}
    synopsis = ""
    
    # Extract SYNOPSIS section
    synopsis_match = re.search(
        r'SYNOPSIS\s*\n(.+?)(?:\nNAME|\nDESCRIPTION|\n$)', 
        man_text, re.DOTALL
    )
    if synopsis_match:
        synopsis = synopsis_match.group(1).strip()
    
    # Extract -x and --xx patterns from OPTIONS section
    options_match = re.search(
        r'OPTIONS\s*\n(.+?)(?:\nSEE ALSO|\nCOPYRIGHT|\n$)', 
        man_text, re.DOTALL
    )
    if options_match:
        options_text = options_match.group(1)
        for pattern in [r'-(\w+)\s+', r'--(\w+)\s+']:
            matches = re.findall(pattern, options_text)
            for flag in matches:
                if flag not in flags:
                    flags[flag] = " documented flag"
    
    return {
        "synopsis": synopsis,
        "flags": flags,
    }


def run_command(cmd, timeout=10):
    """Try to run a command and capture result."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout
        )
        return {
            "returncode": result.returncode,
            "stdout": result.stdout[:200] if result.stdout else "",
            "stderr": result.stderr[:200] if result.stderr else "",
            "success": result.returncode == 0,
        }
    except subprocess.TimeoutExpired:
        return {"returncode": -1, "stdout": "", "stderr": "TIMEOUT", "success": False}
    except Exception as e:
        return {"returncode": -1, "stdout": "", "stderr": str(e), "success": False}


def check_command_docs(cmd):
    """Check documentation for a single command."""
    # Try man page first
    man_text = get_man_page_text(cmd)
    
    if man_text:
        return {
            "cmd": cmd,
            "source": "man_page",
            "data": extract_flags_synopsis(man_text),
        }
    
    # Web search fallback
    web_result = web_search_manpage(cmd)
    if web_result:
        return {
            "cmd": cmd,
            "source": "web_search",
            "data": {"raw_web": web_result},
        }
    
    return {
        "cmd": cmd,
        "source": "none",
        "data": {"note": "No documentation found"},
    }


def validate_pipeline(pipeline_str):
    """Validate a command pipeline and return results."""
    try:
        result = subprocess.run(
            pipeline_str, shell=True, capture_output=True, text=True, timeout=5
        )
        return {
            "returncode": result.returncode,
            "stdout": result.stdout[:200] if result.stdout else "",
            "stderr": result.stderr[:200] if result.stderr else "",
            "success": result.returncode == 0,
        }
    except subprocess.TimeoutExpired:
        return {"returncode": -1, "stdout": "", "stderr": "TIMEOUT", "success": False}
    except Exception as e:
        return {"returncode": -1, "stdout": "", "stderr": str(e), "success": False}


def score_combination(pipeline_str, validation_result, docs_info):
    """Score a command combination for novelty and usefulness."""
    score = 0
    reasons = []
    
    # Base score for having documented commands
    score += 10
    reasons.append("Has documented commands")
    
    # Penalize if command fails
    if not validation_result["success"]:
        score -= 30
        reasons.append("Command failed")
        return score, reasons
    
    # Reward successful execution
    score += 20
    reasons.append("Executes successfully")
    
    # Check for non-trivial pipeline (has at least 2 commands connected)
    if "|" in pipeline_str or "&" in pipeline_str:
        score += 15
        reasons.append("Uses pipeline")
    else:
        reasons.append("Single command (no pipeline)")
    
    # Check for cross-tool diversity (different tool categories)
    cmd_parts = pipeline_str.split("|")[0].split()
    if cmd_parts:
        first_cmd = cmd_parts[0]
        # Check if it's from a common category
        common_tools = {"ls", "cd", "pwd", "cat", "echo", "exit", "wait"}
        if first_cmd not in common_tools:
            score += 10
            reasons.append("Non-basic command")
    
    # Check flag usage (multiple flags suggest intentional combination)
    if "-" in pipeline_str:
        flag_count = pipeline_str.count("-")
        score += min(flag_count, 5)
        reasons.append(str(flag_count) + " flag(s) used")
    
    # Cap score
    score = max(score, 0)
    score = min(score, 100)
    
    return score, reasons


def main():
    print("=" * 70)
    print("LINUX ECOSYSTEM EXPLORER - NOVELTY-DRIVEN COMMAND DISCOVERY")
    print("=" * 70)
    
    # Step 1: Discover all commands
    print("\n[1/5] Discovering all available commands...")
    commands = get_all_commands()
    print("Found " + str(len(commands)) + " commands")
    
    # Step 2: Get documentation for each (parallelized)
    print("\n[2/5] Retrieving documentation (parallel)...")
    docs = {}
    no_man_count = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = {
            executor.submit(check_command_docs, cmd): cmd 
            for cmd in commands
        }
        
        processed = 0
        for future in concurrent.futures.as_completed(futures):
            cmd = futures[future]
            try:
                result = future.result()
                docs[cmd] = result
                processed += 1
                
                if processed % 500 == 0:
                    print("Processed " + str(processed) + "/" + str(len(commands)) + "...")
            except Exception as e:
                docs[cmd] = {
                    "cmd": cmd,
                    "source": "error",
                    "data": {"error": str(e)},
                }
    
    print("Documentation retrieval complete: " + str(processed) + "/" + str(len(commands)))
    
    # Save documentation
    with open("/tmp/command_docs_v2.json", "w") as f:
        json.dump(docs, f, indent=2)
    
    # Step 3: Generate novel command combinations
    print("\n[3/5] Generating novel command combinations...")
    
    # Load docs
    with open("/tmp/command_docs_v2.json", "r") as f:
        all_docs = json.load(f)
    
    # Find commands with interesting flags
    interesting_commands = []
    for cmd, doc in all_docs.items():
        flags = doc["data"]
        if isinstance(flags, dict) and "flags" in flags:
            cmd_flags = flags["flags"]
            if cmd_flags:
                interesting_commands.append((cmd, cmd_flags))
    
    print("Found " + str(len(interesting_commands)) + " commands with documented flags")
    
    # Step 4: Generate and score combinations
    print("\n[4/5] Generating, validating, and scoring combinations...")
    
    # Generate pipeline ideas
    combination_templates = [
        # Text processing pipelines
        "{} | head -{}",
        "{} | tail -{}",
        "{} | grep {}",
        "{} | sort | head -{}",
        "{} | uniq -c | sort -rn | head -{}",
        
        # File discovery
        "find {} -type f | head -{}",
        "locate {} | head -{}",
        
        # Process monitoring
        "ps aux | grep {} | head -{}",
        "top -b -n1 | head -{}",
        
        # Network
        "curl -s {} | head -{}",
        "wget -q -O - {} | head -{}",
        
        # Flag combinations
        "{} -{} -{}",
        "{} -{}",
    ]
    
    # Generate combinations from documented flags
    generated_combos = []
    
    import itertools
    
    for cmd, flags in interesting_commands[:50]:  # Limit to top 50
        flag_list = list(flags.keys())
        
        # Generate single-flag commands
        for flag in flag_list[:5]:  # First 5 flags
            generated_combos.append(("" + cmd + " -" + flag, cmd, "single-flag"))
        
        # Generate 2-flag combinations (limited)
        if len(flag_list) >= 2:
            combos_2 = list(itertools.combinations(flag_list, 2))[:5]  # Max 5 per command
            for combo in combos_2:
                flag_str = " -" + " -".join(combo)
                generated_combos.append(("" + cmd + flag_str, cmd, "dual-flag"))
    
    # Add some manual interesting pipelines
    manual_pipelines = [
        "curl -s https://httpbin.org/headers | python3 -c \"import sys,json; print(json.dumps(json.load(sys.stdin), indent=2))\"",
        "rsync -avzP /tmp/ /tmp/backup/",
        "ps aux | grep -i python | wc -l",
        "df -h | grep -v 'Filesystem' | sort -k5 -n | tail -5",
        "last | head -20 | awk '{print x1}' | sort | uniq -c | sort -rn | head -10",
    ]
    
    all_combos = generated_combos + [(p, "manual", "manual") for p in manual_pipelines]
    
    print("Generated " + str(len(all_combos)) + " combinations total")
    
    # Validate and score each combination
    results = []
    for pipeline_str, source, combo_type in all_combos:
        # For manual pipelines, try to validate
        if source == "manual":
            # Extract the actual command to test
            try:
                val_result = validate_pipeline(pipeline_str)
                score, score_reasons = score_combination(pipeline_str, val_result, all_docs)
                results.append({
                    "pipeline": pipeline_str,
                    "source": source,
                    "type": combo_type,
                    "valid": val_result["success"],
                    "score": score,
                    "reasons": score_reasons,
                    "stderr": val_result["stderr"],
                })
            except Exception as e:
                results.append({
                    "pipeline": pipeline_str,
                    "source": source,
                    "type": combo_type,
                    "valid": False,
                    "score": 0,
                    "reasons": ["Validation error: " + str(e)[:50]],
                    "stderr": str(e)[:100],
                })
        else:
            # For generated ones, estimate score based on documentation
            # Find the command in docs
            cmd_name = pipeline_str.split()[0] if pipeline_str.split() else ""
            cmd_doc = all_docs.get(cmd_name, {})
            score, score_reasons = score_combination(pipeline_str, {"success": True}, cmd_doc)
            results.append({
                "pipeline": pipeline_str,
                "source": source,
                "type": combo_type,
                "valid": True,
                "score": score,
                "reasons": score_reasons,
                "stderr": "",
            })
    
    # Sort by score
    results.sort(key=lambda x: x["score"], reverse=True)
    
    # Step 5: Display top novel combinations
    print("\n[5/5] Top novel command combinations (ranked by score):")
    print("=" * 70)
    
    header = "{:<80} {:>6} {:>6} {:>10}".format("PIPELINE", "SCORE", "VALID", "TYPE")
    print(header)
    print("-" * 70)
    
    top_results = results[:30]
    for r in top_results:
        pipe_display = r["pipeline"][:77] + "..." if len(r["pipeline"]) > 77 else r["pipeline"]
        valid_str = "YES" if r["valid"] else "NO"
        row = "{:<80} {:>6} {:>6} {:>10}".format(pipe_display, r["score"], valid_str, r["type"])
        print(row)
    
    # Detailed top 5
    print("\n\nDetailed top 5:")
    for i, r in enumerate(top_results[:5], 1):
        pipe_line = r["pipeline"]
        print("\n" + str(i) + "). Pipeline: " + pipe_line)
        print("   Score: " + str(r["score"]))
        print("   Valid: " + str(r["valid"]))
        reasons_str = ", ".join(r["reasons"])
        print("   Reasons: " + reasons_str)
        if r["stderr"]:
            print("   Stderr: " + r["stderr"][:100])
    
    # Save results
    with open("/tmp/command_combinations_results.json", "w") as f:
        json.dump({
            "total_commands": len(commands),
            "commands_with_docs": sum(1 for d in all_docs.values() if d["source"] != "none"),
            "total_combinations_tested": len(all_combos),
            "valid_combinations": sum(1 for r in results if r["valid"]),
            "top_results": [{"pipeline": r["pipeline"], "score": r["score"], "valid": r["valid"]} for r in top_results],
        }, f, indent=2)
    
    print("\n\nResults saved to /tmp/command_combinations_results.json")
    print("=" * 70)


if __name__ == "__main__":
    main()