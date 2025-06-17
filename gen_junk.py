#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_junk.py - Junk file generator for testing PyClean
coded by Br3noAraujo

Este script gera arquivos e pastas de "lixo digital" em diretórios comuns de teste até ser interrompido (Ctrl+C).
Mostra em tempo real a quantidade de arquivos e o tamanho total gerados.
"""
import os
import random
import string
import time
from pathlib import Path

JUNK_DIRS = [
    Path.home() / '.cache',
    Path('/var/cache'),
    Path('/tmp'),
    Path.home() / '.local/share/Trash',
    Path.home() / '.cache/thumbnails',
]

FILE_SIZE_RANGE = (1024, 1024 * 1024)  # 1KB a 1MB


def random_filename():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))

def human_readable_size(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"

def main():
    print('Generating junk files. Press Ctrl+C to stop...')
    total_files = 0
    total_size = 0
    try:
        while True:
            dir_choice = random.choice(JUNK_DIRS)
            dir_choice.mkdir(parents=True, exist_ok=True)
            fname = dir_choice / random_filename()
            fsize = random.randint(*FILE_SIZE_RANGE)
            try:
                with open(fname, 'wb') as f:
                    f.write(os.urandom(fsize))
                total_files += 1
                total_size += fsize
                print(f'Files: {total_files} | Total size: {human_readable_size(total_size)}', end='\r', flush=True)
            except PermissionError:
                pass
            time.sleep(0.05)
    except KeyboardInterrupt:
        print(f'\nStopped. Total junk generated: {total_files} files, {human_readable_size(total_size)}')
        print('You can now run PyClean to test the cleaning!')

if __name__ == '__main__':
    main() 