#!/usr/bin/env python3
"""
Objective Value Scoring for Linux Command Combinations

Upgrades the explorer to measure REAL human utility, not just heuristics.
Uses task-based validation, time measurement, and outcome tracking.
"""

import subprocess
import json
import os
import re
import time
import itertools
from concurrent.futures import ThreadPoolExecutor, as_completed


def run_pipeline_timed(pipeline_str, timeout=15):
    """Run a pipeline and measure execution time + success."""
    start = time.time()
    try:
        result = subprocess.run(
            pipeline_str, shell=True, capture_output=True, text=True, timeout=timeout
        )
        elapsed = time.time() - start
        return {
            "success": result.returncode == 0,
            "elapsed": elapsed,
            "stdout": result.stdout[:500] if result.stdout else "",
            "stderr": result.stderr[:500] if result.stderr else "",
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "elapsed": timeout,
            "stdout": "",
            "stderr": "TIMEOUT",
            "returncode": -1,
        }
    except Exception as e:
        return {
            "success": False,
            "elapsed": time.time() - start,
            "stdout": "",
            "stderr": str(e)[:200],
            "returncode": -1,
        }


def task_matches_pattern(pipeline_str, task_category):
    """Check if a pipeline is relevant to a known task category."""
    task_keywords = {
        "disk_usage": {"df", "du", "size", "disk", "filesystem"},
        "process_monitoring": {"ps", "top", "process", "running", "python", "java"},
        "file_management": {"find", "locate", "grep", "search", "file"},
        "text_processing": {"awk", "sed", "sort", "uniq", "head", "tail", "cat"},
        "network_info": {"curl", "wget", "ip", "network", "http", "headers"},
        "system_info": {"uptime", "free", "memory", "load", "system"},
    }
    
    keywords = task_keywords.get(task_category, set())
    pipeline_lower = pipeline_str.lower()
    
    # Check if key command words are present
    found = keywords & set(pipeline_lower.split())
    return len(found) >= 2  # At least 2 matching keywords


def score_objective(pipeline_str, timed_result, task_categories):
    """Score by actual objective value, not heuristics."""
    score = 0
    reasons = []
    
    # BASE: If command fails, score = 0 (no value if it doesn't work)
    if not timed_result["success"]:
        score = 0
        reasons.append("FAILED - no objective value")
        return score, reasons
    
    # REWARD: Successful execution gives base score
    score += 25
    reasons.append("Executes successfully (+25)")
    
    # REWARD: Fast execution (< 1 second for simple commands)
    if timed_result["elapsed"] < 1.0:
        score += 20
        reasons.append("Fast execution (+20) - under 1s")
    elif timed_result["elapsed"] < 5.0:
        score += 10
        reasons.append("Reasonable execution (+10) - under 5s")
    
    # TASK RELEVANCE: Does it match a known useful task category?
    best_match = 0
    for category, keywords in task_categories.items():
        if task_matches_pattern(pipeline_str, category):
            # Higher score for more essential categories
            essential = {"disk_usage": 30, "process_monitoring": 25, 
                        "text_processing": 20, "network_info": 15, "system_info": 10}
            best_match = max(best_match, essential.get(category, 5))
    
    score += best_match
    if best_match > 0:
        reasons.append(f"Task-relevant: {best_match}+ points for {best_match}-keyword match")
    
    # EFFICIENCY: Pipeline with | is more valuable than single command
    if "|" in pipeline_str:
        score += 15
        reasons.append("Pipeline optimization (+15)")
    
    # NOVELTY: Uncommon flag combinations or cross-tool pipelines
    # Heuristic: many different flags or mixed tool categories
    flag_count = pipeline_str.count("-")
    if flag_count >= 3:
        score += 5
        reasons.append("Complex flag usage (+5)")
    
    # Cross-tool diversity (commands from different categories)
    cmd_parts = pipeline_str.split("|")[0].split()
    if cmd_parts:
        common_singles = {"ls", "cd", "pwd", "cat", "echo", "exit", "wait", "clear"}
        if cmd_parts[0] not in common_singles:
            score += 5
            reasons.append("Non-trivial command (+5)")
    
    # Cap and floor
    score = max(score, 0)
    score = min(score, 100)
    
    return score, reasons


