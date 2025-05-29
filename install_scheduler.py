#!/usr/bin/env python3
"""
AI Newsletter Scheduler Installation Script
Automatically sets up launchd service for daily newsletter scheduling on macOS
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path
import argparse

# Configuration
SCRIPT_DIR = Path(__file__).parent.absolute()
LAUNCHD_PLIST = "com.ainewsletter.daily.plist"
LAUNCHD_DIR = Path.home() / "Library" / "LaunchAgents"
REQUIRED_FILES = [
    "newsletter_scheduler.py",
    "run_newsletter.sh",
    "com.ainewsletter.daily.plist",
    "enhanced_newsletter_generator.py",
    "config.py"
]

def print_header():
    """Print installation header"""
    print("=" * 60)
    print("🤖 AI Newsletter Scheduler Installation")
    print("=" * 60)
    print()

def check_requirements():
    """Check if all required files exist"""
    print("📋 Checking requirements...")
    
    missing_files = []
    for file in REQUIRED_FILES:
        file_path = SCRIPT_DIR / file
        if not file_path.exists():
            missing_files.append(file)
        else:
            print(f"  ✅ {file}")
    
    if missing_files:
        print(f"\n❌ Missing required files:")
        for file in missing_files:
            print(f"  • {file}")
        return False
    
    print("✅ All required files found")
    return True

def check_python_dependencies():
    """Check Python dependencies"""
    print("\n🐍 Checking Python dependencies...")
    
    required_modules = [
        "holidays",
        "smtplib", 
        "email",
        "pathlib",
        "datetime",
        "logging",
        "argparse"
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError:
            missing_modules.append(module)
            print(f"  ❌ {module}")
    
    if missing_modules:
        print(f"\n⚠️ Missing Python modules: {', '.join(missing_modules)}")
        print("Installing missing modules...")
        
        for module in missing_modules:
            if module == "holidays":
                try:
                    subprocess.run([sys.executable, "-m", "pip", "install", "holidays"], 
                                 check=True, capture_output=True)
                    print(f"  ✅ Installed {module}")
                except subprocess.CalledProcessError:
                    print(f"  ❌ Failed to install {module}")
                    return False
    
    print("✅ All Python dependencies satisfied")
    return True

def setup_directories():
    """Create necessary directories"""
    print("\n📁 Setting up directories...")
    
    # Create logs directory
    logs_dir = SCRIPT_DIR / "logs"
    logs_dir.mkdir(exist_ok=True)
    print(f"  ✅ Created logs directory: {logs_dir}")
    
    # Create LaunchAgents directory if it doesn't exist
    LAUNCHD_DIR.mkdir(parents=True, exist_ok=True)
    print(f"  ✅ LaunchAgents directory ready: {LAUNCHD_DIR}")
    
    return True

def install_launchd_service():
    """Install the launchd service"""
    print("\n🔧 Installing launchd service...")
    
    source_plist = SCRIPT_DIR / LAUNCHD_PLIST
    target_plist = LAUNCHD_DIR / LAUNCHD_PLIST
    
    try:
        # Copy plist file to LaunchAgents
        shutil.copy2(source_plist, target_plist)
        print(f"  ✅ Copied plist to: {target_plist}")
        
        # Load the service
        result = subprocess.run([
            "launchctl", "load", str(target_plist)
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("  ✅ launchd service loaded successfully")
        else:
            print(f"  ⚠️ launchctl load warning: {result.stderr}")
            # This might not be an error - service might already be loaded
        
        # Enable the service
        result = subprocess.run([
            "launchctl", "enable", f"gui/{os.getuid()}/com.ainewsletter.daily"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("  ✅ launchd service enabled successfully")
        else:
            print(f"  ⚠️ launchctl enable warning: {result.stderr}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Failed to install launchd service: {e}")
        return False

def test_scheduler():
    """Test the scheduler configuration"""
    print("\n🧪 Testing scheduler configuration...")
    
    try:
        # Test the scheduler
        result = subprocess.run([
            sys.executable, str(SCRIPT_DIR / "newsletter_scheduler.py"), "--test"
        ], capture_output=True, text=True, cwd=SCRIPT_DIR)
        
        if result.returncode == 0:
            print("  ✅ Scheduler configuration test passed")
            return True
        else:
            print(f"  ❌ Scheduler test failed:")
            print(f"    {result.stderr}")
            return False
            
    except Exception as e:
        print(f"  ❌ Failed to test scheduler: {e}")
        return False

def show_status():
    """Show current scheduler status"""
    print("\n📊 Scheduler Status:")
    
    try:
        # Check if service is loaded
        result = subprocess.run([
            "launchctl", "list", "com.ainewsletter.daily"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("  ✅ Service is loaded and active")
            
            # Parse the output for more details
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if line.strip():
                    print(f"    {line}")
        else:
            print("  ❌ Service is not loaded")
            
    except Exception as e:
        print(f"  ❌ Failed to check status: {e}")

def show_next_run():
    """Show when the newsletter will next run"""
    print("\n⏰ Next Scheduled Runs:")
    
    try:
        from datetime import datetime, timedelta
        import calendar
        
        now = datetime.now()
        
        # Find next 5 weekdays at 7 AM
        next_runs = []
        check_date = now.replace(hour=7, minute=0, second=0, microsecond=0)
        
        # If it's already past 7 AM today and today is a weekday, start from tomorrow
        if now.hour >= 7 and now.weekday() < 5:
            check_date += timedelta(days=1)
        
        days_checked = 0
        while len(next_runs) < 5 and days_checked < 14:
            if check_date.weekday() < 5:  # Monday=0, Friday=4
                next_runs.append(check_date)
            check_date += timedelta(days=1)
            days_checked += 1
        
        for run_time in next_runs:
            day_name = calendar.day_name[run_time.weekday()]
            print(f"  📅 {day_name}, {run_time.strftime('%B %d, %Y at %I:%M %p')}")
            
    except Exception as e:
        print(f"  ❌ Failed to calculate next runs: {e}")

def show_management_commands():
    """Show useful management commands"""
    print("\n🛠️ Management Commands:")
    print(f"  Start service:    launchctl load ~/Library/LaunchAgents/{LAUNCHD_PLIST}")
    print(f"  Stop service:     launchctl unload ~/Library/LaunchAgents/{LAUNCHD_PLIST}")
    print(f"  Check status:     launchctl list com.ainewsletter.daily")
    print(f"  View logs:        tail -f {SCRIPT_DIR}/logs/newsletter_scheduler.log")
    print(f"  Test scheduler:   python3 {SCRIPT_DIR}/newsletter_scheduler.py --test")
    print(f"  Force run:        python3 {SCRIPT_DIR}/newsletter_scheduler.py --force")
    print(f"  Dry run:          python3 {SCRIPT_DIR}/newsletter_scheduler.py --dry-run")

def uninstall_scheduler():
    """Uninstall the scheduler"""
    print("\n🗑️ Uninstalling AI Newsletter Scheduler...")
    
    target_plist = LAUNCHD_DIR / LAUNCHD_PLIST
    
    try:
        # Unload the service
        if target_plist.exists():
            subprocess.run([
                "launchctl", "unload", str(target_plist)
            ], capture_output=True)
            print("  ✅ Service unloaded")
            
            # Remove plist file
            target_plist.unlink()
            print("  ✅ Plist file removed")
        else:
            print("  ⚠️ Service was not installed")
        
        print("✅ Scheduler uninstalled successfully")
        return True
        
    except Exception as e:
        print(f"  ❌ Failed to uninstall scheduler: {e}")
        return False

def main():
    """Main installation function"""
    parser = argparse.ArgumentParser(
        description='AI Newsletter Scheduler Installation',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--uninstall', action='store_true',
                       help='Uninstall the scheduler')
    parser.add_argument('--status', action='store_true',
                       help='Show scheduler status')
    parser.add_argument('--test-only', action='store_true',
                       help='Only test configuration, do not install')
    
    args = parser.parse_args()
    
    print_header()
    
    if args.uninstall:
        success = uninstall_scheduler()
        sys.exit(0 if success else 1)
    
    if args.status:
        show_status()
        show_next_run()
        show_management_commands()
        sys.exit(0)
    
    # Check system compatibility
    if sys.platform != "darwin":
        print("❌ This installer is designed for macOS only")
        sys.exit(1)
    
    # Run installation steps
    steps = [
        ("Checking requirements", check_requirements),
        ("Checking Python dependencies", check_python_dependencies),
        ("Setting up directories", setup_directories),
    ]
    
    if not args.test_only:
        steps.append(("Installing launchd service", install_launchd_service))
    
    steps.append(("Testing scheduler", test_scheduler))
    
    # Execute steps
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Installation failed at: {step_name}")
            sys.exit(1)
    
    # Show final status
    if not args.test_only:
        print("\n🎉 Installation completed successfully!")
        show_next_run()
        show_management_commands()
        
        print("\n📧 Important Notes:")
        print("  • Make sure your .env file is configured with email settings")
        print("  • The scheduler will run Monday-Friday at 7:00 AM")
        print("  • Check logs in the 'logs' directory if issues occur")
        print("  • Your Mac should be plugged in for reliable scheduling")
    else:
        print("\n✅ Configuration test completed successfully!")

if __name__ == "__main__":
    main()
