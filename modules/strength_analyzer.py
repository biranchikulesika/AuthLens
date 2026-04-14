import math
import os
import re
from datetime import datetime
from typing import Dict, List, Any

# Common weak passwords
COMMON_PASSWORDS = {
    "password",
    "password123",
    "admin",
    "admin123",
    "welcome",
    "welcome123",
    "qwerty",
    "qwerty123",
    "letmein",
    "login",
    "user",
    "guest",
    "test",
    "test123",
    "root",
    "root123",
    "india123",
    "abc123",
    "123456",
    "12345678",
    "123456789",
    "111111",
    "000000",
    "iloveyou",
    "monkey",
    "sunshine",
    "princess",
    "1234567890",
}

KEYBOARD_PATTERNS = [
    "qwerty",
    "asdf",
    "zxcv",
    "qaz",
    "wsx",
    "edc",
    "1234",
    "12345",
    "123456",
]

SEQUENTIAL_STRINGS = [
    "abcdefghijklmnopqrstuvwxyz",
    "0123456789",
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm",
]


def load_dictionary_words(filepath="sample_data/common_words.txt") -> set:
    """Load common weak words from file."""
    if not os.path.exists(filepath):
        return set()

    words = set()
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            word = line.strip().lower()
            if word and len(word) >= 3:
                words.add(word)
    return words


def get_character_pool_size(password: str) -> int:
    """Calculate effective character pool size."""
    pool = 0
    if re.search(r"[a-z]", password):
        pool += 26
    if re.search(r"[A-Z]", password):
        pool += 26
    if re.search(r"[0-9]", password):
        pool += 10
    if re.search(r"[^a-zA-Z0-9]", password):
        pool += 32  # Common symbols
    return max(pool, 1)


def estimate_entropy(password: str) -> float:
    """Improved entropy calculation."""
    if not password:
        return 0.0

    length = len(password)
    pool = get_character_pool_size(password)

    # Base entropy
    entropy = length * math.log2(pool)

    # Penalty for patterns
    if has_repeated_characters(password):
        entropy *= 0.7
    if has_sequential_pattern(password):
        entropy *= 0.6
    if has_keyboard_pattern(password):
        entropy *= 0.65

    return round(entropy, 2)


def estimate_crack_time(entropy: float) -> str:
    """Estimate time to crack assuming 10 billion guesses per second (modern GPU)."""
    if entropy < 1:
        return "Instant"

    guesses_per_second = 10_000_000_000  # 10 billion
    seconds = 2**entropy / guesses_per_second

    if seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.1f} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.1f} hours"
    elif seconds < 31536000:
        return f"{seconds/86400:.1f} days"
    else:
        years = seconds / 31536000
        if years > 1000:
            return "Thousands of years"
        return f"{years:.1f} years"


def has_repeated_characters(password: str, threshold: int = 3) -> bool:
    """Detect runs of same character."""
    pattern = r"(.)\1{" + str(threshold - 1) + r",}"
    return re.search(pattern, password) is not None


def has_sequential_pattern(password: str, min_len: int = 4) -> bool:
    """Detect sequential patterns."""
    lower_pw = password.lower()
    for i in range(len(lower_pw) - min_len + 1):
        sub = lower_pw[i : i + min_len]
        for seq in SEQUENTIAL_STRINGS:
            if sub in seq:
                return True
    return False


def has_keyboard_pattern(password: str) -> bool:
    """Detect keyboard walk patterns."""
    lower_pw = password.lower()
    return any(pattern in lower_pw for pattern in KEYBOARD_PATTERNS)


def is_common_password(password: str, dictionary_words: set) -> bool:
    lower_pw = password.lower()
    return lower_pw in COMMON_PASSWORDS or lower_pw in dictionary_words


def contains_dictionary_word(password: str, dictionary_words: set) -> bool:
    """Check if password contains dictionary words as substring."""
    lower_pw = password.lower()
    for word in dictionary_words.union(COMMON_PASSWORDS):
        if len(word) >= 4 and word in lower_pw:
            return True
    return False


def analyze_composition(password: str) -> Dict[str, Any]:
    """Analyze character composition."""
    return {
        "length": len(password),
        "has_lowercase": bool(re.search(r"[a-z]", password)),
        "has_uppercase": bool(re.search(r"[A-Z]", password)),
        "has_digits": bool(re.search(r"[0-9]", password)),
        "has_symbols": bool(re.search(r"[^a-zA-Z0-9]", password)),
    }


