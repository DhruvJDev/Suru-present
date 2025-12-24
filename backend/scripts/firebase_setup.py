#!/usr/bin/env python
"""
Setup and manage Firebase Realtime Database for Suru A.I.

Usage:
    python backend/scripts/firebase_setup.py upload   # Upload app_mappings.json to Firebase
    python backend/scripts/firebase_setup.py download # Download app_mappings from Firebase (for testing)
    python backend/scripts/firebase_setup.py check    # Check Firebase connectivity
"""

import sys
import os
import json

# Add project root to path so we can import backend modules
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from backend.firebase_utils import (
    get_app_mappings_from_firebase,
    upload_app_mappings_to_firebase,
    get_firebase_key_path,
)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1].lower()

    if command == "upload":
        local_path = os.path.join(project_root, "data", "json", "app_mappings.json")
        if not os.path.isfile(local_path):
            print(f"Error: {local_path} not found")
            return
        print(f"Uploading {local_path} to Firebase...")
        success = upload_app_mappings_to_firebase(local_path)
        sys.exit(0 if success else 1)

    elif command == "download":
        print("Downloading app_mappings from Firebase...")
        data = get_app_mappings_from_firebase()
        print(json.dumps(data, indent=2))

    elif command == "check":
        print("Checking Firebase connectivity...")
        key_path = get_firebase_key_path()
        if not os.path.isfile(key_path):
            print(f"❌ Firebase key not found at: {key_path}")
            print(
                "📝 To set up Firebase:\n"
                "   1. Create a Firebase project at https://firebase.google.com/\n"
                "   2. Download a service account key JSON from:\n"
                "      Project Settings → Service Accounts → Generate Key\n"
                f"   3. Save it to: {key_path}\n"
            )
            return

        print(f"✅ Firebase key found at: {key_path}")
        data = get_app_mappings_from_firebase()
        if data:
            print(f"✅ Successfully fetched {len(data)} app mappings from Firebase")
        else:
            print("⚠️  No app_mappings found in Firebase (using local fallback)")

    else:
        print(f"Unknown command: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()
