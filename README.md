# Password Audit Suite

## Overview

Password Audit Suite is a Python-based cybersecurity project designed to analyze password security in a controlled and ethical environment. The project demonstrates how weak password patterns can be identified, how password strength can be evaluated, how brute-force difficulty can be estimated, and how credential hash formats can be classified.

This project is intended for educational use, security awareness, defensive auditing, and internship demonstration purposes.

---

## Features

### 1. Dictionary Generator
Generates password candidates using:
- user-provided seed words
- capitalization variations
- leetspeak substitutions
- common suffixes
- token combinations

Output file:
- `output/generated_dictionary.txt`

---

### 2. Password Strength Analyzer
Evaluates passwords based on:
- length
- lowercase usage
- uppercase usage
- digit usage
- symbol usage
- entropy estimation
- dictionary-word detection
- keyboard patterns
- repeated characters
- sequential patterns

Output file:
- `output/password_analysis_report.txt`

---

### 3. Brute-Force Simulator
Estimates the difficulty of brute-forcing passwords based on:
- password length
- character set size
- attacker guesses per second

It provides:
- total search space
- best-case crack time
- average-case crack time
- worst-case crack time
- practical risk level

Output file:
- `output/brute_force_report.txt`

---

### 4. Hash Parser
Classifies sample hash entries based on structure and known format patterns.

Supported identification types include:
- MD5-Crypt
- SHA-256-Crypt
- SHA-512-Crypt
- bcrypt
- yescrypt
- possible NTLM / MD5
- possible SHA-1
- possible SHA-256
- possible SHA-512

Output file:
- `output/hash_analysis_report.txt`

---

### 5. Final Report Generator
Combines password analysis and hash analysis into one final audit report.

Output file:
- `output/final_audit_report.txt`

---

## Project Structure

```text
password_audit_suite/
│
├── main.py
├── README.md
├── requirements.txt
│
├── modules/
│   ├── __init__.py
│   ├── dictionary_generator.py
│   ├── strength_analyzer.py
│   ├── brute_force_simulator.py
│   ├── hash_parser.py
│   └── report_generator.py
│
├── sample_data/
│   ├── common_words.txt
│   ├── sample_passwords.txt
│   ├── sample_linux_shadow.txt
│   └── sample_ntlm_hashes.txt
│
├── output/
│   ├── generated_dictionary.txt
│   ├── password_analysis_report.txt
│   ├── brute_force_report.txt
│   ├── hash_analysis_report.txt
│   └── final_audit_report.txt
│
└── report/