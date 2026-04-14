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


def load_dictionary_words(filepath="sample_data/wordlist_common.txt") -> set:
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


from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def print_analysis(result: Dict[str, Any]):
    """Beautiful CLI output using rich."""
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Property", style="bold blue")
    table.add_column("Value", style="none")
    
    table.add_row("Password", result['password'])
    table.add_row("Length", f"{result['length']} characters")
    table.add_row("Entropy", f"{result['entropy']} bits")
    table.add_row("Est. Crack Time", result['estimated_crack_time'])
    table.add_row("Score", f"{result['score']}/10")
    
    strength_color = "red"
    if result["score"] >= 8:
        strength_color = "green"
    elif result["score"] >= 6:
        strength_color = "yellow"
    table.add_row("Strength", f"[bold {strength_color}]{result['strength']}[/bold {strength_color}]")

    comp = result
    comp_text = (
        f"   Lowercase     : {'✅' if comp['has_lowercase'] else '❌'}\n"
        f"   Uppercase     : {'✅' if comp['has_uppercase'] else '❌'}\n"
        f"   Digits        : {'✅' if comp['has_digits'] else '❌'}\n"
        f"   Symbols       : {'✅' if comp['has_symbols'] else '❌'}"
    )

    weakness_text = ""
    for key, value in result["findings"].items():
        if value:
            weakness_text += f"   • {key.replace('_', ' ').title()}\n"
    if not weakness_text:
        weakness_text = "   [dim]None[/dim]\n"

    rec_text = ""
    for i, rec in enumerate(result["recommendations"], 1):
        rec_text += f"   {i}. {rec}\n"

    from rich.console import Group
    content = Group(
        table,
        "\n[bold magenta]📊 Composition:[/bold magenta]",
        comp_text,
        "\n[bold yellow]⚠️  Weakness Findings:[/bold yellow]",
        weakness_text,
        "[bold green]💡 Recommendations:[/bold green]",
        rec_text.strip()
    )

    panel = Panel(
        content,
        title="[bold green]🔐 PASSWORD STRENGTH ANALYSIS[/bold green]",
        border_style="green",
        expand=False
    )
    console.print()
    console.print(panel)


def save_analysis_report(
    results: List[Dict], output_file=None
) -> str:
    """Save detailed report."""
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"output/strengthmeter_report_{timestamp}.txt"
        
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("PASSWORD STRENGTH ANALYSIS REPORT\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")

        weak = sum(1 for r in results if r["score"] <= 5)
        strong = sum(1 for r in results if r["score"] >= 8)
        moderate = len(results) - weak - strong
        f.write("SUMMARY\n")
        f.write("-" * 80 + "\n")
        f.write(f"Total Passwords    : {len(results)}\n")
        f.write(f"Weak/Very Weak     : {weak}\n")
        f.write(f"Moderate           : {moderate}\n")
        f.write(f"Strong/Very Strong : {strong}\n")
        f.write("=" * 80 + "\n\n")

        for result in results:
            f.write(f"Password           : {result['password']}\n")
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

    return output_file


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


def run_strengthmeter():
    """Improved user-friendly CLI."""
    dictionary_words = load_dictionary_words()

    console.print()
    console.print(Panel("[bold blue]🔐 StrengthMeter - Password Analyzer[/bold blue]", border_style="blue", expand=False, padding=(0, 2)))
    
    console.print("  [blue]1.[/blue] Analyze a single password")
    console.print("  [blue]2.[/blue] Analyze passwords from file (sample or custom)")

    from modules.nav import ask_choice, ask_string
    choice = ask_choice("\nEnter your choice", choices=["1", "2"])

    if choice in ["b", "q"]:
        return

    if choice == "1":
        password = ask_string("\n[bold yellow]Enter password to analyze[/bold yellow]")
        if password == "__BACK__": return
        if not password:
            console.print("[red]No password entered.[/red]")
            return

        result = analyze_password(password, dictionary_words)
        print_analysis(result)

    elif choice == "2":
        default_file = "sample_data/target_passwords.txt"
        filepath = ask_string("Enter full path to your password file", default=default_file)
        if filepath == "__BACK__": return

        if not os.path.exists(filepath):
            console.print(f"[red]❌ File not found:[/red] {filepath}")
            console.print("Please create the file with one password per line.")
            return

        console.print(f"\n[blue]Analyzing passwords from {filepath}...[/blue]")
        results = []

        with open(filepath, "r", encoding="utf-8") as f:
            passwords = [line.strip() for line in f if line.strip()]

        from rich.progress import track
        for pw in track(passwords, description="Analyzing..."):
            results.append(analyze_password(pw, dictionary_words))

        console.print(f"\n[bold green]✅ Analyzed {len(results)} passwords successfully![/bold green]")

        weak = sum(1 for r in results if r["score"] <= 5)
        strong = sum(1 for r in results if r["score"] >= 8)
        moderate = len(results) - weak - strong
        
        console.print(f"  • [red]Weak / Very Weak:[/red]   {weak}")
        console.print(f"  • [yellow]Moderate:[/yellow]           {moderate}")
        console.print(f"  • [green]Strong / Very Strong:[/green] {strong}")

        saved_file = save_analysis_report(results)
        console.print(f"\n[bold green]📄 Full report saved to:[/bold green] {saved_file}")

    elif choice == "3":
        return
