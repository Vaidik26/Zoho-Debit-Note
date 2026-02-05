# Debit Note Generator - Streamlit Application

A professional web application for generating debit notes from overdue invoices with automated interest calculations.

## 🚀 Features

- **📤 File Upload**: Upload raw Excel files containing overdue invoice data
- **🔧 Configurable Settings**: Customize interest rates, thresholds, and invoice numbering
- **💰 Interest Calculation**: Automatic calculation of interest on overdue invoices
- **📊 Data Visualization**: View detailed statistics and summaries
- **📄 Debit Note Generation**: Generate formatted debit notes ready for export
- **📥 Excel Export**: Download results in Excel format

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🛠️ Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd "c:/Job Workspace/Final Debit Note"
   ```

2. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Usage

1. **Start the Streamlit application**:
   ```bash
   streamlit run app.py
   ```

2. **Access the application**:
   - The application will automatically open in your default browser
   - If not, navigate to `http://localhost:8501`

3. **Upload and Process**:
   - Upload your raw Excel file (raw.xlsx)
   - Configure settings in the sidebar (optional)
   - Click "Process Data & Generate Debit Notes"

4. **View Results**:
   - Check the "Results" tab for detailed statistics
   - Review interest calculations and generated debit notes

5. **Download**:
   - Go to the "Download" tab
   - Click the download button to get your Excel file

## 📁 Project Structure

```
Final Debit Note/
├── app.py                          # Main Streamlit application
├── modules/
│   ├── __init__.py                 # Module initialization
│   ├── data_processor.py           # Data cleaning and filtering
│   ├── interest_calculator.py      # Interest calculation logic
│   └── debit_note_generator.py     # Debit note generation
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── clean_conversion.ipynb          # Original Jupyter notebook (reference)
```

## ⚙️ Configuration Options

### Interest Settings
- **Per Day Interest Rate**: Daily interest rate percentage (default: 0.06%)
- **Due Days Threshold**: Days after which interest is calculated (default: 150)
- **Max Working Days**: Maximum working days for interest calculation (default: 31)

### Invoice Settings
- **Invoice Prefix**: Prefix for generated invoice numbers (default: "CDN/SA-")
- **Starting Invoice Number**: Starting number for invoice sequence (default: 311)

## 📊 Data Processing Flow

1. **Data Upload**: Raw Excel file with overdue invoices
2. **Filtering**: Filter only "Overdue" status records
3. **Cleaning**: Remove duplicates, clean currency values, process age data
4. **Interest Calculation**:
   - Filter by age threshold (> 150 days)
   - Calculate working days (capped at 31)
   - Calculate interest percentage and amount
5. **Debit Note Generation**:
   - Group by customer and sales person
   - Generate invoice numbers
   - Format output with all required fields
6. **Export**: Download as Excel file

## 🎨 Features Breakdown

### Module: Data Processor
- Filters overdue invoices
- Removes duplicate columns
- Cleans currency values (removes ₹ and commas)
- Processes age data
- Handles Customer Opening Balance records

### Module: Interest Calculator
- Configurable interest rates and thresholds
- Calculates working days (capped)
- Computes interest percentages
- Calculates final interest amounts
- Maintains detailed calculation history

### Module: Debit Note Generator
- Groups transactions by customer
- Generates sequential invoice numbers
- Adds all required debit note fields
- Formats output for Zoho Books import
- Sorts by Customer ID

## 📝 Input Data Requirements

Your Excel file should contain the following columns:
- Region
- Area Name
- Market
- Customer Name
- Customer Number
- DATE
- Transaction#
- Type
- Status
- Age
- Due Date
- Amount
- Balance Due
- Sales person (or Sale person)

## 📤 Output Format

The generated debit notes include:
- Invoice Date
- Invoice No.
- Invoice Status
- Accounts Receivable
- Customer ID
- Customer Name
- Is Inclusive Tax
- SubTotal
- Total
- Balance
- Notes
- Invoice Type
- Location Name
- Item Desc
- Quantity
- Item Total
- Item Price
- Sales person
- Item Type
- Reason for issuing Debit Note
- Account
- Line Item Location Name
- Supply Type
- CF.Bill Type

## 🐛 Troubleshooting

**Issue**: Application won't start
- **Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`

**Issue**: File upload fails
- **Solution**: Ensure your Excel file has the required columns and is in .xlsx format

**Issue**: No data after processing
- **Solution**: Check that your data has records with "Overdue" status and Age > threshold

## 📞 Support

For issues or questions, please refer to the original Jupyter notebook (`clean_conversion.ipynb`) for the underlying logic.

## 📄 License

This project is for internal use.

---


