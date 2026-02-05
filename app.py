"""
Debit Note Generator - Streamlit Application
Main application file for generating debit notes from overdue invoices
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import io

# Import custom modules
from modules.data_processor import DataProcessor
from modules.interest_calculator import InterestCalculator
from modules.debit_note_generator import DebitNoteGenerator

# Page configuration
st.set_page_config(
    page_title="Debit Note Generator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">📊 Debit Note Generator</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Interest rate configuration
        st.subheader("Interest Settings")
        per_day_rate = st.number_input(
            "Per Day Interest Rate (%)",
            min_value=0.0,
            max_value=10.0,
            value=0.06,
            step=0.01,
            help="Daily interest rate percentage"
        )
        
        due_days_threshold = st.number_input(
            "Due Days Threshold",
            min_value=0,
            max_value=365,
            value=150,
            step=1,
            help="Days after which interest is calculated"
        )
        
        max_working_days = st.number_input(
            "Max Working Days",
            min_value=1,
            max_value=100,
            value=31,
            step=1,
            help="Maximum working days for interest calculation"
        )
        
        st.markdown("---")
        
        # Invoice number configuration
        st.subheader("Invoice Settings")
        invoice_prefix = st.text_input(
            "Invoice Prefix",
            value="CDN/SA-",
            help="Prefix for generated invoice numbers"
        )
        
        starting_number = st.number_input(
            "Starting Invoice Number",
            min_value=1,
            max_value=999999,
            value=311,
            step=1,
            help="Starting number for invoice sequence"
        )
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["📤 Upload & Process", "📊 Results", "📥 Download"])
    
    with tab1:
        st.markdown('<div class="section-header">Upload Raw Data</div>', unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Upload your raw Excel file (raw.xlsx)",
            type=['xlsx', 'xls'],
            help="Upload the Excel file containing overdue invoice data"
        )
        
        if uploaded_file is not None:
            try:
                # Read the uploaded file
                df_raw = pd.read_excel(uploaded_file)
                
                st.success(f"✅ File uploaded successfully! Found {len(df_raw)} rows and {len(df_raw.columns)} columns.")
                
                # Show preview
                with st.expander("📋 Preview Raw Data (First 10 rows)"):
                    st.dataframe(df_raw.head(10), use_container_width=True)
                
                # Process button
                if st.button("🚀 Process Data & Generate Debit Notes", type="primary", use_container_width=True):
                    with st.spinner("Processing data..."):
                        # Initialize processors
                        data_processor = DataProcessor()
                        interest_calculator = InterestCalculator(
                            per_day_rate=per_day_rate,
                            due_days_threshold=due_days_threshold,
                            max_working_days=max_working_days
                        )
                        debit_note_gen = DebitNoteGenerator(
                            invoice_prefix=invoice_prefix,
                            starting_number=starting_number
                        )
                        
                        # Step 1: Clean and filter data
                        st.info("Step 1/3: Cleaning and filtering data...")
                        df_filtered = data_processor.filter_overdue(df_raw)
                        df_cleaned = data_processor.clean_data(df_filtered)
                        
                        # Step 2: Calculate interest
                        st.info("Step 2/3: Calculating interest...")
                        df_with_interest = interest_calculator.calculate_interest(df_cleaned)
                        
                        # Step 3: Generate debit notes
                        st.info("Step 3/3: Generating debit notes...")
                        df_debit_notes = debit_note_gen.generate_debit_notes(df_with_interest)
                        
                        # Store in session state
                        st.session_state['df_interest'] = df_with_interest
                        st.session_state['df_debit_notes'] = df_debit_notes
                        st.session_state['processed'] = True
                        st.session_state['current_tab'] = 1  # Move to Results tab
                        
                        st.success("✅ Processing complete! Click 'Next: View Results' below.")
                        st.balloons()
                
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
                st.exception(e)
        else:
            st.info("👆 Please upload an Excel file to begin.")
        
        # Navigation button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col3:
            if 'processed' in st.session_state and st.session_state['processed']:
                if st.button("Next: View Results ➡️", type="primary", use_container_width=True):
                    st.session_state['current_tab'] = 1
                    st.rerun()
    
    with tab2:
        st.markdown('<div class="section-header">Processing Results</div>', unsafe_allow_html=True)
        
        if 'processed' in st.session_state and st.session_state['processed']:
            df_interest = st.session_state['df_interest']
            df_debit_notes = st.session_state['df_debit_notes']
            
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Total Transactions",
                    f"{len(df_interest):,}",
                    help="Number of overdue transactions"
                )
            
            with col2:
                st.metric(
                    "Total Interest",
                    f"₹{df_interest['interest amount'].sum():,.2f}",
                    help="Total interest amount calculated"
                )
            
            with col3:
                st.metric(
                    "Debit Notes",
                    f"{len(df_debit_notes):,}",
                    help="Number of debit notes generated"
                )
            
            with col4:
                st.metric(
                    "Avg Interest/Note",
                    f"₹{df_debit_notes['Total'].mean():,.2f}",
                    help="Average interest per debit note"
                )
            
            st.markdown("---")
            
            # Interest calculation details
            st.subheader("📈 Interest Calculation Details")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Interest Statistics**")
                stats_df = pd.DataFrame({
                    'Metric': ['Total Interest', 'Average Interest', 'Max Interest', 'Min Interest'],
                    'Amount (₹)': [
                        f"{df_interest['interest amount'].sum():,.2f}",
                        f"{df_interest['interest amount'].mean():,.2f}",
                        f"{df_interest['interest amount'].max():,.2f}",
                        f"{df_interest['interest amount'].min():,.2f}"
                    ]
                })
                st.dataframe(stats_df, use_container_width=True, hide_index=True)
            
            with col2:
                st.markdown("**Top 5 Customers by Interest**")
                top_customers = df_interest.groupby('Customer Name')['interest amount'].sum().sort_values(ascending=False).head(5)
                top_df = pd.DataFrame({
                    'Customer': top_customers.index,
                    'Interest (₹)': [f"{v:,.2f}" for v in top_customers.values]
                })
                st.dataframe(top_df, use_container_width=True, hide_index=True)
            
            # Data tables
            st.markdown("---")
            
            view_option = st.radio(
                "Select data to view:",
                ["Interest Calculations", "Debit Notes"],
                horizontal=True
            )
            
            if view_option == "Interest Calculations":
                st.subheader("💰 Interest Calculation Details")
                st.info(f"Showing all {len(df_interest)} records")
                st.dataframe(df_interest, use_container_width=True)
            else:
                st.subheader("📄 Generated Debit Notes")
                st.info(f"Showing all {len(df_debit_notes)} records")
                st.dataframe(df_debit_notes, use_container_width=True)
            
            # Navigation buttons
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button("⬅️ Back to Upload", use_container_width=True):
                    st.session_state['current_tab'] = 0
                    st.rerun()
            with col3:
                if st.button("Next: Download ➡️", type="primary", use_container_width=True):
                    st.session_state['current_tab'] = 2
                    st.rerun()
        
        else:
            st.info("👈 Please upload and process data in the 'Upload & Process' tab first.")
    
    with tab3:
        st.markdown('<div class="section-header">Download Results</div>', unsafe_allow_html=True)
        
        if 'processed' in st.session_state and st.session_state['processed']:
            df_debit_notes = st.session_state['df_debit_notes']
            
            st.success("✅ Your debit notes are ready for download!")
            
            # Convert to Excel
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_debit_notes.to_excel(writer, index=False, sheet_name='Debit Notes')
            
            excel_data = output.getvalue()
            
            # Download button
            st.download_button(
                label="📥 Download Debit Notes (Excel)",
                data=excel_data,
                file_name=f"debit_notes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
                type="primary"
            )
            
            # Summary
            st.markdown("---")
            st.subheader("📊 Download Summary")
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Total Records:** {len(df_debit_notes)}")
                st.info(f"**Total Amount:** ₹{df_debit_notes['Total'].sum():,.2f}")
            
            with col2:
                st.info(f"**File Format:** Excel (.xlsx)")
                st.info(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Navigation buttons
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button("⬅️ Back to Results", use_container_width=True):
                    st.session_state['current_tab'] = 1
                    st.rerun()
            with col3:
                if st.button("🔄 Start New Process", type="secondary", use_container_width=True):
                    # Clear session state
                    for key in ['df_interest', 'df_debit_notes', 'processed']:
                        if key in st.session_state:
                            del st.session_state[key]
                    st.session_state['current_tab'] = 0
                    st.rerun()
        
        else:
            st.info("👈 Please upload and process data in the 'Upload & Process' tab first.")

if __name__ == "__main__":
    main()
