#!/usr/bin/env python3
"""Benchmark build performance"""

import sys
import time
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.config import Config
from modules.build import FreeBSDBuilder

def benchmark_build():
    """Run build benchmark"""
    print("FreeBSD Build Benchmark")
    print("=" * 60)
    
    config = Config("./freebsd_workspace", "BenchmarkOS", "14.0-RELEASE", "amd64")
    config.make_jobs = 1  # Start with single job
    
    results = []
    
    for jobs in [1, 2, 4, 8]:
        print(f"\nTesting with {jobs} jobs...")
        config.make_jobs = jobs
        
        start = time.time()
        # Simulate build (in real scenario, run actual build)
        time.sleep(2)  # Placeholder
        elapsed = time.time() - start
        
        results.append({
            'jobs': jobs,
            'time_seconds': elapsed,
            'time_formatted': f"{elapsed:.2f}s"
        })
        
        print(f"Completed in {elapsed:.2f}s")
    
    # Save results
    with open('benchmark_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "=" * 60)
    print("Benchmark Results:")
    for result in results:
        print(f"  {result['jobs']} jobs: {result['time_formatted']}")

if __name__ == '__main__':
    benchmark_build()
