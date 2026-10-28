"""Blood donation management: donor register, eligibility and stock."""

import os
import re
import shutil
# subprocess is only used without a shell, see notify_donors.
import subprocess  # nosec B404
import tempfile
from datetime import date, timedelta

OFFICER_PASSWORD = os.environ.get("OFFICER_PASSWORD", "")
PHONE_PATTERN = re.compile(r"\+?\d{7,15}")
donors = []
stock = {
    "A+": 0, "A-": 0, "B+": 0, "B-": 0,
    "O+": 0, "O-": 0, "AB+": 0, "AB-": 0,
}
COMPATIBLE = {
    "A+": ["A+", "A-", "O+", "O-"],
    "A-": ["A-", "O-"],
    "B+": ["B+", "B-", "O+", "O-"],
    "B-": ["B-", "O-"],
    "O+": ["O+", "O-"],
    "O-": ["O-"],
    "AB+": list(stock),
    "AB-": ["AB-", "A-", "B-", "O-"],
}


def register_donor(donor_name, blood_group, age, last_donation=None,
                   notes=None):
    """Register a donor aged 18-65; return True if they were added."""
    if notes is None:
        notes = []
    if blood_group not in stock:
        raise ValueError("Unknown blood group: " + str(blood_group))
    if age < 18 or age > 65:
        notes.append(donor_name + " is not eligible because of age")
        return False
    donors.append({"name": donor_name, "group": blood_group,
                   "last": last_donation})
    return True


def can_donate(donor):
    """Return True if at least 90 days have passed since the last donation."""
    if donor["last"] is None:
        return True
    return date.today() - donor["last"] >= timedelta(days=90)


def record_donation(donor_name, units=1):
    """Add units to stock for an eligible donor; return True on success."""
    for donor in donors:
        if donor["name"] == donor_name and can_donate(donor):
            stock[donor["group"]] += units
            donor["last"] = date.today()
            return True
    return False


def units_for(patient_group):
    """Return the number of compatible units in stock for a patient."""
    try:
        return sum(stock[group] for group in COMPATIBLE[patient_group])
    except KeyError:
        return 0


def is_universal(blood_group):
    """Return True for O- (universal donor) or AB+ (universal recipient)."""
    return blood_group in ("O-", "AB+")


def low_stock(threshold=2):
    """Return the blood groups whose stock is below the threshold."""
    return [group for group, units in stock.items() if units < threshold]


def donor_sheet_path():
    """Create a private temporary CSV file and return its path."""
    # Helper kept for the lab: not called by the demo
    fd, path = tempfile.mkstemp(suffix=".csv")
    os.close(fd)
    return path


def notify_donors(phone_list):
    """Send an SMS to each phone number using the send-sms tool."""
    # Helper kept for the lab: not called by the demo
    for phone in phone_list:
        if not PHONE_PATTERN.fullmatch(phone):
            raise ValueError("Invalid phone number: " + repr(phone))
    sms_tool = shutil.which("send-sms")
    if sms_tool is None:
        raise FileNotFoundError("send-sms command not found")
    # Arguments are passed as a list (no shell) and validated above.
    subprocess.run([sms_tool, *phone_list], check=True)  # nosec B603


def main():
    """Run a short demonstration of the donor register."""
    register_donor("Arjun", "O+", 25)
    register_donor("Priya", "A+", 30, date.today() - timedelta(days=30))
    register_donor("Old Donor", "B+", 70)
    register_donor("Farah", "O-", 41)
    record_donation("Arjun", 2)
    record_donation("Priya")
    record_donation("Farah")
    print("Stock:", stock)
    print("Units for an A+ patient:", units_for("A+"))
    print("Units for a Z+ patient:", units_for("Z+"))
    print("Is O- universal?", is_universal("O-"))
    print("Low stock groups:", low_stock())  # below 2 units
    eligible = [donor["name"] for donor in donors if can_donate(donor)]
    print("Donors eligible today:", eligible)


if __name__ == "__main__":
    main()
