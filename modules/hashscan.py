import os
import re
from datetime import datetime
from typing import Dict, List, Any, Optional

# Common hash format patterns
HASH_PATTERNS = {
    # Linux shadow formats
    r"^\$1\$": {"type": "MD5-Crypt", "platform": "Linux/Unix", "confidence": "High"},
    r"^\$2[aby]\$": {
        "type": "bcrypt",
        "platform": "Linux/Unix/Applications",
        "confidence": "High",
    },
    r"^\$5\$": {
        "type": "SHA-256-Crypt",
        "platform": "Linux/Unix",
        "confidence": "High",
    },
    r"^\$6\$": {
        "type": "SHA-512-Crypt",
        "platform": "Linux/Unix",
        "confidence": "High",
    },
    r"^\$y\$": {"type": "yescrypt", "platform": "Modern Linux", "confidence": "High"},
    r"^\$gy\$": {
        "type": "yescrypt",
        "platform": "Modern Linux",
        "confidence": "Medium",
    },
    # Argon2 (very common in 2025+)
    r"^\$argon2id\$": {
        "type": "Argon2id",
        "platform": "Modern Applications",
        "confidence": "High",
    },
    r"^\$argon2i\$": {
        "type": "Argon2i",
        "platform": "Modern Applications",
        "confidence": "High",
    },
    # PBKDF2
    r"^\$pbkdf2-": {"type": "PBKDF2", "platform": "Applications", "confidence": "High"},
}


def identify_hash_type(hash_value: str) -> Dict[str, str]:
    """
    Identify hash type based on format, prefix, and length.
    Does NOT crack the hash — only classifies it.
    """
    hash_value = hash_value.strip()
    if not hash_value:
        return {
            "hash": hash_value,
            "type": "Unknown",
            "platform": "Unknown",
            "description": "Empty input provided.",
            "confidence": "Low",
        }

    # Check prefix-based patterns first
    for pattern, info in HASH_PATTERNS.items():
        if re.match(pattern, hash_value):
            return {
                "hash": hash_value,
                "type": info["type"],
                "platform": info["platform"],
                "description": f"Standard {info['type']} format.",
                "confidence": info["confidence"],
            }

    # Raw hexadecimal hashes
    if re.fullmatch(r"[A-Fa-f0-9]{32}", hash_value):
        return {
            "hash": hash_value,
            "type": "Possible NTLM / MD5",
            "platform": "Windows or Generic",
            "description": "32 hex chars — commonly NTLM (Windows) or MD5.",
            "confidence": "Medium",
        }

    if re.fullmatch(r"[A-Fa-f0-9]{40}", hash_value):
        return {
            "hash": hash_value,
            "type": "Possible SHA-1",
            "platform": "Generic",
            "description": "40 hex chars — typical SHA-1 format.",
            "confidence": "Medium",
        }

    if re.fullmatch(r"[A-Fa-f0-9]{64}", hash_value):
        return {
            "hash": hash_value,
            "type": "Possible SHA-256",
            "platform": "Generic / Modern",
            "description": "64 hex chars — typical SHA-256 format.",
            "confidence": "Medium",
        }

    if re.fullmatch(r"[A-Fa-f0-9]{128}", hash_value):
        return {
            "hash": hash_value,
            "type": "Possible SHA-512",
            "platform": "Generic",
            "description": "128 hex chars — typical SHA-512 format.",
            "confidence": "Medium",
        }

    # Legacy Windows LM hash pair
    if re.fullmatch(r"[A-Fa-f0-9]{16}:[A-Fa-f0-9]{16}", hash_value):
        return {
            "hash": hash_value,
            "type": "Possible LM Hash Pair",
            "platform": "Legacy Windows",
            "description": "Split LM hash (old Windows format).",
            "confidence": "Low",
        }

    return {
        "hash": hash_value,
        "type": "Unknown",
        "platform": "Unknown",
        "description": "Format not recognized. Could be a custom or rare hash type.",
        "confidence": "Low",
    }


def parse_shadow_line(line: str) -> Optional[Dict[str, Any]]:
    """Parse a Linux /etc/shadow style line."""
    parts = line.strip().split(":")
    if len(parts) < 2:
        return None

    username = parts[0]
    hash_value = parts[1]

    return {
        "entry_type": "Linux Shadow Entry",
        "username": username,
        "hash": hash_value,
        "hash_info": identify_hash_type(hash_value),
    }


def parse_ntlm_line(line: str) -> Optional[Dict[str, Any]]:
    """Parse Windows NTLM / generic hash file lines."""
    line = line.strip()
    if not line:
        return None

    parts = line.split(":")
    if len(parts) == 1:
        hash_value = parts[0]
        return {
            "entry_type": "Generic Hash",
            "username": "(unknown)",
            "hash": hash_value,
            "hash_info": identify_hash_type(hash_value),
        }

    username = parts[0] or "(unknown)"
    # Take the last non-empty field (handles formats like user:::hash)
    hash_value = next((p for p in reversed(parts[1:]) if p), "")

    return {
        "entry_type": "Windows / NTLM Credential Entry",
        "username": username,
        "hash": hash_value,
        "hash_info": identify_hash_type(hash_value),
    }


