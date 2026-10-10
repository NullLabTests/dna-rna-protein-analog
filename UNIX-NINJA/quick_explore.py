#!/usr/bin/env python3
"""
Quick Linux Ecosystem Explorer - fast mode.
Skips full discovery for rapid experimentation.
"""

import json
import os
import re
import subprocess
from urllib.request import urlopen
from urllib.error import URLError


def quick_docs():
    """Quick documentation check for a few interesting commands."""
    interesting = ['ls', 'grep', 'awk', 'find', 'curl', 'python3']
    results = {}
    
    for cmd in interesting:
        # Try man page
        try:
            result = subprocess.run(
                ["man", cmd], capture_output=True, text=True, timeout=3
            )
            if result.returncode == 0 and result.stdout.strip():
                results[cmd] = {"source": "man_page", "has_man": True}
                continue
        except Exception:
            pass
        
        # Web search
        try:
            url = "https://manpages.ubuntu.com/manpages/noble/man1/" + cmd + ".1.html"
            req = urlopen(url, timeout=3)
            if req.getcode() == 200:
                results[cmd] = {"source": "web_search", "has_man": True}
                continue
        except Exception:
            pass
        
        results[cmd] = {"source": "none", "has_man": False}
    
    return results


def main():
    print("Linux Ecosystem Explorer - Quick Mode")
    print("=" * 50)
    
    docs = quick_docs()
    
    for cmd, info in docs.items():
        print(cmd + ":", info["source"])
    
    # Show a few novel combinations
    print("\nSample novel combinations:")
    print("  $ df -h | grep -v 'Filesystem' | sort -k5 -n | tail -5")
    print("  $ last | head -5 | awk '{print $1}' | sort | uniq -c")
    print("  $ curl -s http://ifconfig.me")


if __name__ == "__main__":
    main()