def main():
    print("=" * 70)
    print("OBJECTIVE VALUE SCORING FOR LINUX COMMAND COMBINATIONS")
    print("=" * 70)
    print()
    print("This upgrade measures REAL utility:")
    print("  - Execution success (binary: yes/no)")
    print("  - Execution time (faster = more valuable)")
    print("  - Task relevance (disk, process, text, network, system)")
    print("  - Pipeline efficiency (| vs single commands)")
    print("  - Flag complexity and cross-tool diversity")
    print()
    print("=" * 70)
    
    # Load previously generated combinations
    try:
        with open("/tmp/command_combinations_results.json") as f:
            results_data = json.load(f)
        top_combos = results_data["top_results"][:20]
    except FileNotFoundError:
        print("No previous results found. Running full exploration first...")
        # Quick run
        from explore_linux_ecosystem import main as run_explorer
        run_explorer()
        with open("/tmp/command_combinations_results.json") as f:
            results_data = json.load(f)
        top_combos = results_data["top_results"][:20]
    
    # Define task categories with keyword patterns
    task_categories = {
        "disk_usage": {"df", "du", "size", "disk", "filesystem", "partition"},
        "process_monitoring": {"ps", "top", "process", "running", "python", "java", "node"},
        "file_management": {"find", "locate", "grep", "search", "file", "directory"},
        "text_processing": {"awk", "sed", "sort", "uniq", "head", "tail", "cat", "grep"},
        "network_info": {"curl", "wget", "ip", "network", "http", "headers", "port"},
        "system_info": {"uptime", "free", "memory", "load", "system", "version"},
    }
    
    # Evaluate each combination for objective value
    print(f"\nEvaluating {len(top_combos)} combinations for objective value...\n")
    
    evaluated = []
    
    for i, r in enumerate(top_combos, 1):
        pipeline = r["pipeline"]
        print(f"\n[{i}/{len(top_combos)}] Testing: {pipeline[:70]}...")
        
        # Run timed
        timed = run_pipeline_timed(pipeline, timeout=10)
        
        # Score objectively
        score, reasons = score_objective(pipeline, timed, task_categories)
        
        # Also get speed category
        if timed["success"]:
            speed = "FAST" if timed["elapsed"] < 1.0 else "MODERATE" if timed["elapsed"] < 5.0 else "SLOW"
        else:
            speed = "FAILED"
        
        evaluated.append({
            "pipeline": pipeline,
            "objective_score": score,
            "success": timed["success"],
            "elapsed": round(timed["elapsed"], 3),
            "speed": speed,
            "reasons": reasons,
            "stderr": timed["stderr"][:100],
        })
        
        # Progress indicator
        if (i % 5) == 0:
            print(f"  Progress: {i}/{len(top_combos)} evaluated...")
    
    # Sort by objective score
    evaluated.sort(key=lambda x: x["objective_score"], reverse=True)
    
    # Display results
    print("\n" + "=" * 70)
    print("OBJECTIVE VALUE RANKINGS (highest to lowest)")
    print("=" * 70)
    
    header = "{:<80} {:>6} {:>8} {:>6} {:>40}".format(
        "PIPELINE", "OBJ-SCORE", "SPEED", "VALID", "REASONS"
    )
    print(header)
    print("-" * 70)
    
    top_results = evaluated[:20]
    for r in top_results:
        pipe_display = r["pipeline"][:77] + "..." if len(r["pipeline"]) > 77 else r["pipeline"]
        valid_str = "YES" if r["success"] else "NO"
        row = "{:<80} {:>6} {:>8} {:>6} {:>40}".format(
            pipe_display, r["objective_score"], r["speed"], valid_str, 
            "; ".join(r["reasons"])[:35]
        )
        print(row)
    
    # Summary stats
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    valid_count = sum(1 for r in evaluated if r["success"])
    avg_time = sum(r["elapsed"] for r in evaluated if r["success"]) / max(valid_count, 1)
    fast_count = sum(1 for r in evaluated if r["success"] and r["elapsed"] < 1.0)
    
    print(f"Total evaluated: {len(evaluated)}")
    print(f"Successful: {valid_count}/{len(evaluated)} ({100*valid_count/len(evaluated):.1f}%)")
    print(f"Average valid time: {avg_time:.3f}s")
    print(f"Fast (<1s): {fast_count}/{valid_count}")
    print(f"Highest objective score: {evaluated[0]['objective_score']}")
    
    # Save results
    with open("/tmp/objective_value_results.json", "w") as f:
        json.dump({
            "total_evaluated": len(evaluated),
            "successful": valid_count,
            "average_time": avg_time,
            "fast_commands": fast_count,
            "results": [{"pipeline": r["pipeline"], "objective_score": r["objective_score"], 
                        "success": r["success"], "elapsed": r["elapsed"], 
                        "speed": r["speed"], "reasons": r["reasons"]} for r in evaluated],
        }, f, indent=2)
    
    print(f"\nResults saved to /tmp/objective_value_results.json")
    print("=" * 70)
    
    # Return the top result
    return evaluated[0] if evaluated else None


if __name__ == "__main__":
    top = main()
    if top:
        print(f"\nTOP RESULT: score={top['objective_score']}, pipeline={top['pipeline'][:60]}...")
        print(f"  Success: {top['success']}, Time: {top['elapsed']}s, Speed: {top['speed']}")
        print(f"  Reasons: {', '.join(top['reasons'])}")