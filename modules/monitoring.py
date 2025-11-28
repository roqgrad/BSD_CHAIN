"""Build monitoring and progress tracking module"""

import time
import psutil
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List

class BuildMonitor:
    """Monitors build progress and system resources"""
    
    def __init__(self, config):
        self.config = config
        self.start_time = None
        self.metrics = []
        self.checkpoints = []
    
    def start(self):
        """Start monitoring"""
        self.start_time = time.time()
        print("[*] Build monitoring started")
    
    def checkpoint(self, name: str):
        """Record a checkpoint"""
        if not self.start_time:
            return
        
        elapsed = time.time() - self.start_time
        checkpoint = {
            'name': name,
            'timestamp': datetime.now().isoformat(),
            'elapsed_seconds': elapsed,
            'elapsed_formatted': self._format_time(elapsed)
        }
        self.checkpoints.append(checkpoint)
        print(f"[✓] Checkpoint: {name} ({checkpoint['elapsed_formatted']})")
    
    def collect_metrics(self):
        """Collect system metrics"""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage(str(self.config.work_dir)).percent,
        }
        
        # Add disk I/O if available
        try:
            io_counters = psutil.disk_io_counters()
            metrics['disk_read_mb'] = io_counters.read_bytes / (1024 * 1024)
            metrics['disk_write_mb'] = io_counters.write_bytes / (1024 * 1024)
        except:
            pass
        
        self.metrics.append(metrics)
        return metrics
    
    def generate_report(self):
        """Generate monitoring report"""
        if not self.start_time:
            return
        
        total_time = time.time() - self.start_time
        report_file = self.config.work_dir / "build_monitor.json"
        
        report = {
            'build_info': {
                'os_name': self.config.os_name,
                'version': self.config.version,
                'target_arch': self.config.target_arch,
                'start_time': datetime.fromtimestamp(self.start_time).isoformat(),
                'total_time_seconds': total_time,
                'total_time_formatted': self._format_time(total_time)
            },
            'checkpoints': self.checkpoints,
            'metrics': self.metrics
        }
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n[i] Monitoring report: {report_file}")
        self._print_summary(report)
    
    def _print_summary(self, report):
        """Print monitoring summary"""
        print("\n" + "="*60)
        print("Build Monitoring Summary")
        print("="*60)
        print(f"Total Time: {report['build_info']['total_time_formatted']}")
        print(f"\nCheckpoints:")
        for cp in report['checkpoints']:
            print(f"  {cp['name']}: {cp['elapsed_formatted']}")
        
        if self.metrics:
            avg_cpu = sum(m['cpu_percent'] for m in self.metrics) / len(self.metrics)
            avg_mem = sum(m['memory_percent'] for m in self.metrics) / len(self.metrics)
            print(f"\nAverage Resource Usage:")
            print(f"  CPU: {avg_cpu:.1f}%")
            print(f"  Memory: {avg_mem:.1f}%")
    
    def _format_time(self, seconds):
        """Format seconds to human readable"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        elif minutes > 0:
            return f"{minutes}m {secs}s"
        else:
            return f"{secs}s"

class ProgressTracker:
    """Tracks build progress with visual feedback"""
    
    def __init__(self):
        self.current_phase = None
        self.total_phases = 0
        self.completed_phases = 0
    
    def set_phases(self, phases: List[str]):
        """Set build phases"""
        self.total_phases = len(phases)
        self.completed_phases = 0
    
    def start_phase(self, phase_name: str):
        """Start a new phase"""
        self.current_phase = phase_name
        print(f"\n{'='*60}")
        print(f"Phase {self.completed_phases + 1}/{self.total_phases}: {phase_name}")
        print(f"{'='*60}")
    
    def complete_phase(self):
        """Mark current phase as complete"""
        self.completed_phases += 1
        progress = (self.completed_phases / self.total_phases) * 100
        print(f"[✓] Phase complete ({progress:.0f}% total)")
    
    def print_progress_bar(self, current: int, total: int, prefix: str = ''):
        """Print a progress bar"""
        bar_length = 40
        filled = int(bar_length * current / total)
        bar = '█' * filled + '░' * (bar_length - filled)
        percent = (current / total) * 100
        print(f'\r{prefix} |{bar}| {percent:.1f}%', end='', flush=True)
        
        if current == total:
            print()  # New line when complete
