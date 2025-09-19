from datetime import datetime, timedelta
from pathlib import Path

def get_user_confirmation_with_record(
        trust_file: str,
        warning_msg: str,
        max_age_days: int = 7
) -> bool:
    """
    Checks with user for confirmation. Stores confirmation by touching given file name.
    If file exists and is within max_age_days, proceeds.

    Args:
        trust_file:
        warning_msg:
        max_age_days: set to -1 for never reprompt

    Returns:

    """
    path = Path(trust_file)

    # If file exists and was modified within max_age_days, skip prompt
    if path.exists():
        if max_age_days == -1:
            return True
        mtime = datetime.fromtimestamp(path.stat().st_mtime)
        if datetime.now() - mtime <= timedelta(days=max_age_days):
            return True

    # Otherwise, prompt user
    print(f"⚠️  WARNING: {warning_msg}")
    response = input("Do you want to continue this action? (y/n): ").strip().lower()

    if response == "y":
        # Touch the file to update mod time
        path.touch()
        print(f"✔️  Trust recorded. Will not reprompt for {max_age_days}. Proceeding...")
        return True
    else:
        print("❌  Will not record trust.")
        return False