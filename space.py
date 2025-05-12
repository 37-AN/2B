#!/usr/bin/env python
"""
Register this app with Hugging Face Spaces SDK.
This file is used for deploying the app to Hugging Face Spaces.
"""
import os
import subprocess
import sys
from huggingface_hub import SpaceHardware, SpaceStage, SpaceSDK

def create_space():
    """Create or update a Hugging Face Space."""
    # Get the Space name or use a default
    space_name = os.environ.get("SPACE_NAME", "personal-rag-assistant")
    owner = os.environ.get("HF_USERNAME")
    
    if not owner:
        print("Please set the HF_USERNAME environment variable to your Hugging Face username.")
        sys.exit(1)
    
    # Initialize the SDK
    sdk = SpaceSDK(
        space_id=f"{owner}/{space_name}",
        token=os.environ.get("HF_TOKEN")
    )
    
    # Check if space exists, if not create it
    try:
        space_info = sdk.get_space_runtime()
        print(f"Space {owner}/{space_name} exists.")
        exists = True
    except Exception:
        exists = False
    
    # Create or update the space
    if not exists:
        print(f"Creating new space: {owner}/{space_name}")
        sdk.create_space(
            space_hardware=SpaceHardware.CPU_BASIC,
            space_storage=1,
            space_sleep_time=3600,  # 1 hour of inactivity before sleep
            space_stage=SpaceStage.RUNNING,
        )
    
    print(f"Space URL: https://huggingface.co/spaces/{owner}/{space_name}")
    return sdk

if __name__ == "__main__":
    create_space() 