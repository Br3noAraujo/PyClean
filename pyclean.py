#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyClean - Linux digital junk cleaner utility
coded by Br3noAraujo

LEGAL DISCLAIMER:

This script is provided solely for educational and maintenance purposes. By using this tool, you acknowledge and accept the following:

- You are solely responsible for any actions performed with this script and for any consequences that may arise, including but not limited to data loss, system instability, or other damages.
- The author does not provide any warranty, express or implied, and shall not be held liable for any direct, indirect, incidental, or consequential damages resulting from the use or misuse of this script.
- It is your duty to ensure you have proper backups and understand the impact of deleting files or directories before proceeding.
- Use of this script on systems you do not own or without explicit authorization is strictly prohibited and may be illegal.
- By executing this script, you agree to these terms and assume full responsibility for your actions.

Thank you for using PyClean responsibly.
"""
import argparse
import os
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import Tuple
import sys
import subprocess

# Directories and patterns for cleaning
CLEAN_PATHS = [
    Path.home() / '.cache',
    Path('/var/cache'),
    Path('/tmp'),
    Path.home() / '.local/share/Trash',
    Path.home() / '.cache/thumbnails',
]
SNAP_PATH = Path.home() / 'snap'
LOG_PATH = Path('/var/log')

# Cores frias para o terminal
BLUE = '\033[94m'
CYAN = '\033[96m'
GREEN = '\033[92m'
BOLD = '\033[1m'
RESET = '\033[0m'
RED = '\033[91m'

# Helper: check if a path is safe to delete
def is_safe_to_delete(path: Path) -> bool:
    # Never allow deletion of root, home, or system dirs
    unsafe = [Path('/'), Path.home(), Path('/bin'), Path('/usr'), Path('/etc'), Path('/lib'), Path('/sbin'), Path('/boot')]
    try:
        return not any(str(path).startswith(str(u)) for u in unsafe)
    except Exception:
        return False

def get_size_and_count(path: Path) -> Tuple[int, int]:
    total_size = 0
    total_count = 0
    if not path.exists():
        return 0, 0
    if path.is_file():
        return path.stat().st_size, 1
    for root, dirs, files in os.walk(str(path), onerror=lambda e: None):
        for f in files:
            try:
                fp = Path(root) / f
                total_size += fp.stat().st_size
                total_count += 1
            except Exception:
                continue
    return total_size, total_count

def human_readable_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"

# Helper: delete a file or directory
def delete_path(path: Path, dry_run: bool = False, verbose: bool = False):
    try:
        if dry_run:
            if verbose:
                print(f'[DRY-RUN] Would remove: {path}')
            return True
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
            if verbose:
                print(f'Removed directory: {path}')
        else:
            path.unlink(missing_ok=True)
            if verbose:
                print(f'Removed file: {path}')
        return True
    except Exception:
        return False  # Ignore errors silently

def list_no_extension_files(base: Path) -> list:
    if not base.exists() or not base.is_dir():
        return []
    result = []
    for f in base.iterdir():
        try:
            if f.is_file() and f.suffix == '':
                result.append(f)
        except Exception:
            continue
    return result

# Clean cache, temp, trash, thumbnails
def clean_standard(dry_run: bool = False, aggressive: bool = False, verbose: bool = False, list_only: bool = False):
    count = 0
    size = 0
    noext_count = 0
    noext_size = 0
    for base in CLEAN_PATHS:
        if not base.exists():
            continue
        # Arquivos sem extensão
        noext_files = list_no_extension_files(base)
        for f in noext_files:
            fsize = f.stat().st_size
            if list_only:
                print(f'{CYAN}[noext]{RESET} {f} - {human_readable_size(fsize)}')
                noext_count += 1
                noext_size += fsize
            else:
                removed = delete_path(f, dry_run, verbose)
                if removed:
                    noext_count += 1
                    noext_size += fsize
        # Demais arquivos/pastas
        for item in base.iterdir():
            if is_safe_to_delete(item):
                # Evita contar duas vezes arquivos sem extensão
                if item.is_file() and item.suffix == '':
                    continue
                item_size, item_count = get_size_and_count(item)
                if list_only:
                    print(f'{item} - {human_readable_size(item_size)} - {item_count} items')
                    count += item_count
                    size += item_size
                else:
                    if delete_path(item, dry_run, verbose):
                        count += item_count
                        size += item_size
    if list_only:
        if noext_count:
            print(f'{CYAN}No-extension files: {noext_count} files, {human_readable_size(noext_size)}{RESET}')
        print(f'{CYAN}Total (standard): {count} items, {human_readable_size(size)}{RESET}')
    else:
        if noext_count:
            print(f'{CYAN}No-extension files cleaned: {noext_count} files, {human_readable_size(noext_size)}{RESET}')
        print(f'{BLUE}Total cleaned (standard): {count} items, {human_readable_size(size)}{RESET}')

# Clean logs (keep current logs, remove rotated/old)
def clean_logs(dry_run: bool = False, aggressive: bool = False, verbose: bool = False, list_only: bool = False):
    if not LOG_PATH.exists():
        return
    count = 0
    size = 0
    for log in LOG_PATH.iterdir():
        if log.is_file():
            if log.suffix in ['.gz', '.1', '.old', '.xz', '.zip'] or log.name.endswith(('.gz', '.1', '.old', '.xz', '.zip')) or (aggressive and log.name != 'lastlog'):
                log_size = log.stat().st_size
                if list_only:
                    print(f'{log} - {human_readable_size(log_size)}')
                    count += 1
                    size += log_size
                else:
                    if delete_path(log, dry_run, verbose):
                        count += 1
                        size += log_size
    if list_only:
        print(f'Total logs: {count} items, {human_readable_size(size)}')
    else:
        print(f'Total logs cleaned: {count} items, {human_readable_size(size)}')

# Clean orphaned Snap folders
def clean_snap_leftovers(dry_run: bool = False, aggressive: bool = False, verbose: bool = False, list_only: bool = False):
    if not SNAP_PATH.exists():
        return
    count = 0
    size = 0
    for folder in SNAP_PATH.iterdir():
        if folder.is_dir():
            folder_size, folder_count = get_size_and_count(folder)
            if not any(folder.iterdir()) or aggressive:
                if list_only:
                    print(f'{folder} - {human_readable_size(folder_size)} - {folder_count} items')
                    count += folder_count
                    size += folder_size
                else:
                    if delete_path(folder, dry_run, verbose):
                        count += folder_count
                        size += folder_size
    if list_only:
        print(f'Total Snap leftovers: {count} items, {human_readable_size(size)}')
    else:
        print(f'Total Snap leftovers cleaned: {count} items, {human_readable_size(size)}')

# Clean a specific target path
def clean_target(target: Path, dry_run: bool = False, verbose: bool = False, list_only: bool = False):
    if not target.exists():
        print(f'Target does not exist: {target}')
        return
    if not is_safe_to_delete(target):
        print(f'Not safe to delete: {target}')
        return
    size, count = get_size_and_count(target)
    if list_only:
        print(f'{target} - {human_readable_size(size)} - {count} items')
        print(f'Target total: {count} items, {human_readable_size(size)}')
    else:
        if delete_path(target, dry_run, verbose):
            print(f'Target cleaned: {target} ({count} items, {human_readable_size(size)})')

def is_root():
    return os.geteuid() == 0

def reinvoke_with_sudo():
    print(f'{RED}WARNING: Root privileges are required for aggressive cleaning. You will be prompted for your password. Proceed with caution!{RESET}')
    print(f'{CYAN}Re-running with sudo for aggressive cleaning...{RESET}')
    try:
        cmd = ['sudo', sys.executable] + sys.argv
        os.execvp('sudo', cmd)
    except Exception as e:
        print(f'{RED}Failed to elevate privileges: {e}{RESET}')
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description=f'{BOLD}{BLUE}PyClean - Linux digital junk cleaner{RESET}',
        epilog=f'{CYAN}Examples:{RESET}\n'
               f'  {BOLD}python pyclean.py -l{RESET}        {CYAN}# List digital junk only{RESET}\n'
               f'  {BOLD}python pyclean.py -a -v{RESET}     {CYAN}# Aggressive clean, verbose{RESET}\n'
               f'  {BOLD}python pyclean.py -t ~/Downloads -l{RESET} {CYAN}# List junk in Downloads{RESET}\n',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--dry-run', '-dr', action='store_true', help=f'{CYAN}List what would be deleted, but do not delete{RESET}')
    parser.add_argument('--aggressive', '-a', action='store_true', help=f'{CYAN}Delete everything, including logs and Snap leftovers{RESET}')
    parser.add_argument('--target', '-t', type=str, help=f'{CYAN}Clean a specific folder or file{RESET}')
    parser.add_argument('--verbose', '-v', action='store_true', help=f'{CYAN}Show each file/folder being deleted{RESET}')
    parser.add_argument('--list', '-l', action='store_true', help=f'{CYAN}List what is taking up space and how many items, do not delete{RESET}')
    args = parser.parse_args()

    if args.aggressive and not is_root():
        reinvoke_with_sudo()
        sys.exit(0)

    if is_root() and os.environ.get('SUDO_USER'):
        print(f'{CYAN}NOTICE: Running as root (sudo). The script will use root\'s home directory (~/ = /root) for cleaning. To clean your user\'s home, execute without sudo.{RESET}')

    if args.list:
        print(f'{BOLD}{BLUE}Listing digital junk:{RESET}')
        if args.target:
            clean_target(Path(args.target).expanduser(), dry_run=True, verbose=False, list_only=True)
            return
        clean_standard(dry_run=True, aggressive=args.aggressive, verbose=False, list_only=True)
        clean_logs(dry_run=True, aggressive=args.aggressive, verbose=False, list_only=True)
        clean_snap_leftovers(dry_run=True, aggressive=args.aggressive, verbose=False, list_only=True)
        print(f'{BOLD}{CYAN}Listing finished.{RESET}')
        return

    print(f'{BOLD}{CYAN}Cleaning...{RESET}')
    if args.target:
        clean_target(Path(args.target).expanduser(), dry_run=args.dry_run, verbose=args.verbose, list_only=False)
        return
    clean_standard(dry_run=args.dry_run, aggressive=args.aggressive, verbose=args.verbose, list_only=False)
    clean_logs(dry_run=args.dry_run, aggressive=args.aggressive, verbose=args.verbose, list_only=False)
    clean_snap_leftovers(dry_run=args.dry_run, aggressive=args.aggressive, verbose=args.verbose, list_only=False)
    print(f'{BOLD}{GREEN}PyClean finished.{RESET}')

if __name__ == '__main__':
    main()