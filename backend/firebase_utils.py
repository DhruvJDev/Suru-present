import os
import json
from typing import Optional, Dict, Any
import requests

# Global flag to track Firebase initialization
_firebase_initialized = False


def get_firebase_key_path() -> str:
    """Return path to Firebase service account key."""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "firebase_key.json")


def get_app_mappings_from_firebase() -> Dict[str, Any]:
    """
    Fetch app_mappings from Firebase Realtime Database using public REST API.
    No authentication required - users can clone and run immediately.
    """

    # Firebase Realtime Database public REST API endpoint
    firebase_public_url = "url_to_your_firebase_database/app_mappings.json"
    
    try:
        print("Fetching app_mappings from Firebase...")
        resp = requests.get(firebase_public_url, timeout=10)
        
        if resp.status_code == 200:
            data = resp.json()
            if data:
                print("✅ Successfully fetched app_mappings from Firebase")
                return data
            else:
                print("❌ Firebase returned empty data")
                return {}
        else:
            print(f"❌ Firebase API returned status {resp.status_code}")
            return {}
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to fetch from Firebase: {e}")
        return {}
    except Exception as e:
        print(f"❌ Unexpected error fetching Firebase data: {e}")
        return {}


def _get_firebase_url_from_key(key_path: str) -> str:
    """Extract Firebase Realtime Database URL from service account key JSON.
    
    Note: The URL format depends on the region. Modern Firebase projects may use
    URLs like: https://{project_id}-default-rtdb.{region}.firebasedatabase.app/
    
    Try custom URL via environment variable first, then default to regional format.
    """
    try:
        # Check if user provided a custom database URL via environment variable
        custom_url = os.environ.get("FIREBASE_DATABASE_URL")
        if custom_url:
            return custom_url
            
        with open(key_path, "r") as f:
            key_data = json.load(f)
            project_id = key_data.get("project_id", "")
            if not project_id:
                raise ValueError("project_id not found in Firebase key")
            
            # Try regional format first (modern Firebase)
            # Default to asia-southeast1 region - can be overridden via env var
            region = os.environ.get("FIREBASE_REGION", "asia-southeast1")
            return f"https://{project_id}-default-rtdb.{region}.firebasedatabase.app"
    except Exception as e:
        raise ValueError(f"Failed to extract Firebase URL from key: {e}")


def upload_app_mappings_to_firebase(
    local_json_path: str,
) -> bool:
    """
    Upload app mappings from a local JSON file to Firebase Realtime Database.

    Args:
        local_json_path: Path to the local JSON file to upload.

    Returns:
        True if successful, False otherwise.
    """
    try:
        import firebase_admin
        from firebase_admin import db
    except ImportError:
        print("Error: firebase-admin not installed. Run: pip install firebase-admin")
        return False

    try:
        # Initialize Firebase if not already done
        try:
            app = firebase_admin.get_app(name="default")
        except ValueError:
            # App not initialized, initialize it now
            key_path = get_firebase_key_path()
            if not os.path.isfile(key_path):
                print(f"Error: Firebase service account key not found at {key_path}")
                return False

            cred = firebase_admin.credentials.Certificate(key_path)
            db_url = _get_firebase_url_from_key(key_path)
            firebase_admin.initialize_app(
                cred,
                {"databaseURL": db_url},
                name="default",
            )

        # Load and upload data
        with open(local_json_path, "r") as f:
            data = json.load(f)

        ref = db.reference("app_mappings")
        ref.set(data)

        print(f"✅ Successfully uploaded app_mappings to Firebase from {local_json_path}")
        return True

    except Exception as e:
        print(f"❌ Error: Failed to upload to Firebase: {e}")
        import traceback
        traceback.print_exc()
        return False
