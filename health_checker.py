#!/usr/bin/env python3
"""
api-health-checker
A CLI utility to monitor multiple API endpoints from a configuration file.
"""

import sys
import json
import time
import argparse
import urllib.request
from urllib.error import URLError, HTTPError
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class EndpointResult:
    name: str
    url: str
    status_code: Optional[int]
    elapsed_ms: float
    success: bool
    error_reason: str = ""
    expected_status: int = 200

def parse_config(config_path: str) -> List[Dict[str, Any]]:
    """Parse the JSON configuration file."""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("Config root must be a list of endpoint objects.")
            return data
    except Exception as e:
        print(f"❌ Error reading configuration {config_path}: {e}")
        sys.exit(1)

def check_endpoint(config: Dict[str, Any]) -> EndpointResult:
    name = config.get("name", "Unnamed Endpoint")
    url = config.get("url")
    expected_status = config.get("expected_status", 200)
    timeout_ms = config.get("timeout_ms", 5000)

    if not url:
        return EndpointResult(name, "Unknown URL", None, 0, False, "Missing URL config", expected_status)

    req = urllib.request.Request(url, headers={'User-Agent': 'API-Health-Checker/1.0'})
    timeout_sec = timeout_ms / 1000.0

    start_time = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout_sec) as response:
            status = response.getcode()
            elapsed_ms = (time.time() - start_time) * 1000
            
            success = status == expected_status
            reason = f"Expected [{expected_status}], got {status}" if not success else ""
            return EndpointResult(name, url, status, elapsed_ms, success, reason, expected_status)
    
    except HTTPError as e:
        elapsed_ms = (time.time() - start_time) * 1000
        status = e.code
        success = status == expected_status
        reason = f"Expected [{expected_status}], got {status}" if not success else ""
        return EndpointResult(name, url, status, elapsed_ms, success, reason, expected_status)

    except URLError as e:
        elapsed_ms = (time.time() - start_time) * 1000
        return EndpointResult(name, url, None, elapsed_ms, False, f"Connection Failed: {e.reason}", expected_status)

    except Exception as e:
        elapsed_ms = (time.time() - start_time) * 1000
        return EndpointResult(name, url, None, elapsed_ms, False, f"Error: {str(e)}", expected_status)

def main() -> int:
    parser = argparse.ArgumentParser(description="Monitor the health of multiple endpoints.")
    parser.add_argument("--config", "-c", type=str, required=True, help="Path to JSON configuration file")
    
    args = parser.parse_args()
    
    endpoints = parse_config(args.config)
    
    print("🔍 Starting API Health Check...")
    print("-" * 50)

    total = len(endpoints)
    failed = 0

    for ep in endpoints:
        result = check_endpoint(ep)
        time_str = f"({result.elapsed_ms:.0f}ms)"
        
        if result.success:
            print(f"✅ [{result.status_code}] {result.url} {time_str}")
        else:
            status_print = result.status_code if result.status_code else "ERR"
            print(f"❌ [{status_print}] {result.url} -- {result.error_reason}")
            failed += 1

    print("-" * 50)
    if failed > 0:
        print(f"🚨 Health check failed: {failed}/{total} endpoints down.")
        return 1
    else:
        print(f"🌟 All {total} endpoints are healthy!")
        return 0

if __name__ == "__main__":
    sys.exit(main())