def score_password(password: str, dictionary_words: set) -> int:
    """Improved scoring (0-10)."""
    if not password:
        return 0

    composition = analyze_composition(password)
    entropy = estimate_entropy(password)
    score = 0

    # Positive factors
    if composition["length"] >= 8:
        score += 1
    if composition["length"] >= 12:
        score += 2
    if composition["length"] >= 16:
        score += 2

    if composition["has_lowercase"]:
        score += 1
    if composition["has_uppercase"]:
        score += 1
    if composition["has_digits"]:
        score += 1
    if composition["has_symbols"]:
        score += 1

    if entropy >= 50:
        score += 1
    if entropy >= 70:
        score += 1

    # Negative factors
    if is_common_password(password, dictionary_words):
        score -= 5
    if contains_dictionary_word(password, dictionary_words):
        score -= 3
    if has_keyboard_pattern(password):
        score -= 3
    if has_repeated_characters(password):
        score -= 2
    if has_sequential_pattern(password):
        score -= 2

    return max(0, min(10, score))


def classify_score(score: int) -> str:
    if score <= 3:
        return "Very Weak"
    if score <= 5:
        return "Weak"
    if score <= 7:
        return "Moderate"
    if score <= 9:
        return "Strong"
    return "Very Strong"


def generate_recommendations(
    password: str, composition: dict, dictionary_words: set
) -> List[str]:
    """Generate prioritized recommendations."""
    suggestions = []

    if len(password) < 12:
        suggestions.append("❌ Increase length to at least 12-16 characters")
    elif len(password) < 16:
        suggestions.append(
            "⚠️  Consider making password longer (16+ characters recommended)"
        )

    if not composition["has_lowercase"]:
        suggestions.append("❌ Add lowercase letters")
    if not composition["has_uppercase"]:
        suggestions.append("❌ Add uppercase letters")
    if not composition["has_digits"]:
        suggestions.append("❌ Add numbers")
    if not composition["has_symbols"]:
        suggestions.append("❌ Add special characters (!@#$%^&*)")

    if is_common_password(password, dictionary_words):
        suggestions.append("❌ This is a very common password - change it immediately")
    if contains_dictionary_word(password, dictionary_words):
        suggestions.append("❌ Avoid using dictionary words or names in password")
    if has_keyboard_pattern(password):
        suggestions.append("❌ Avoid keyboard patterns (qwerty, asdf, etc.)")
    if has_repeated_characters(password):
        suggestions.append("❌ Avoid repeated characters (aaa, 1111)")
    if has_sequential_pattern(password):
        suggestions.append("❌ Avoid sequential patterns (1234, abcd)")

    if not suggestions:
        suggestions.append(
            "✅ Excellent password composition! Use a password manager for best security."
        )

    return suggestions


def analyze_password(password: str, dictionary_words: set) -> Dict[str, Any]:
    """Main analysis function."""
    composition = analyze_composition(password)
    entropy = estimate_entropy(password)
    score = score_password(password, dictionary_words)
    strength = classify_score(score)
    crack_time = estimate_crack_time(entropy)
    recommendations = generate_recommendations(password, composition, dictionary_words)

    findings = {
        "is_common_password": is_common_password(password, dictionary_words),
        "contains_dictionary_word": contains_dictionary_word(
            password, dictionary_words
        ),
        "has_keyboard_pattern": has_keyboard_pattern(password),
        "has_repeated_characters": has_repeated_characters(password),
        "has_sequential_pattern": has_sequential_pattern(password),
    }

    return {
        "password": password,
        "masked_password": (
            password[:2] + "*" * (len(password) - 4) + password[-2:]
            if len(password) > 4
            else password
        ),
        "length": composition["length"],
        "has_lowercase": composition["has_lowercase"],
        "has_uppercase": composition["has_uppercase"],
        "has_digits": composition["has_digits"],
        "has_symbols": composition["has_symbols"],
        "entropy": entropy,
        "score": score,
        "strength": strength,
        "estimated_crack_time": crack_time,
        "findings": findings,
        "recommendations": recommendations,
    }


