"""
Data Processor Module
Handles data cleaning, filtering, and preprocessing
"""

import pandas as pd
import numpy as np


class DataProcessor:
    """Class for processing and cleaning raw invoice data"""
    
    def __init__(self):
        """Initialize the DataProcessor"""
        pass
    
    def filter_overdue(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter only overdue status rows
        
        Args:
            df: Raw DataFrame
            
        Returns:
            Filtered DataFrame with only overdue records
        """
        df_filtered = df[df['Status'] == 'Overdue'].copy()
        return df_filtered
    
    def remove_duplicate_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove duplicate columns
        
        Args:
            df: DataFrame
            
        Returns:
            DataFrame with duplicate columns removed
        """
        columns_to_drop = ['Sale person']
        df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])
        return df
    
    def clean_currency_column(self, df: pd.DataFrame, column_name: str, fill_na: float = 0) -> pd.DataFrame:
        """
        Clean currency column by removing rupee symbol and commas
        
        Args:
            df: DataFrame
            column_name: Name of the column to clean
            fill_na: Value to fill NaN with (default: 0)
            
        Returns:
            DataFrame with cleaned column
        """
        df[column_name] = (
            df[column_name]
            .astype(str)
            .str.replace('₹', '', regex=False)
            .str.replace(',', '', regex=False)
            .str.strip()
        )
        df[column_name] = pd.to_numeric(df[column_name], errors='coerce').fillna(fill_na)
        return df
    
    def clean_age_column(self, df: pd.DataFrame, opening_balance_age: int = 300) -> pd.DataFrame:
        """
        Clean Age column by removing 'Days' text and converting to numeric
        
        Args:
            df: DataFrame
            opening_balance_age: Age to set for Customer Opening Balance rows (default: 300)
            
        Returns:
            DataFrame with cleaned Age column
        """
        df['Age'] = (
            df['Age']
            .astype(str)
            .str.replace(' Days', '', regex=False)
            .str.strip()
        )
        df['Age'] = pd.to_numeric(df['Age'], errors='coerce')
        
        # For Customer Opening Balance rows, set Age to configurable value
        df.loc[df['Type'] == 'Customer Opening Balance', 'Age'] = opening_balance_age
        
        return df
    
    def clean_data(self, df: pd.DataFrame, opening_balance_age: int = 300) -> pd.DataFrame:
        """
        Perform all cleaning operations on the DataFrame
        
        Args:
            df: Raw filtered DataFrame
            opening_balance_age: Age to set for Customer Opening Balance rows
            
        Returns:
            Cleaned DataFrame
        """
        # Remove duplicate columns
        df = self.remove_duplicate_columns(df)
        
        # Clean currency columns
        df = self.clean_currency_column(df, 'Balance Due', fill_na=0)
        df = self.clean_currency_column(df, 'Amount', fill_na=0)
        
        # Clean Age column with configurable opening balance age
        df = self.clean_age_column(df, opening_balance_age)
        
        return df
    
    def sort_by_customer(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Sort DataFrame by Customer Name alphabetically
        
        Args:
            df: DataFrame
            
        Returns:
            Sorted DataFrame
        """
        df = df.sort_values('Customer Name').reset_index(drop=True)
        return df
