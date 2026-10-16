# Day 27 — Backup Security

**Cybersecurity Internship Project | Veda Technology**  
**Project:** Basic Backup and Recovery Strategy for a Small Organization

## 1. Overview
This project demonstrates a simple, local backup workflow with timestamped backup folders, SHA-256 integrity hashes, and a verification command. It is an educational prototype—not a substitute for an organization's tested, access-controlled backup platform.

## 2. Objectives
- Apply the 3-2-1 backup principle.
- Create a dated backup of a chosen source folder.
- Record SHA-256 hashes to help detect accidental changes or corruption.
- Verify a backup against its manifest.
- Document recovery, access control, retention, and testing.

## 3. The 3-2-1 rule
- **3 copies** of important data: the original plus two backups.
- **2 different media/types** (for example, a workstation plus a NAS and cloud storage).
- **1 off-site copy** protected from local incidents.

For ransomware resilience, keep at least one backup offline or immutable, use separate backup credentials, and prevent ordinary users from deleting backup copies.

## 4. Example strategy
| Data | Frequency | Destination | Retention |
|---|---|---|---|
| Critical documents | Daily | Local backup drive/NAS | 30 daily copies |
| Full weekly backup | Weekly | Separate encrypted drive | 8 weekly copies |
| Off-site copy | Daily/weekly | Approved cloud or off-site location | Based on policy |
| Restore test | Monthly | Isolated test folder | Record results |

Set retention based on business needs, legal requirements, and storage capacity. Encrypt backup media and cloud transfers. Never store real passwords, customer data, or confidential company files in this demo repository.

## 5. Requirements
- Python 3.9+
- Standard library only (no third-party packages)
- A test folder containing files you are allowed to copy

## 6. Run the demo
From this repository folder:

```bash
python backup.py sample_data backups
```

Verify the newest backup (copy the path printed by the script):

```bash
python backup.py --verify "backups/backup_YYYYMMDD_HHMMSS"
```

The script writes `manifest.sha256.json` into each backup. The manifest stores relative file paths, file sizes, and SHA-256 hashes. A successful verification means the files match the manifest at verification time; it does not prove that the backup is complete, malware-free, or recoverable in every situation.

## 7. Recovery procedure
1. Identify the incident and stop unintended writes to the affected data.
2. Choose a known-good backup from before the incident.
3. Verify the backup manifest and scan files using approved security tools.
4. Restore to a **separate test directory first**; do not overwrite production data immediately.
5. Compare important files and confirm that applications/users can use the restored data.
6. Obtain owner approval before production recovery.
7. Record backup date, verification result, restore test result, and any gaps.

The demo's `restore.py` restores into a new destination and refuses to overwrite an existing destination directory.

```bash
python restore.py "backups/backup_YYYYMMDD_HHMMSS" "restore_test"
```

## 8. Security controls
- Use least-privilege access and separate backup administrator credentials.
- Encrypt backups at rest and in transit (this demo does not implement encryption).
- Keep an offline or immutable copy.
- Monitor failed backup jobs and alert an owner.
- Protect manifests and logs against unauthorized modification.
- Test restores regularly and document recovery time and recovery point objectives (RTO/RPO).
- Keep backup software and systems patched.

## 9. Evidence to capture
For the internship submission, capture screenshots of:
1. The repository file list.
2. Running `python backup.py sample_data backups`.
3. A successful `--verify` result.
4. A restore into a new directory and comparison of restored files.
5. Your GitHub repository URL.

Do not claim screenshots or cloud deployment that you have not actually completed.

## 10. Limitations
This is a local educational demo. It does not provide scheduling, encryption, immutable storage, cloud upload, access management, malware scanning, or enterprise monitoring. Add and test these controls before any real organizational use.

## 11. Interview questions
**What is the 3-2-1 backup rule?** Keep three copies of data, on two different media/types, with one copy off-site.

**Why test backups?** A completed backup job does not guarantee the data can be restored. Restore tests validate integrity and recovery steps.

**Why use hashes?** A cryptographic hash such as SHA-256 helps detect whether file contents differ from those recorded in a manifest.

## 12. Author
**Ritu Raj**  
Cybersecurity Internship — Day 27  
Project: Backup Security
