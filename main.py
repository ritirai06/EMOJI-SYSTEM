#!/usr/bin/env python3
"""
Emoji Matching AI - Main Entry Point
"""

import sys
import os
import subprocess

def run_script(script_path):
    """Run a Python script and handle errors."""
    try:
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_path}:")
        print(e.stderr)
        return False

def main():
    """Run the complete emoji matching AI pipeline."""
    
    print("🚀 Emoji Matching AI Pipeline")
    print("=" * 40)
    
    scripts = [
        ("📥 Downloading emojis", "scripts/1_download_emojis.py"),
        ("📝 Generating descriptions", "scripts/2_generate_descriptions.py"),
        ("🔄 Creating embeddings", "scripts/3_create_embeddings.py"),
        ("🗄️ Building vector database", "scripts/4_build_vectordb.py"),
        ("🔍 Running similarity search", "scripts/5_similarity_search.py")
    ]
    
    for step_name, script_path in scripts:
        print(f"\n{step_name}...")
        
        if not os.path.exists(script_path):
            print(f"❌ Script not found: {script_path}")
            continue
            
        success = run_script(script_path)
        
        if not success:
            print(f"❌ Pipeline stopped at: {step_name}")
            break
        
        print(f"✅ {step_name} completed")
    
    print("\n🎉 Pipeline complete!")

if __name__ == "__main__":
    main()