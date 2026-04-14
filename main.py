from modules.dictionary_generator import run_dictionary_generator
from modules.strength_analyzer import run_strength_analyzer
from modules.brute_force_simulator import run_brute_force_simulator
from modules.hash_parser import run_hash_parser
from modules.report_generator import run_report_generator


def print_menu():
    print("\n" + "=" * 50)
    print(" PASSWORD AUDIT SUITE ".center(50, "="))
    print("=" * 50)
    print("1. Generate Dictionary")
    print("2. Analyze Password Strength")
    print("3. Simulate Brute Force")
    print("4. Parse Sample Hashes")
    print("5. Generate Audit Report")
    print("6. Exit")
    print("=" * 50)


def main():
    while True:
        print_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            run_dictionary_generator()
        elif choice == "2":
            run_strength_analyzer()
        elif choice == "3":
            run_brute_force_simulator()
        elif choice == "4":
            run_hash_parser()
        elif choice == "5":
            run_report_generator()
        elif choice == "6":
            print("Exiting Password Audit Suite. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()