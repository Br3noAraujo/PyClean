# PyClean 🧹🐧
# ![PyClean Banner](https://i.imgur.com/k19tpaJ.png)
**PyClean** is a powerful, safe and customizable digital junk cleaner for Linux systems. Clean up cache, temp files, logs, thumbnails, Snap leftovers and more — all from your terminal!

---

## ✨ Features

- Clean user and system caches (`~/.cache`, `/var/cache`)
- Remove temp files (`/tmp`, `~/.local/share/Trash`)
- Delete old logs (with safe and aggressive modes)
- Clean thumbnails and Snap orphan folders
- Special handling for files with no extension
- Dry-run, verbose, and listing modes
- Colorful, modern CLI output
- Compatible with Python 3.7+

---

## 🚀 Installation

```bash
git clone https://github.com/Br3noAraujo/PyClean.git
cd PyClean
python3 pyclean.py -h
```

---

## 🛠️ Usage

### Basic Cleaning
```bash
python3 pyclean.py
```

### Aggressive Cleaning (requires sudo)
```bash
sudo python3 pyclean.py -a
```

### List what would be deleted (no deletion)
```bash
python3 pyclean.py -l
```

### Verbose mode (see each file/folder being deleted)
```bash
python3 pyclean.py -v
```

### Dry-run (show what would be deleted, but do not delete)
```bash
python3 pyclean.py -dr
```

### Clean or list a specific folder
```bash
python3 pyclean.py -t ~/Downloads -l
```

---

## 🔎 Modes Explained

- **Normal:**
  - Cleans user cache, temp, trash, thumbnails, and rotated logs.
  - Removes files with no extension in those directories.
  - Does **not** remove active logs or Snap leftovers.

- **Aggressive (`-a`):**
  - Cleans everything from normal mode **plus**:
    - All logs in `/var/log` (except `lastlog`)
    - Snap orphan folders in `~/snap`
  - Automatically requests sudo/root privileges.
  - ⚠️ **Warning:** May remove important system logs. Use with caution!

- **List (`-l`):**
  - Only lists what would be deleted, with size and count, including files with no extension.

- **Verbose (`-v`):**
  - Shows each file/folder being deleted.

- **Dry-run (`-dr`):**
  - Shows what would be deleted, but does not delete anything.

---

## 🧪 Testing

You can generate junk files for testing with the included script:

```bash
python3 gen_junk.py
```
Press `Ctrl+C` to stop. Then run PyClean to see and clean the generated junk.

---

## ⚡️ Make PyClean Globally Executable

Want to run `pyclean` from anywhere? Follow these quick steps:

1. **Make the script executable:**
   ```bash
   chmod +x /path/to/your/PyClean/pyclean.py
   ```
2. **(Optional) Rename for convenience:**
   ```bash
   mv /path/to/your/PyClean/pyclean.py /path/to/your/PyClean/pyclean
   ```
3. **Move to a directory in your $PATH (e.g., /usr/local/bin):**
   ```bash
   sudo mv /path/to/your/PyClean/pyclean /usr/local/bin/pyclean
   ```
4. **Run from anywhere!**
   ```bash
   pyclean -h
   pyclean -l
   sudo pyclean -a
   ```

> **Tip:**
> - Ensure the first line of the script is `#!/usr/bin/env python3`.
> - To update, just replace the file in `/usr/local/bin/`. 


## ⚠️ Legal Disclaimer

> **PyClean is provided solely for educational and maintenance purposes.**
>
> - You are solely responsible for any actions performed with this script and for any consequences that may arise, including but not limited to data loss, system instability, or other damages.
> - The author does not provide any warranty, express or implied, and shall not be held liable for any direct, indirect, incidental, or consequential damages resulting from the use or misuse of this script.
> - It is your duty to ensure you have proper backups and understand the impact of deleting files or directories before proceeding.
> - Use of this script on systems you do not own or without explicit authorization is strictly prohibited and may be illegal.
> - By executing this script, you agree to these terms and assume full responsibility for your actions.
>
> Thank you for using PyClean responsibly.

---

## 👤 Author

- GitHub: [Br3noAraujo](https://github.com/Br3noAraujo)

---

## 📝 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---
