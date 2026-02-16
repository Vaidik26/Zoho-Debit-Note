"""
Interest Calculator Module
Handles all interest calculation logic
"""

import pandas as pd
import numpy as np


class InterestCalculator:
    """Class for calculating interest on overdue invoices"""
    
    def __init__(self, per_day_rate: float = 0.06, due_days_threshold: int = 150, max_working_days: int = 31):
        """
        Initialize the InterestCalculator
        
        Args:
            per_day_rate: Daily interest rate percentage (default: 0.06%)
            due_days_threshold: Days after which interest is calculated (default: 150)
            max_working_days: Maximum working days for interest calculation (default: 31)
        """
        self.per_day_rate = per_day_rate
        self.due_days_threshold = due_days_threshold
        self.max_working_days = max_working_days
    
    def filter_by_age(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Filter rows where Age is greater than due days threshold
        
        Args:
            df: DataFrame
            
        Returns:
            Filtered DataFrame
        """
        df_filtered = df[df['Age'] > self.due_days_threshold].copy()
        return df_filtered
    
    def calculate_working_days(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate interest working days and previous interest days
        
        Args:
            df: DataFrame
            
        Returns:
            DataFrame with calculated days
        """
        # Set Due days
        df['Due days'] = self.due_days_threshold
        
        # Calculate days overdue
        days_overdue = df['Age'] - self.due_days_threshold
        
        # Calculate interest working days (capped at max_working_days)
        df['interst working'] = days_overdue.clip(upper=self.max_working_days)
        
        # Calculate Previous interest (cumulative days before current working period)
        df['Previous interst'] = days_overdue - df['interst working']
        
        return df
    
    def calculate_interest_percentage(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate interest percentage based on working days
        
        Args:
            df: DataFrame
            
        Returns:
            DataFrame with interest percentages
        """
        # Set per day interest rate
        df['per day interst%'] = self.per_day_rate
        
        # Calculate working interest percentage
        df['working interst in %'] = df['interst working'] * df['per day interst%']
        
        return df
    
    def calculate_interest_amount(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate final interest amount
        
        Args:
            df: DataFrame
            
        Returns:
            DataFrame with interest amounts
        """
        # Calculate interest amount
        df['interest amount'] = df['Balance Due'] * (df['working interst in %'] / 100)
        
        # Round to 4 decimal places
        df['interest amount'] = df['interest amount'].round(4)
        
        return df
    
    def select_final_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Select and order final columns
        
        Args:
            df: DataFrame
            
        Returns:
            DataFrame with final column selection
        """
        final_columns = [
            'Region',
            'Area Name',
            'Market',
            'Customer Name',
            'Customer Number',
            'DATE',
            'Transaction#',
            'Type',
            'Status',
            'Due Date',
            'Amount',
            'Balance Due',
            'Age',
            'Due days',
            'Previous interst',
            'interst working',
            'per day interst%',
            'working interst in %',
            'interest amount',
            'Sale Person'
        ]
        
        df_output = df[final_columns]
        return df_output
    
    def calculate_interest(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Perform all interest calculation operations
        
        Args:
            df: Cleaned DataFrame
            
        Returns:
            DataFrame with interest calculations
        """
        # Filter by age threshold
        df = self.filter_by_age(df)
        
        # Sort by customer name
        df = df.sort_values('Customer Name').reset_index(drop=True)
        
        # Calculate working days
        df = self.calculate_working_days(df)
        
        # Calculate interest percentage
        df = self.calculate_interest_percentage(df)
        
        # Calculate interest amount
        df = self.calculate_interest_amount(df)
        
        # Select final columns
        df_output = self.select_final_columns(df)
        
        return df_output
