# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import argparse

import pandas as pd
import matplotlib.pyplot as plt


def analyse_payment_pattern(file_path):
    print(f'File path {file_path}')

    chunk_size = 100
    credit_amount = 0
    debit_amount = 0
    total_upi_spent = 0
    other_payments = 0
    amount_spent_on_zerodha = 0
    amount_spent_on_ksrtc = 0
    amount_from_fd = 0

    CREDIT_AMOUNT_CLM = 'Credit Amount'
    DEBIT_AMOUNT_CLM = 'Debit Amount'
    NARRATION = 'Narration'

    for chunk in pd.read_csv(file_path, low_memory=False, chunksize=chunk_size, on_bad_lines='skip', delimiter=','):
        chunk.columns = chunk.columns.str.strip()

        if DEBIT_AMOUNT_CLM in chunk:
            # check for the empty ness in the
            credit_amount += chunk[CREDIT_AMOUNT_CLM].sum()

            debit_amount += chunk[DEBIT_AMOUNT_CLM].sum()

            filtered_narration_type = chunk[chunk[('%s' % NARRATION)].str.contains("UPI")]
            total_upi_spent += filtered_narration_type[DEBIT_AMOUNT_CLM].sum()

            filtered_upi_zerodha = chunk[chunk[NARRATION].str.contains("UPI-ZERODHA")]
            amount_spent_on_zerodha += filtered_upi_zerodha[DEBIT_AMOUNT_CLM].sum()

            filtered_ksrtc_payment = chunk[chunk[NARRATION].str.contains("UPI-KARNATAKA")]
            amount_spent_on_ksrtc += filtered_ksrtc_payment[DEBIT_AMOUNT_CLM].sum()

            other_upi_payment = chunk[~chunk[NARRATION].str.contains("UPI")]
            other_payments += other_upi_payment[DEBIT_AMOUNT_CLM].sum()

            filtered_fd_payments = chunk[chunk[NARRATION].str.contains("PRIN")]
            amount_from_fd += filtered_fd_payments[CREDIT_AMOUNT_CLM].sum()

    print(f'Total credit amount {credit_amount:.2f}')
    print(f'Debit account balance details {debit_amount:.2f}')
    print(f'Total Spent on UPI payment {total_upi_spent}')
    print(f'Total Spent other than UPI payment {other_payments}')
    print(f'Total Spent on Zerodha Broking firm {amount_spent_on_zerodha}')
    print(f'Total Spent on KSRTC firm {amount_spent_on_ksrtc}')
    print(f'From FD {amount_from_fd}')

    if credit_amount > 0:
        percentage_upi_payment = (total_upi_spent / credit_amount) * 100
        print(f'Total percentage of UPI payment: {percentage_upi_payment:.2f}%')
    else:
        print('Total percentage of UPI payment: 0.00%')

    # Plotting the chart
    categories = [
        "Credit Amount",
        "Debit Amount",
        "Total UPI Spent",
        "Other Payments",
        "Amount Spent on Zerodha",
        "Amount Spent on KSRTC",
        "From FD"
    ]
    values = [
        credit_amount,
        debit_amount,
        total_upi_spent,
        other_payments,
        amount_spent_on_zerodha,
        amount_spent_on_ksrtc,
        amount_from_fd
    ]

    plt.figure(figsize=(10, 6))
    plt.bar(categories, values, color=['blue', 'orange', 'green', 'red', 'purple', 'brown', 'purple'])
    plt.xlabel('Categories')
    plt.ylabel('Amount (in Rupees)')
    plt.title('Financial Overview')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Analyze payment patterns in a CSV file.')
    # parser.add_argument('file_path', type=str, help='Path to the CSV file')
    # args = parser.parse_args()

    # analyse_payment_pattern(args.file_path)
    file_path = "statement_XX5065_07082024.csv"
    analyse_payment_pattern(file_path)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
