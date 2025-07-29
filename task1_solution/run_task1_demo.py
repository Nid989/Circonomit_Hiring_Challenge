#!/usr/bin/env python3
"""
STK Produktion Task-1 Demo Runner
Simple script to execute the comprehensive demonstration

Usage: python run_task1_demo.py
"""

import sys
import subprocess
import importlib.util

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'langgraph',
        'typing_extensions'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        if importlib.util.find_spec(package) is None:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required dependencies:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nPlease install missing packages:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def main():
    """Main execution function"""
    print("🚀 STK Produktion Task-1 Demo Runner")
    print("="*50)
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        print("❌ Dependency check failed. Please install required packages.")
        return 1
    
    print("✅ All dependencies satisfied")
    
    # Run the demonstration
    print("\n🏭 Starting STK Produktion demonstration...")
    print("="*50)
    
    try:
        # Import and run the demo
        from stk_demo import main as demo_main
        return demo_main()
        
    except ImportError as e:
        print(f"❌ Failed to import demo module: {e}")
        return 1
    except Exception as e:
        print(f"❌ Demo execution failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 