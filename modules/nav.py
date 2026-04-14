import sys
import tty
import termios
from rich.console import Console

console = Console()

def getch():
    """Reads a single character from standard input instantly."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            import select
            if select.select([sys.stdin], [], [], 0.01)[0]:
                ch += sys.stdin.read(2)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def ask_choice(prompt: str, choices: list) -> str:
    """Prompt for a single character instantly."""
    choices_str = "/".join(choices + ["b", "q"])
    console.print(f"[bold yellow]{prompt}[/bold yellow] [[cyan]{choices_str}[/cyan]]: ", end="")
    
    while True:
        ch = getch()
        ch_lower = ch.lower() if len(ch) == 1 else ch
        
        # Intercept shortcuts
        if ch == '\x1b' or ch_lower == 'q' or ch_lower == '\x03':
            print()
            return 'q'
        if ch_lower == 'b':
            print()
            return 'b'
            
        if ch in choices:
            print(ch)
            return ch

def ask_string(prompt: str, default: str = "") -> str:
    """Read full string with support for ESC to instantly abort."""
    if default:
        console.print(f"[bold yellow]{prompt}[/bold yellow] ([dim]{default}[/dim]) [dim][ESC][/dim]: ", end="")
    else:
        console.print(f"[bold yellow]{prompt}[/bold yellow] [dim][ESC][/dim]: ", end="")
        
    buffer = ""
    while True:
        ch = getch()
        
        if ch == '\x1b' or ch == '\x03': # ESC or Ctrl+C
            print()
            return "__BACK__"
            
        if ch == '\r' or ch == '\n':
            print()
            return buffer.strip() if buffer.strip() else default
            
        # Backspace
        if ch == '\x7f' or ch == '\b':
            if len(buffer) > 0:
                buffer = buffer[:-1]
                sys.stdout.write("\b \b")
                sys.stdout.flush()
            continue
            
        # Ignore other escape sequences
        if ch.startswith('\x1b'):
            continue
            
        sys.stdout.write(ch)
        sys.stdout.flush()
        buffer += ch
