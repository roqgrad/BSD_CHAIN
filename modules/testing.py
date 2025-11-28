"""Testing and validation module"""

import subprocess
import sys
from pathlib import Path

class TestRunner:
    """Runs tests and validation"""
    
    def __init__(self, config):
        self.config = config
        self.test_results = []
    
    def run_all_tests(self):
        """Run all test suites"""
        print("[*] Running test suites...")
        
        self._test_kernel_build()
        self._test_world_build()
        self._test_boot_loader()
        self._generate_test_report()
    
    def _test_kernel_build(self):
        """Test kernel build"""
        print("[*] Testing kernel build...")
        
        kernel_path = self.config.obj_dir / "usr/src" / self.config.target_arch / "sys" / \
                      (self.config.custom_kernel_config or self.config.kernel_config) / "kernel"
        
        if kernel_path.exists():
            print("[✓] Kernel binary exists")
            self.test_results.append(("Kernel Build", "PASS", "Kernel binary found"))
        else:
            print("[✗] Kernel binary not found")
            self.test_results.append(("Kernel Build", "FAIL", "Kernel binary missing"))
    
    def _test_world_build(self):
        """Test world build"""
        print("[*] Testing world build...")
        
        # Check for essential binaries
        essential_bins = ["bin/sh", "sbin/init", "usr/bin/login"]
        
        for bin_path in essential_bins:
            full_path = self.config.dist_dir / bin_path
            if full_path.exists():
                print(f"[✓] {bin_path} exists")
                self.test_results.append((f"Binary: {bin_path}", "PASS", "Binary found"))
            else:
                print(f"[✗] {bin_path} missing")
                self.test_results.append((f"Binary: {bin_path}", "FAIL", "Binary missing"))
    
    def _test_boot_loader(self):
        """Test boot loader"""
        print("[*] Testing boot loader...")
        
        loader_path = self.config.dist_dir / "boot/loader"
        if loader_path.exists():
            print("[✓] Boot loader exists")
            self.test_results.append(("Boot Loader", "PASS", "Loader found"))
        else:
            print("[✗] Boot loader missing")
            self.test_results.append(("Boot Loader", "FAIL", "Loader missing"))
    
    def _generate_test_report(self):
        """Generate test report"""
        report_file = self.config.work_dir / "test_report.txt"
        
        passed = sum(1 for _, status, _ in self.test_results if status == "PASS")
        failed = sum(1 for _, status, _ in self.test_results if status == "FAIL")
        
        with open(report_file, 'w') as f:
            f.write(f"{self.config.os_name} Test Report\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Total Tests: {len(self.test_results)}\n")
            f.write(f"Passed: {passed}\n")
            f.write(f"Failed: {failed}\n\n")
            
            f.write("Test Results:\n")
            f.write("-" * 50 + "\n")
            for test_name, status, message in self.test_results:
                f.write(f"{test_name}: {status} - {message}\n")
        
        print(f"\n[i] Test report: {report_file}")
        print(f"[i] Tests passed: {passed}/{len(self.test_results)}")

class VMTester:
    """Test OS in virtual machine"""
    
    def __init__(self, config):
        self.config = config
    
    def test_in_qemu(self):
        """Test OS in QEMU"""
        print("[*] Testing in QEMU...")
        
        iso_file = self.config.work_dir / f"{self.config.os_name}_{self.config.version}_{self.config.target_arch}.iso"
        
        if not iso_file.exists():
            print("[!] ISO file not found")
            return
        
        cmd = [
            'qemu-system-x86_64',
            '-cdrom', str(iso_file),
            '-m', '2048',
            '-boot', 'd',
            '-display', 'none',
            '-serial', 'stdio'
        ]
        
        print("[i] Starting QEMU (press Ctrl+C to stop)...")
        try:
            subprocess.run(cmd)
        except FileNotFoundError:
            print("[!] QEMU not found. Install qemu to test in VM.")
        except KeyboardInterrupt:
            print("\n[i] QEMU stopped")
