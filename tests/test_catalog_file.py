from pathlib import Path

CATALOG_PATH = Path("knowledge_base/aether_catalog.txt")


def main():
    # Check if file exists
    if not CATALOG_PATH.exists():
        print("ERROR: Catalog file not found.")
        return

    print("Catalog file found.")

    # Read file
    content = CATALOG_PATH.read_text(encoding="utf-8")

    # Count book entries
    book_count = content.count("BOOK ENTRY")
    print(f"Book entries found: {book_count}")

    # Count policy sections
    policy_count = content.count("Policy Name:")
    print(f"Policy sections found: {policy_count}")

    # Validation
    errors = []

    if book_count < 5:
        errors.append("Minimum 5 book entries required.")

    if policy_count < 4:
        errors.append("Minimum 4 policy sections required.")

    if errors:
        print("\nValidation failed:")
        for error in errors:
            print(f"- {error}")
    else:
        print("\nKnowledge base validation successful.")


if __name__ == "__main__":
    main()