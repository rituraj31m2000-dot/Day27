#!/usr/bin/env python3
"""Restore a verified demo backup into a new destination directory."""
import json
import shutil
import sys
from pathlib import Path
from backup import MANIFEST, sha256_file

def main():
    if len(sys.argv) != 3:
        print('Usage: python restore.py "BACKUP_DIR" "NEW_DESTINATION"')
        raise SystemExit(2)
    backup_dir = Path(sys.argv[1]).resolve()
    destination = Path(sys.argv[2]).resolve()
    manifest_path = backup_dir / MANIFEST
    if not manifest_path.is_file():
        print("ERROR: backup manifest not found.")
        raise SystemExit(1)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for item in manifest.get("files", []):
        rel = Path(item["path"])
        if rel.is_absolute() or ".." in rel.parts:
            print(f"ERROR: unsafe path in manifest: {rel}")
            raise SystemExit(1)
        source = backup_dir / rel
        if not source.is_file() or sha256_file(source) != item["sha256"]:
            print(f"ERROR: verification failed for {rel}; restore cancelled.")
            raise SystemExit(1)
    if destination.exists():
        print("ERROR: destination already exists. Choose a new, empty path.")
        raise SystemExit(1)
    destination.mkdir(parents=True)
    for item in manifest.get("files", []):
        rel = Path(item["path"])
        target = destination / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(backup_dir / rel, target)
    print(f"Restore completed to: {destination}")
    print(f"Restored files: {len(manifest.get('files', []))}")
    print("Review the restored data before using it in production.")

if __name__ == "__main__":
    main()
