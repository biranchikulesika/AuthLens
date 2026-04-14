import os
from datetime import datetime

# Imports from our improved modules
from modules.strength_analyzer import (
    load_dictionary_words,
    analyze_password_file,      # ← This is now available after adding the function above
)
from modules.hash_parser import analyze_hash_file


def summarize_password_results(results):
    """Clean summary for passwords."""
    if not results:
        return None

    summary = {
        "total": len(results),
        "weak": sum(1 for r in results if r["strength"] in ["Very Weak", "Weak"]),
        "moderate": sum(1 for r in results if r["strength"] == "Moderate"),
        "strong": sum(1 for r in results if r["strength"] in ["Strong", "Very Strong"]),
        "common": sum(1 for r in results if r["findings"]["is_common_password"]),
        "dictionary": sum(1 for r in results if r["findings"]["contains_dictionary_word"]),
        "predictable": sum(1 for r in results if r["findings"]["has_keyboard_pattern"] or
                          r["findings"]["has_sequential_pattern"] or
                          r["findings"]["has_repeated_characters"]),
    }
    return summary


def summarize_hash_results(results):
    """Clean summary for hashes."""
    if not results:
        return None

    summary = {
        "total": len(results),
        "linux_unix": sum(1 for r in results if "Linux" in r["hash_info"]["platform"] or "Unix" in r["hash_info"]["platform"]),
        "windows_generic": sum(1 for r in results if "Windows" in r["hash_info"]["platform"] or "Generic" in r["hash_info"]["platform"]),
        "unknown": sum(1 for r in results if r["hash_info"]["type"] == "Unknown"),
    }
    return summary


def build_final_report(password_results, hash_results):
    """Minimalistic, clean and easy-to-read final report."""
    pw = summarize_password_results(password_results)
    hs = summarize_hash_results(hash_results)

    report = []
    report.append("=" * 85)
    report.append("🔐 AUTH LENS - FINAL SECURITY AUDIT REPORT")
    report.append("=" * 85)
    report.append(f"Generated on : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")

    report.append("EXECUTIVE SUMMARY")
    report.append("-" * 85)
    report.append("This report combines password strength analysis and hash format detection")
    report.append("to demonstrate authentication security risks.\n")

    # Password Summary
    report.append("1. PASSWORD STRENGTH SUMMARY")
    report.append("-" * 85)
    if pw:
        report.append(f"Total passwords analyzed      : {pw['total']}")
        report.append(f"Weak / Very Weak              : {pw['weak']}")
        report.append(f"Moderate                      : {pw['moderate']}")
        report.append(f"Strong / Very Strong          : {pw['strong']}")
        report.append(f"Common or dictionary-based    : {pw['common'] + pw['dictionary']}")
        report.append(f"Predictable patterns          : {pw['predictable']}")
    else:
        report.append("No password data available.")
    report.append("")

    # Hash Summary
    report.append("2. HASH ANALYSIS SUMMARY")
    report.append("-" * 85)
    if hs:
        report.append(f"Total hashes analyzed         : {hs['total']}")
        report.append(f"Linux/Unix hashes             : {hs['linux_unix']}")
        report.append(f"Windows/Generic hashes        : {hs['windows_generic']}")
        report.append(f"Unknown formats               : {hs['unknown']}")
    else:
        report.append("No hash data available.")
    report.append("")

    # Recommendations
    report.append("3. KEY RECOMMENDATIONS")
    report.append("-" * 85)
    report.append("• Enforce 12–16+ character passwords")
    report.append("• Block common and dictionary-based passwords")
    report.append("• Reject keyboard walks, sequences, and repeated characters")
    report.append("• Use modern hashing (bcrypt, Argon2, SHA-512-Crypt)")
    report.append("• Enable Multi-Factor Authentication (MFA)")
    report.append("• Promote password managers")
    report.append("")

    report.append("4. CONCLUSION")
    report.append("-" * 85)
    report.append("Weak passwords and legacy hash storage are high-risk areas.")
    report.append("Strong policies and modern practices significantly reduce risk.")
    report.append("")
    report.append("Thank you for using Auth Lens.")
    report.append("=" * 85)

    return "\n".join(report)


def save_final_report(report_text: str, output_file="output/final_audit_report.txt"):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report_text)


def run_report_generator():
    """User-friendly final report generation."""
    print("\n📋 Auth Lens - Final Audit Report Generator")
    print("=" * 65)
    print("Generating final security audit report...\n")

    dictionary_words = load_dictionary_words()

    password_results = analyze_password_file("sample_data/sample_passwords.txt", dictionary_words)
    linux_hashes = analyze_hash_file("sample_data/sample_linux_shadow.txt", "shadow")
    ntlm_hashes = analyze_hash_file("sample_data/sample_ntlm_hashes.txt", "ntlm")
    hash_results = linux_hashes + ntlm_hashes

    report_text = build_final_report(password_results, hash_results)
    save_final_report(report_text)

    print("✅ Final audit report generated successfully!")
    print(f"📄 Saved to : output/final_audit_report.txt\n")

    # Show short preview
    print("Preview:")
    print("-" * 40)
    for line in report_text.splitlines()[:12]:
        print(line)
    print("-" * 40)