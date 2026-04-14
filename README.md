# 🔐 AuthLens

**AuthLens** is a modular cybersecurity audit tool designed to analyze authentication weaknesses, simulate attacks, and generate security reports.

AuthLens runs in your terminal and provides a simple and clean interface with color output, fast navigation, and structured reports.

You can use AuthLens to:

* Generate custom password wordlists
* Analyze password strength
* Simulate brute force attacks
* Identify hash formats
* Generate final security audit reports

---

# 🚀 Features

AuthLens includes a clean terminal interface powered by **rich** with:

* Simple startup screen
* Fast navigation
* Configurable settings using `config.json`
* Modular architecture
* Automatic report generation

---

## 📖 PassForge (Dictionary Generator)

Generate targeted password wordlists using:

* Names
* Phone numbers
* Dates of birth
* Custom keywords

PassForge creates realistic password combinations including:

* Common suffixes
* Human patterns
* Gamer style passwords

This is useful for:

* Security testing
* Password policy checks
* Security awareness

---

## 🔐 StrengthMeter (Password Analyzer)

Analyze password strength using:

* Entropy calculation
* Dictionary detection
* Keyboard pattern detection
* Sequential pattern detection
* Repeated character detection
* Character composition analysis

Features:

* Analyze single password
* Analyze password file
* Export detailed report

---

## 🔥 BruteCheck (Brute Force Simulator)

Simulate brute force attacks using:

* Password length
* Character sets
* Realistic cracking speeds

Output includes:

* Search space
* Estimated crack time
* Risk level

---

## 🔍 HashScan (Hash Analyzer)

Identify hash formats including:

* Linux shadow hashes
* bcrypt
* yescrypt
* Argon2
* PBKDF2
* NTLM
* SHA256 / SHA512

AuthLens does not crack hashes. It only identifies them for security auditing.

---

## 📋 Auditor (Security Audit Report)

Generate final security reports using:

* Password files
* Linux shadow files
* Windows hash files

The Auditor generates:

* Summary of weaknesses
* Risk assessment
* Security recommendations

---

# ⚙️ Configuration

AuthLens uses `config.json`:

```json
{
  "output_directory": "output",
  "default_brute_speed": "fast",
  "show_banner": true
}
```

You can change:

* Output directory
* Default settings
* UI behavior

---

# 🛠️ Installation

Requires Python 3.8+

Clone repository:

```bash
git clone https://github.com/biranchikulesika/AuthLens.git
cd AuthLens
```

Install dependencies:

```bash
pip install rich
```

---

# 🎮 Usage

Run:

```bash
python main.py
```

---

## Navigation Keys

| Key | Action         |
| --- | -------------- |
| 1-7 | Select modules |
| b   | Go back        |
| q   | Quit           |
| ESC | Quit           |

---

# 📁 Project Structure

```
AuthLens/
│── main.py
│── README.md
│── config.json
│── modules/
│   ├── about.py
│   ├── auditor.py
│   ├── brutecheck.py
│   ├── config.py
│   ├── hashscan.py
│   ├── nav.py
│   ├── passforge.py
│   └── strengthmeter.py
│── sample_data/
│   ├── target_ntlm.txt
│   ├── target_passwords.txt
│   ├── target_shadow.txt
│   └── wordlist_common.txt
└── output/
```

---

# 📄 Output Files

AuthLens automatically saves files in the `output` folder.

Example:

```
output/
dict_mon_142010.txt
strength_mon_142015.txt
brute_mon_142020.txt
hash_mon_142025.txt
audit_mon_142030.txt
```

---

# 🎯 Use Cases

* Cybersecurity internships
* Security auditing
* Password testing
* Security awareness
* Learning cybersecurity concepts

---

# 🤝 Contributing

Contributions are welcome.

Steps:

1. Fork repository
2. Create branch
3. Submit pull request
