#!/usr/bin/env python3
"""Educational local backup utility with SHA-256 manifest verification."""
import argparse
import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path

MANIFEST = "manifest.sha256.json"

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def verify_backup(backup_dir: Path) -> bool:
    manifest_path = backup_dir / MANIFEST
    if not manifest_path.is_file():
        print(f"ERROR: manifest not found: {manifest_path}")
        return False
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read manifest: {exc}")
        return False

    failures = []
    for item in manifest.get("files", []):
        rel = Path(item["path"])
        if rel.is_absolute() or ".." in rel.parts:
            failures.append(f"Unsafe manifest path: {rel}")
            continue
        target = backup_dir / rel
        if not target.is_file():
            failures.append(f"MISSING: {rel}")
            continue
        actual_hash = sha256_file(target)
        if actual_hash != item["sha256"]:
            failures.append(f"HASH MISMATCH: {rel}")
        if target.stat().st_size != item["size_bytes"]:
            failures.append(f"SIZE MISMATCH: {rel}")

    if failures:
        print("Verification FAILED:")
        for failure in failures:
            print(f" - {failure}")
        return False
    print(f"Verification PASSED: {len(manifest.get('files', []))} file(s) match the manifest.")
    return True

def create_backup(source: Path, destination_root: Path) -> Path:
    source = source.resolve()
    destination_root = destination_root.resolve()
    if not source.is_dir():
        raise ValueError(f"Source directory does not exist: {source}")
    if destination_root == source or source in destination_root.parents:
        raise ValueError("Backup destination must not be inside the source directory.")
    destination_root.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = destination_root / f"backup_{stamp}"
    backup_dir.mkdir()
    entries = []
    try:
        for path in sorted(source.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(source)
            target = backup_dir / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            entries.append({
                "path": relative.as_posix(),
                "size_bytes": target.stat().st_size,
                "sha256": sha256_file(target)
            })
        manifest = {
            "created_at": datetime.now().astimezone().isoformat(),
            "source_directory": str(source),
            "hash_algorithm": "SHA-256",
            "files": entries
        }
        (backup_dir / MANIFEST).write_text(
            json.dumps(manifest, indent=2), encoding="utf-8"
        )
    except Exception:
        shutil.rmtree(backup_dir, ignore_errors=True)
        raise
    print(f"Backup created: {backup_dir}")
    print(f"Files copied: {len(entries)}")
    print(f"Verify with: python backup.py --verify \"{backup_dir}\"")
    return backup_dir

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", help="Source folder to back up")
    parser.add_argument("destination", nargs="?", help="Folder in which backups are stored")
    parser.add_argument("--verify", metavar="BACKUP_DIR", help="Verify an existing backup")
    args = parser.parse_args()
    if args.verify:
        raise SystemExit(0 if verify_backup(Path(args.verify)) else 1)
    if not args.source or not args.destination:
        parser.error("provide SOURCE DESTINATION, or use --verify BACKUP_DIR")
    try:
        create_backup(Path(args.source), Path(args.destination))
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

if __name__ == "__main__":
    main()
