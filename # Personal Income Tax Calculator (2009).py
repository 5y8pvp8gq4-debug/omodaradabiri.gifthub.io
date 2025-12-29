"""
Personal Income Tax Calculator (2009) — improved

Usage examples:
  - Interactive: run the script and follow prompts
  - Non-interactive: python "c:\\Users\\DELL\\# Personal Income Tax Calculator (2009).py" -s 0 -i 50000

Outputs the total tax owed formatted to two decimals.
"""

import argparse
import sys


def compute_tax(status, income):
    """Compute the tax owed for the given filing `status` and `income`.

    status: 0=Single, 1=Married Jointly, 2=Married Separately, 3=Head of Household
    income: taxable income (float, >= 0)
    """
    brackets = {
        0: [
            (0.10, 0, 8350),
            (0.15, 8350, 33950),
            (0.25, 33950, 82250),
            (0.28, 82250, 171550),
            (0.33, 171550, 372950),
            (0.35, 372950, float("inf")),
        ],
        1: [
            (0.10, 0, 16700),
            (0.15, 16700, 67900),
            (0.25, 67900, 137050),
            (0.28, 137050, 208850),
            (0.33, 208850, 372950),
            (0.35, 372950, float("inf")),
        ],
        2: [
            (0.10, 0, 8350),
            (0.15, 8350, 33950),
            (0.25, 33950, 68525),
            (0.28, 68525, 104425),
            (0.33, 104425, 186475),
            (0.35, 186475, float("inf")),
        ],
        3: [
            (0.10, 0, 11950),
            (0.15, 11950, 45500),
            (0.25, 45500, 117450),
            (0.28, 117450, 190200),
            (0.33, 190200, 372950),
            (0.35, 372950, float("inf")),
        ],
    }

    if status not in brackets:
        raise ValueError(f"Invalid filing status: {status}")

    if income < 0:
        raise ValueError("Income must be non-negative")

    tax = 0.0
    for rate, lower, upper in brackets[status]:
        if income > lower:
            taxable_amount = min(income, upper) - lower
            tax += taxable_amount * rate
        else:
            break
    return tax


def parse_args():
    parser = argparse.ArgumentParser(description="Personal Income Tax Calculator (2009)")
    parser.add_argument("-s", "--status", type=int, choices=range(0, 4), help="Filing status (0=Single,1=Married Jointly,2=Married Separately,3=Head of Household)")
    parser.add_argument("-i", "--income", type=float, help="Taxable income (non-negative)")
    parser.add_argument("--no-input", action="store_true", help="Do not prompt for missing values; require both --status and --income")
    args = parser.parse_args()

    status = args.status
    income = args.income

    if status is None or income is None:
        if args.no_input:
            parser.error("Both --status and --income are required when --no-input is used.")
        try:
            if status is None:
                status = int(input("Enter filing status (0=Single, 1=Married Jointly, 2=Married Separately, 3=Head of Household): "))
            if income is None:
                income = float(input("Enter taxable income: "))
        except (ValueError, EOFError) as exc:
            parser.error(f"Invalid input: {exc}")

    if status not in (0, 1, 2, 3):
        parser.error("Status must be 0, 1, 2, or 3")
    if income is None or income < 0:
        parser.error("Income must be a non-negative number")

    return status, income


def main():
    status, income = parse_args()
    tax = compute_tax(status, income)
    print(f"Total tax owed: ${tax:.2f}")


if __name__ == "__main__":
    main()
