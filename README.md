# 🔐 AuthLens

**AuthLens** is a modern, modular, and professional security audit suite designed to analyze, test, and educate on authentication vulnerabilities. AuthLens brings a cohesive, fully-featured toolkit directly to your terminal, complete with non-blocking instant navigation, rich color-coding, and comprehensive reporting.

Whether you're compiling custom wordlists, identifying unknown hashes, assessing password entropy, or generating final high-level executive security audits—AuthLens has you covered.

---

## 🚀 Features

AuthLens features an elegant, zero-friction Terminal Interface powered by [`rich`](https://github.com/Textualize/rich). It includes a professional startup banner, intelligent configuration loading (`config.json`), built-in documentation via About/Help screens, and instantaneous keystroke-based navigation (`b` to go back, `q`/`ESC` to quit) so you never get slowed down.

1. **📖 PassForge (Dictionary Generator)**
   * Generate extensive, highly targeted wordlists and passwords instantly.
   * Input names, phone numbers, birthdates, and custom keywords to automatically produce human-predictable combinations, suffix expansions, and gamer/slang variants.

2. **🔐 StrengthMeter (Password Analyzer)**
   * Not just a basic score script! StrengthMeter checks for keyboard walks (e.g., `qwerty`), repetition (`aaa`), sequential patterns, and known dictionary words.
   * Calculates real entropy and provides actionable, prioritized recommendations.
   * Can evaluate massive dumps of passwords and bulk-export results.

3. **🔥 BruteCheck (Brute Force Simulator)**
   * Demonstrates the real-world search space for a given password length and character pool.
   * Compares estimated crack times across realistic cracking rigs (from a basic CPU to a 10 billion guesses/sec Cloud GPU Cluster).

4. **🔍 HashScan (Hash Parser / Analyzer)**
   * Analyzes complex authentication hashes without cracking them.
   * Automatically identifies hash architectures such as Linux Shadow formats (`$6$` SHA-512, `$y$` yescrypt), modern web applications (Argon2, PBKDF2), and legacy Windows systems (NTLM/LM pairs).

5. **📋 Auditor (Security Audit Report)**
   * Combines input from simulated target populations (password and hash lists).
   * Automatically generates a beautiful, executive-ready security audit report highlighting systemic weaknesses and key security recommendations.

## 🛠️ Installation

Requires **Python 3.8+**. 

1. **Clone the repository:**
   ```bash
   git clone https://github.com/biranchikulesika/AuthLens.git
   cd AuthLens
   ```

2. **Install the dependencies:**
   AuthLens strictly utilizes the standard library and `rich` for its beautiful interface.
   ```bash
   pip install rich
   ```

## 🎮 Usage

Launch the primary interactive menu:

```bash
python3 main.py
```

### Navigation Keys
- **1-7**: Select modules / choices (including About and Help screens) immediately.
- **b**: Instantly go back to the previous menu.
- **q** or **ESC**: Quit the application from anywhere.

### Output Files
When reports or wordlists are generated, AuthLens automatically formats and saves them gracefully to the `output/` directory with clean, short timestamp tags (e.g., `audit_tue_151027.txt` and `hash_tue_151027.txt`) for simple reference and retrieval.

---

## 📁 Project Structure

```text
AuthLens/
│── main.py                 # Core application entry point
│── README.md               # Documentation
│── modules/                # Application modules
│   ├── about.py            # Professional UI Headers & Help Screens
│   ├── auditor.py          # Report Aggregator
│   ├── brutecheck.py       # Simulation Tool 
│   ├── config.py           # Configuration Management & Versioning
│   ├── hashscan.py         # Hash Identifier
│   ├── nav.py              # Instant Non-Blocking Keyboard UI Routing
│   ├── passforge.py        # Custom Wordlist Generator
│   └── strengthmeter.py    # Entropy & Strength Evaluation
│── sample_data/            # Sample test sets for auditing
│   ├── target_ntlm.txt     # Windows Sample Hashes
│   ├── target_passwords.txt# User Paswords
│   ├── target_shadow.txt   # Linux Sample Hashes
│   └── wordlist_common.txt # Default known-weak word dictionary
└── output/                 # Automatically generated logs & reports
```

## 🤝 Contributing
Contributions are well appreciated! If you have a suggestion that would make this better, please fork the repo and create a pull request or open an issue.

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.