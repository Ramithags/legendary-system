import argparse
import os

import pandas as pd
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor, as_completed


def process_chunk(chunk):
    CREDIT_AMOUNT_CLM = 'Credit Amount'
    DEBIT_AMOUNT_CLM = 'Debit Amount'
    NARRATION = 'Narration'

    chunk.columns = chunk.columns.str.strip()

    # Replace empty strings with NaN and then fill NaN with 0
    chunk[CREDIT_AMOUNT_CLM] = chunk[CREDIT_AMOUNT_CLM].replace('', 0).astype(float)
    chunk[DEBIT_AMOUNT_CLM] = chunk[DEBIT_AMOUNT_CLM].replace('', 0).astype(float)

    credit_amount = chunk[CREDIT_AMOUNT_CLM].sum()
    debit_amount = chunk[DEBIT_AMOUNT_CLM].sum()

    filtered_narration_type = chunk[chunk[NARRATION].str.contains("UPI", na=False)]
    total_upi_spent = filtered_narration_type[DEBIT_AMOUNT_CLM].sum()

    filtered_upi_zerodha = chunk[chunk[NARRATION].str.contains("UPI-ZERODHA", na=False)]
    amount_spent_on_zerodha = filtered_upi_zerodha[DEBIT_AMOUNT_CLM].sum()

    filtered_ksrtc_payment = chunk[chunk[NARRATION].str.contains("UPI-KARNATAKA", na=False)]
    amount_spent_on_ksrtc = filtered_ksrtc_payment[DEBIT_AMOUNT_CLM].sum()

    other_upi_payment = chunk[~chunk[NARRATION].str.contains("UPI", na=False)]
    other_payments = other_upi_payment[DEBIT_AMOUNT_CLM].sum()

    filtered_fd_payments = chunk[chunk[NARRATION].str.contains("PRIN", na=False)]
    amount_from_fd = filtered_fd_payments[CREDIT_AMOUNT_CLM].sum()

    return {
        'credit_amount': credit_amount,
        'debit_amount': debit_amount,
        'total_upi_spent': total_upi_spent,
        'amount_spent_on_zerodha': amount_spent_on_zerodha,
        'amount_spent_on_ksrtc': amount_spent_on_ksrtc,
        'other_payments': other_payments,
        'amount_from_fd': amount_from_fd
    }


def analyse_payment_pattern(file_path):
    if not file_path:
        print("Error: File path is empty.")
        return

    if not os.path.isfile(file_path):
        print(f"Error: File '{file_path}' not found.")
        return

    print(f'File path: {file_path}')


    chunk_size = 100

    with ThreadPoolExecutor() as executor:
        futures = []
        for chunk in pd.read_csv(file_path, low_memory=False, chunksize=chunk_size, on_bad_lines='skip', delimiter=','):
            futures.append(executor.submit(process_chunk, chunk))

        results = {
            'credit_amount': 0,
            'debit_amount': 0,
            'total_upi_spent': 0,
            'amount_spent_on_zerodha': 0,
            'amount_spent_on_ksrtc': 0,
            'other_payments': 0,
            'amount_from_fd': 0
        }

        for future in as_completed(futures):
            chunk_result = future.result()
            for key in results.keys():
                results[key] += chunk_result[key]

    print(f'Total credit amount {results["credit_amount"]:.2f}')
    print(f'Debit account balance details {results["debit_amount"]:.2f}')
    print(f'Total Spent on UPI payment {results["total_upi_spent"]}')
    print(f'Total Spent other than UPI payment {results["other_payments"]}')
    print(f'Total Spent on Zerodha Broking firm {results["amount_spent_on_zerodha"]}')
    print(f'Total Spent on KSRTC firm {results["amount_spent_on_ksrtc"]}')
    print(f'From FD {results["amount_from_fd"]}')

    if results['credit_amount'] > 0:
        percentage_upi_payment = (results['total_upi_spent'] / results['credit_amount']) * 100
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
        results['credit_amount'],
        results['debit_amount'],
        results['total_upi_spent'],
        results['other_payments'],
        results['amount_spent_on_zerodha'],
        results['amount_spent_on_ksrtc'],
        results['amount_from_fd']
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
    file_path = "2022-jul.csv"
    analyse_payment_pattern(file_path)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