def print_analysis(result: Dict[str, Any]):
    """Beautiful CLI output."""
    print("\n" + "=" * 70)
    print("🔐 PASSWORD STRENGTH ANALYSIS")
    print("=" * 70)
    print(f"Password           : {result['masked_password']}")
    print(f"Length             : {result['length']} characters")
    print(f"Entropy            : {result['entropy']} bits")
    print(f"Estimated Crack Time : {result['estimated_crack_time']}")
    print(f"Score              : {result['score']}/10")
    print(f"Strength           : {result['strength']}")

    print("\n📊 Composition:")
    comp = result
    print(f"   Lowercase     : {'✅' if comp['has_lowercase'] else '❌'}")
    print(f"   Uppercase     : {'✅' if comp['has_uppercase'] else '❌'}")
    print(f"   Digits        : {'✅' if comp['has_digits'] else '❌'}")
    print(f"   Symbols       : {'✅' if comp['has_symbols'] else '❌'}")

    print("\n⚠️  Weakness Findings:")
    for key, value in result["findings"].items():
        if value:
            print(f"   • {key.replace('_', ' ').title()}")

    print("\n💡 Recommendations:")
    for i, rec in enumerate(result["recommendations"], 1):
        print(f"   {i}. {rec}")
    print("=" * 70)


def save_analysis_report(
    results: List[Dict], output_file="output/password_analysis_report.txt"
):
    """Save detailed report."""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("PASSWORD STRENGTH ANALYSIS REPORT\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")

        for result in results:
            f.write(f"Password           : {result['masked_password']}\n")
            f.write(f"Length             : {result['length']}\n")
            f.write(f"Entropy            : {result['entropy']} bits\n")
            f.write(f"Est. Crack Time    : {result['estimated_crack_time']}\n")
            f.write(
                f"Score              : {result['score']}/10 ({result['strength']})\n\n"
            )

            f.write("Composition:\n")
            f.write(f"  Lowercase: {result['has_lowercase']}\n")
            f.write(f"  Uppercase: {result['has_uppercase']}\n")
            f.write(f"  Digits   : {result['has_digits']}\n")
            f.write(f"  Symbols  : {result['has_symbols']}\n\n")

            f.write("Weakness Findings:\n")
            for key, value in result["findings"].items():
                if value:
                    f.write(f"  • {key.replace('_', ' ').title()}\n")

            f.write("\nRecommendations:\n")
            for i, rec in enumerate(result["recommendations"], 1):
                f.write(f"  {i}. {rec}\n")
            f.write("\n" + "-" * 80 + "\n\n")


def analyze_password_file(filepath: str, dictionary_words: set) -> list:
    """
    Analyze all passwords from a file (one password per line).
    Used by the Final Report Generator.
    """
    if not os.path.exists(filepath):
        return []

    results = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            password = line.strip()
            if password:
                results.append(analyze_password(password, dictionary_words))
    return results


def run_strength_analyzer():
    """Improved user-friendly CLI."""
    dictionary_words = load_dictionary_words()

    print("\n🔐 Auth Lens - Password Strength Analyzer")
    print("=" * 55)
    print("1. Analyze a single password")
    print("2. Analyze passwords from file (sample_data/sample_passwords.txt)")
    print("3. Back to main menu")

    choice = input("\nEnter your choice (1-3): ").strip()

    if choice == "1":
        password = input("\nEnter password to analyze: ").strip()
        if not password:
            print("No password entered.")
            return

        result = analyze_password(password, dictionary_words)
        print_analysis(result)

    elif choice == "2":
        filepath = "sample_data/sample_passwords.txt"
        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            print("Please create the file with one password per line.")
            return

        print(f"\nAnalyzing passwords from {filepath}...")
        results = []

        with open(filepath, "r", encoding="utf-8") as f:
            passwords = [line.strip() for line in f if line.strip()]

        for i, pw in enumerate(passwords, 1):
            print(f"  Analyzing {i}/{len(passwords)}...", end="\r")
            results.append(analyze_password(pw, dictionary_words))

        print(f"\n✅ Analyzed {len(results)} passwords successfully!")

        for result in results:
            print_analysis(result)

        save_analysis_report(results)
        print(f"\n📄 Full report saved to: output/password_analysis_report.txt")

    elif choice == "3":
        return
    else:
        print("Invalid choice.")
