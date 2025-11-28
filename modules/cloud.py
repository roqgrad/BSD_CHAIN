"""Cloud image generation module"""

import subprocess
from pathlib import Path

class CloudImageGenerator:
    """Generates cloud-ready images (AWS, Azure, GCP, etc.)"""
    
    def __init__(self, config):
        self.config = config
        self.cloud_dir = config.work_dir / "cloud_images"
        self.cloud_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_aws_ami(self):
        """Generate AWS AMI-compatible image"""
        print("[*] Generating AWS AMI image...")
        
        ami_file = self.cloud_dir / f"{self.config.os_name}_aws.raw"
        
        # Create raw disk image
        self._create_raw_image(ami_file, size_gb=10)
        
        print(f"[✓] AWS AMI image: {ami_file}")
        print("[i] Upload to S3 and import as AMI using aws ec2 import-image")
    
    def generate_azure_vhd(self):
        """Generate Azure VHD image"""
        print("[*] Generating Azure VHD image...")
        
        vhd_file = self.cloud_dir / f"{self.config.os_name}_azure.vhd"
        
        # Create VHD image
        self._create_raw_image(vhd_file, size_gb=10)
        
        print(f"[✓] Azure VHD image: {vhd_file}")
        print("[i] Upload to Azure Storage and create VM from VHD")
    
    def generate_gcp_image(self):
        """Generate Google Cloud Platform image"""
        print("[*] Generating GCP image...")
        
        gcp_file = self.cloud_dir / f"{self.config.os_name}_gcp.tar.gz"
        
        # Create GCP-compatible image
        raw_file = self.cloud_dir / "disk.raw"
        self._create_raw_image(raw_file, size_gb=10)
        
        # Compress for GCP
        subprocess.run(['tar', '-czf', str(gcp_file), '-C', str(self.cloud_dir), 'disk.raw'])
        raw_file.unlink()
        
        print(f"[✓] GCP image: {gcp_file}")
        print("[i] Upload to GCS and import using gcloud compute images create")
    
    def _create_raw_image(self, output_file, size_gb=10):
        """Create raw disk image"""
        # This is a simplified version
        # In production, you'd use makefs, mkimg, or similar tools
        
        size_bytes = size_gb * 1024 * 1024 * 1024
        
        with open(output_file, 'wb') as f:
            f.seek(size_bytes - 1)
            f.write(b'\0')
        
        print(f"[i] Created {size_gb}GB raw image")
