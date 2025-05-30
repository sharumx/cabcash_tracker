import json
from datetime import datetime

class IncomeCounter:
    def __init__(self):
        self.total_income = 0
        self.daily_income = {}  # Example: {'2025-01-04': {'Cash': 50.0, 'Credit/Debit': 67.44}}

    def add_income(self, stream, amount, date):
        if date not in self.daily_income:
            self.daily_income[date] = {}
        if stream in self.daily_income[date]:
            self.daily_income[date][stream] += amount
        else:
            self.daily_income[date][stream] = amount
        self.total_income += amount

    def get_total_income(self):
        return sum(sum(streams.values()) for streams in self.daily_income.values())

    def get_income_by_date(self, date):
        return self.daily_income.get(date, {})

    def reset_counter(self, date=None):
        if date:
            if date in self.daily_income:
                del self.daily_income[date]
        else:
            self.daily_income.clear()
            self.total_income = 0

    def display_summary(self):
        total_income = self.get_total_income()
        print("Total Income:", total_income)
        for date, streams in self.daily_income.items():
            print(f"\nIncome on {date}:")
            for stream, amount in streams.items():
                print(f"  {stream}: ${amount}")

# Utility functions

def save_data_to_json_file(data, filename="income_log.json"):
    try:
        with open(filename, "r") as file:
            existing_data = json.load(file)
            if not isinstance(existing_data, list):
                existing_data = [existing_data]  # Convert to list if it's a dictionary
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    existing_data.append(data)

    with open(filename, "w") as file:
        json.dump(existing_data, file, indent=4)

    print("Data saved successfully.")

def load_data_from_json_file(filename="income_log.json"):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except FileNotFoundError:
        print("No existing data found. Starting fresh.")
        return []

def template(daily_income_dict, total_income):
    current_date = datetime.now().date().strftime("%Y-%m-%d")
    return {
        "Date": current_date,
        "Revenue Streams": daily_income_dict,
        "Total Income": total_income
    }

def main():
    counter = IncomeCounter()

    # Initialize variables for today's data
    daily_income_dict = {}
    current_date = datetime.now().date().strftime("%Y-%m-%d")
    formatted_date = datetime.now().strftime("%B %d, %Y")
    print(f'DATE: {formatted_date}\n')

    # Define revenue streams
    revenue_input = [
        "Cash",
        "Credit/Debit",
        "Gift Purchase",
        "Passenger App",
        "Charge Slips",
        "Coupons",
        "Paperless E-Voucher"
    ]

    # Input revenue amounts
    for revenue_stream in revenue_input:
        while True:
            try:
                daily_income_input = float(input(f"Please Enter an amount for {revenue_stream}: $"))
                daily_income_dict[revenue_stream] = daily_income_input
                break
            except ValueError:
                print("Invalid input, please enter a numeric value.")
        
        # Confirmation of input
        confirm = input(f"Is the following Revenue stream and Income Input correct?\n{revenue_stream} = ${daily_income_input:.2f} (y/n): ").strip().lower()
        if confirm != 'y':
            print("Please enter the correct amount.")
            continue

        print(f'\n*** Revenue Stream ***\n{revenue_stream} = ${daily_income_input:.2f}')

    # Add today's income to the counter
    for stream, amount in daily_income_dict.items():
        counter.add_income(stream, amount, current_date)

    # Save today's data to JSON
    today_total_income = sum(daily_income_dict.values())
    entry = template(daily_income_dict, today_total_income)
    save_data_to_json_file(entry)

    # Display today's summary
    print("\nSummary:")
    print(f"Total Income: ${today_total_income:.2f}")
    print(f"\nIncome on {current_date}:")
    for stream, amount in daily_income_dict.items():
        print(f"  {stream}: ${amount:.2f}")

    print("\nGoodbye :)")

if __name__ == "__main__":
    main()
