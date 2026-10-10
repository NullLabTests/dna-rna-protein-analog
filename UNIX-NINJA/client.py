#!/usr/bin/env python3
"""
Linux Ecosystem Explorer Client

CLI interface for interacting with the Linux Ecosystem Explorer.
Provides subcommands for discovery, documentation, and combination generation.
"""

import argparse
import json
import sys
import os


def load_docs(path="/tmp/command_docs_v2.json"):
    """Load documentation JSON."""
    with open(path) as f:
        return json.load(f)


def discover_commands():
    """Run command discovery and print summary."""
    from explore_linux_ecosystem import get_all_commands
    commands = get_all_commands()
    print(f"Discovered {len(commands)} commands")


def document_commands():
    """Run documentation retrieval and print summary."""
    from explore_linux_ecosystem import check_command_docs
    import concurrent.futures
    
    docs = load_docs()
    # Reload docs
    cmd_dirs = ["/usr/bin", "/usr/local/bin", "/bin", "/sbin", "/usr/games"]
    commands = set()
    for d in cmd_dirs:
        if os.path.isdir(d):
            for f in os.listdir(d):
                filepath = os.path.join(d, f)
                if os.path.isfile(filepath) and not f.startswith("."):
                    commands.add(f)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(check_command_docs, cmd): cmd for cmd in commands}
        processed = 0
        for future in concurrent.futures.as_completed(futures):
            processed += 1
    
    docs = {}
    for future in concurrent.futures.as_completed({
        executor.submit(check_command_docs, cmd): cmd 
        for cmd in commands
    }):
        pass
    
    # Count sources
    sources = {}
    for cmd, doc in docs.items():
        s = doc["source"]
        sources[s] = sources.get(s, 0) + 1
    
    print(f"Documented {processed} commands")
    print(f"Sources: {sources}")


def generate_combinations():
    """Generate and display novel command combinations."""
    from explore_linux_ecosystem import main as run_main
    # Just print a summary of what's available
    import json
    with open("/tmp/command_combinations_results.json") as f:
        results = json.load(f)
    
    print(f"Total combinations tested: {results['total_combinations_tested']}")
    print(f"Valid combinations: {results['valid_combinations']}")
    print(f"Top result score: {results['top_results'][0]['score']}")
    print(f"Top pipeline: {results['top_results'][0]['pipeline']}")


def list_top_combinations():
    """List top-scoring command combinations."""
    import json
    with open("/tmp/command_combinations_results.json") as f:
        results = json.load(f)
    
    print("\nTop 10 command combinations:")
    for i, r in enumerate(results['top_results'][:10], 1):
        valid = "YES" if r['valid'] else "NO"
        print(f"  {i}. Score: {r['score']}, Valid: {valid}")
        print(f"     {r['pipeline'][:80]}...")


def main():
    parser = argparse.ArgumentParser(
        description="Linux Ecosystem Explorer Client"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Discover subcommand
    discover_parser = subparsers.add_parser(
        "discover", help="Discover all available Linux commands"
    )
    discover_parser.set_defaults(func=discover_commands)
    
    # Document subcommand
    document_parser = subparsers.add_parser(
        "document", help="Retrieve documentation for all commands"
    )
    document_parser.set_defaults(func=document_commands)
    
    # Generate subcommand
    generate_parser = subparsers.add_parser(
        "generate", help="Generate novel command combinations"
    )
    generate_parser.set_defaults(func=generate_combinations)
    
    # List top subcommand
    list_parser = subparsers.add_parser(
        "list", help="List top-scoring command combinations"
    )
    list_parser.set_defaults(func=list_top_combinations)
    
    args = parser.parse_args()
    
    if hasattr(args, "func"):
        args.func()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()