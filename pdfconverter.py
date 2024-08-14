import pdfplumber
import pandas as pd


# Function to extract tables from PDF and convert to CSV


# Function to extract tables from PDF and convert to CSV
def pdf_to_csv(pdf_path, csv_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_pages = []
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                all_pages.extend(table)

        # Create a DataFrame from the extracted tables
        df = pd.DataFrame(all_pages[1:], columns=all_pages[0])

        # Apply cleaning function to relevant columns

        # Save DataFrame to CSV
        df.to_csv(csv_path, index=False)

# Example usage


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Analyze payment patterns in a CSV file.')
    # parser.add_argument('file_path', type=str, help='Path to the CSV file')
    # args = parser.parse_args()

    # analyse_payment_pattern(args.file_path)e
    pdf_path = 'Small-Check.pdf'
    csv_path = 'output.csv'
    pdf_to_csv(pdf_path, csv_path)

