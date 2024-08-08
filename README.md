# README

## Overview

This script is designed to analyze payment patterns from a CSV file containing financial transaction data. The analysis includes the total credit and debit amounts, the total spent on UPI payments, other payments, and specific transactions like those with Zerodha and KSRTC. The results are then displayed in a bar chart for visual representation.

## Prerequisites

Ensure you have the following Python packages installed:
- `argparse`
- `pandas`
- `matplotlib`

You can install these packages using pip:
```bash
pip install pandas matplotlib
```

## How to Use

1. **Command Line Execution:**
   - Uncomment the `argparse` section of the script to enable command-line input.
   - Run the script from the command line, providing the path to the CSV file as an argument:
     ```bash
     python script_name.py path_to_csv_file
     ```

2. **Direct Execution:**
   - Set the `file_path` variable to the path of your CSV file in the script.
   - Execute the script in your Python environment.

## Example CSV Structure

The CSV file should have the following columns:
- `Credit Amount`
- `Debit Amount`
- `Narration`

Each transaction should be recorded as a row under these columns.

## Script Functionality

1. **Reading the CSV File:**
   - The script reads the CSV file in chunks to handle large files efficiently.

2. **Calculating Totals:**
   - Sums up the credit and debit amounts.
   - Filters and sums transactions based on specific narrations (e.g., UPI, Zerodha, KSRTC).

3. **Displaying Results:**
   - Prints the calculated totals and percentages.
   - Plots a bar chart to visualize the financial overview.

## Customization

- Modify the `chunk_size` variable to adjust the number of rows processed per chunk.
- Update the filters in the script to include or exclude specific transactions as needed.

## Sample Execution

```python
file_path = "statement_XX5065_07082024.csv"
analyse_payment_pattern(file_path)
```

This sample execution will process the specified CSV file and display the results in the console and as a bar chart.

## Troubleshooting

- Ensure the CSV file path is correct.
- Verify the CSV file has the required columns.
- Check for and handle any parsing errors or missing data in the CSV.

## Additional Information

For further assistance, refer to the official documentation of the libraries used:
- [Pandas Documentation](https://pandas.pydata.org/pandas-docs/stable/)
- [Matplotlib Documentation](https://matplotlib.org/stable/contents.html)