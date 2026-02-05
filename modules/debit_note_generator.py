"""
Debit Note Generator Module
Handles generation of debit notes from interest calculations
"""

import pandas as pd
from datetime import datetime


class DebitNoteGenerator:
    """Class for generating debit notes from interest calculations"""
    
    def __init__(self, invoice_prefix: str = "CDN/SA-", starting_number: int = 311):
        """
        Initialize the DebitNoteGenerator
        
        Args:
            invoice_prefix: Prefix for invoice numbers (default: "CDN/SA-")
            starting_number: Starting number for invoice sequence (default: 311)
        """
        self.invoice_prefix = invoice_prefix
        self.starting_number = starting_number
    
    def group_by_customer(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Group by customer and sales person to aggregate interest amounts
        
        Args:
            df: DataFrame with interest calculations
            
        Returns:
            Grouped DataFrame
        """
        df_grouped = df.groupby([
            'Customer Number',
            'Customer Name',
            'Area Name',
            'Region',
            'Sales person'
        ]).agg({
            'interest amount': 'sum'
        }).reset_index()
        
        # Rename columns for debit note format
        df_grouped = df_grouped.rename(columns={'interest amount': 'Total'})
        
        return df_grouped
    
    def round_totals(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Round Total to nearest integer
        
        Args:
            df: DataFrame
            
        Returns:
            DataFrame with rounded totals
        """
        df['Total'] = df['Total'].round().astype(int)
        return df
    
    def add_debit_note_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add all required debit note fields
        
        Args:
            df: Grouped DataFrame
            
        Returns:
            DataFrame with debit note fields
        """
        df['Description'] = 'OD Charges Dec-2025'
        df['Invoice Status'] = 'Open'
        df['Accounts Receivable'] = 'Accounts Receivable'
        df['Is Inclusive Tax'] = True
        df['SubTotal'] = df['Total']
        df['Balance'] = df['Total']
        df['Notes'] = 'OD Charges Dec-2025'
        df['Invoice Type'] = 'Debit Notes'
        df['Location Name'] = 'Head Office'
        df['Item Desc'] = 'OD Charges Dec-2025'
        df['Quantity'] = 1
        df['Item Total'] = df['Total']
        df['Item Price'] = df['Total']
        df['Item Type'] = 'service'
        df['Reason for issuing Debit Note'] = 'Others'
        df['Account'] = 'OD CHARGES'
        df['Line Item Location Name'] = 'HEAD OFFICE'
        df['Supply Type'] = 'Out of Scope'
        df['CF.Bill Type'] = 'Credit'
        df['Invoice Date'] = datetime.now().strftime('%Y-%m-%d')
        df['Invoice No.'] = ''
        
        return df
    
    def generate_invoice_numbers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate sequential invoice numbers
        
        Args:
            df: DataFrame
            
        Returns:
            DataFrame with invoice numbers
        """
        df['Invoice No.'] = [
            f"{self.invoice_prefix}{str(i + self.starting_number).zfill(6)}"
            for i in range(len(df))
        ]
        return df
    
    def rename_customer_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Rename Customer Number to Customer ID
        
        Args:
            df: DataFrame
            
        Returns:
            DataFrame with renamed column
        """
        df = df.rename(columns={'Customer Number': 'Customer ID'})
        return df
    
    def select_final_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Select and order final columns for output
        
        Args:
            df: DataFrame
            
        Returns:
            DataFrame with final column selection
        """
        cols_to_keep = [
            'Invoice Date', 'Invoice No.', 'Invoice Status', 'Accounts Receivable',
            'Customer ID', 'Customer Name', 'Is Inclusive Tax', 'SubTotal', 'Total',
            'Balance', 'Notes', 'Invoice Type', 'Location Name', 'Item Desc',
            'Quantity', 'Item Total', 'Item Price', 'Sales person', 'Item Type',
            'Reason for issuing Debit Note', 'Account', 'Line Item Location Name',
            'Supply Type', 'CF.Bill Type'
        ]
        
        df_final = df[cols_to_keep].copy()
        
        # Sort by Customer ID
        df_final = df_final.sort_values(by='Customer ID').reset_index(drop=True)
        
        return df_final
    
    def generate_debit_notes(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Perform all debit note generation operations
        
        Args:
            df: DataFrame with interest calculations
            
        Returns:
            DataFrame with generated debit notes
        """
        # Group by customer
        df = self.group_by_customer(df)
        
        # Round totals
        df = self.round_totals(df)
        
        # Add debit note fields
        df = self.add_debit_note_fields(df)
        
        # Generate invoice numbers
        df = self.generate_invoice_numbers(df)
        
        # Rename customer column
        df = self.rename_customer_column(df)
        
        # Select final columns
        df_final = self.select_final_columns(df)
        
        return df_final