from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def print_hash_result(result: Dict[str, Any]):
    """Beautiful CLI output for a single hash using rich."""
    info = result["hash_info"]
    confidence_color = "green" if info["confidence"] == "High" else "yellow" if info["confidence"] == "Medium" else "red"
    
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Property", style="bold magenta")
    table.add_column("Value", style="none")
    
    table.add_row("Entry Type", result['entry_type'])
    table.add_row("Username", result['username'])
    table.add_row("Hash", result['hash'])
    table.add_row("Detected Type", f"[bold white]{info['type']}[/bold white]")
    table.add_row("Platform", info['platform'])
    table.add_row("Confidence", f"[bold {confidence_color}]{info['confidence']}[/bold {confidence_color}]")
    table.add_row("Description", f"[dim]{info['description']}[/dim]")

    panel = Panel(
        table,
        title="[bold blue]🔍 HASH ANALYSIS RESULT[/bold blue]",
        border_style="blue",
        expand=False
    )
    console.print()
    console.print(panel)


def analyze_hash_file(filepath: str, parser_type: str) -> List[Dict[str, Any]]:
    """Analyze hashes from a file."""
    if not os.path.exists(filepath):
        console.print(f"[bold red]❌ File not found:[/bold red] {filepath}")
        return []

    results = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            parsed = (
                parse_shadow_line(stripped)
                if parser_type == "shadow"
                else parse_ntlm_line(stripped)
            )
            if parsed:
                results.append(parsed)

    return results


def save_hash_report(
    results: List[Dict], output_file=None
) -> str:
    """Save professional hash analysis report."""
    if output_file is None:
        timestamp = datetime.now().strftime('%a_%H%M%S').lower()
        output_file = f"output/hash_{timestamp}.txt"
        
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("HASH ANALYSIS REPORT - HashScan\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total Hashes Analyzed : {len(results)}\n\n")

        for result in results:
            info = result["hash_info"]
            f.write(f"Entry Type     : {result['entry_type']}\n")
            f.write(f"Username       : {result['username']}\n")
            f.write(f"Hash           : {result['hash']}\n")
            f.write(f"Detected Type  : {info['type']}\n")
            f.write(f"Platform       : {info['platform']}\n")
            f.write(f"Confidence     : {info['confidence']}\n")
            f.write(f"Description    : {info['description']}\n")
            f.write("-" * 80 + "\n\n")

    return output_file


def run_hashscan():
    """Modern and user-friendly CLI entry point."""
    console.print()
    console.print(Panel("[bold magenta]🔍 HashScan - Hash Analyzer[/bold magenta]", border_style="magenta", expand=False, padding=(0, 2)))
    
    console.print("\n[bold magenta]Choose analysis mode:[/bold magenta]")
    console.print("  [magenta]1.[/magenta] Analyze Linux shadow file (sample or custom)")
    console.print("  [magenta]2.[/magenta] Analyze NTLM / Windows hash file (sample or custom)")
    console.print("  [magenta]3.[/magenta] Analyze a single hash manually")

    from modules.nav import ask_choice, ask_string
    choice = ask_choice("\nEnter your choice", choices=["1", "2", "3"])

    if choice in ["b", "q"]:
        return

    elif choice == "3":  # Single hash
        hash_value = ask_string("\n[yellow]Paste the hash value here[/yellow]")
        if hash_value == "__BACK__": return
        if not hash_value:
            console.print("[red]No hash entered.[/red]")
            return

        result = {
            "entry_type": "Manual Single Hash",
            "username": "(unknown)",
            "hash": hash_value,
            "hash_info": identify_hash_type(hash_value),
        }
        print_hash_result(result)

    elif choice in ["1", "2"]:
        parser_type = "shadow" if choice == "1" else "ntlm"
        default_file = (
            "sample_data/target_shadow.txt"
            if choice == "1"
            else "sample_data/target_ntlm.txt"
        )

        filepath = ask_string("Enter full path to your hash file", default=default_file)
        if filepath == "__BACK__": return

        console.print(f"\n📄 [bold magenta]Analyzing file:[/bold magenta] {filepath}")
        results = analyze_hash_file(filepath, parser_type)

        if not results:
            console.print("[bold yellow]No valid hash entries found in the file.[/bold yellow]")
            return

        console.print(f"[bold green]✅ Found {len(results)} hash entries.[/bold green]\n")

        for result in results:
            print_hash_result(result)

        saved_file = save_hash_report(results)
        console.print(f"\n[bold green]📄 Full report saved to:[/bold green] {saved_file}")
