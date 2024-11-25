#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import plotly.express as px



# Title of the application
st.title("Financial Analysis Tool")

# Define conversion rates globally
conversion_rates = {
    "SAR": 4.11,
    "AED": 3.91
}

# Initialize variables with default values
if 'tab1_vars' not in st.session_state:
    st.session_state.tab1_vars = {
        "exw_cost": 0.64,
        "fob_cost": 1100.0,
        "freight_cost": 2850.0,
        "packaging_cost": 0.0,
        "warehousing_cost": 0.0,
        "markup_percentage": 21.5,
        "revenue_share_percentage": 10.0,
        "projected_units_sold": 26250,
        "salaries_aed": 0.0,
        "rental_aed": 0.0,
        "utilities_aed": 0.0,
        "sales_tax_aed": 0.0,
        "admin_aed": 0.0,
        "licences_aed": 0.0,
        "depreciation_aed": 0.0
    }

# Create tabs at the top for different functionalities
tab1, tab2, tab3 = st.tabs(["Single Product Model", "Batch Product Analysis", "Dashboard"])

# Initialize active tab in session state
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 'tab1'  # Default to Tab 1

# Update active tab based on user interaction
if tab1:
    st.session_state.active_tab = 'tab1'
elif tab2:
    st.session_state.active_tab = 'tab2'

# Sidebar logic
if st.session_state.active_tab == 'tab1':
    with st.sidebar:
        st.header("Input Parameters (Tab 1)")
        
        # COGS inputs
        st.subheader("Cost Parameters")
        st.session_state.tab1_vars["exw_cost"] = st.number_input("EXW Cost per Unit (EUR)", value=st.session_state.tab1_vars["exw_cost"], format="%.2f", key="tab1_exw_cost")
        st.session_state.tab1_vars["fob_cost"] = st.number_input("FOB Cost (Total, EUR)", value=st.session_state.tab1_vars["fob_cost"], format="%.2f", key="tab1_fob_cost")
        st.session_state.tab1_vars["freight_cost"] = st.number_input("Freight Cost (Total, EUR)", value=st.session_state.tab1_vars["freight_cost"], format="%.2f", key="tab1_freight_cost")
        st.session_state.tab1_vars["packaging_cost"] = st.number_input("Packaging and Printing Cost per Unit (EUR)", value=st.session_state.tab1_vars["packaging_cost"], format="%.2f", key="tab1_packaging_cost")
        st.session_state.tab1_vars["warehousing_cost"] = st.number_input("Warehousing Cost per Unit (EUR)", value=st.session_state.tab1_vars["warehousing_cost"], format="%.2f", key="tab1_warehousing_cost")

        # Other Tab 1 specific inputs
        st.session_state.tab1_vars["markup_percentage"] = st.number_input("Markup Percentage (%)", value=st.session_state.tab1_vars["markup_percentage"], format="%.2f", key="tab1_markup")
        st.session_state.tab1_vars["revenue_share_percentage"] = st.number_input("Revenue Share Percentage (%)", value=st.session_state.tab1_vars["revenue_share_percentage"], format="%.2f", key="tab1_revenue_share")
        st.session_state.tab1_vars["projected_units_sold"] = max(1, st.number_input("Projected Units Sold", value=st.session_state.tab1_vars["projected_units_sold"], key="tab1_units"))

        # Operating Expenses (in AED)
        st.subheader("Operating Expenses (in AED)")
        st.session_state.tab1_vars["salaries_aed"] = st.number_input("Salaries (AED)", value=st.session_state.tab1_vars["salaries_aed"], format="%.2f", key="tab1_salaries")
        st.session_state.tab1_vars["rental_aed"] = st.number_input("Rental (AED)", value=st.session_state.tab1_vars["rental_aed"], format="%.2f", key="tab1_rental")
        st.session_state.tab1_vars["utilities_aed"] = st.number_input("Utilities (AED)", value=st.session_state.tab1_vars["utilities_aed"], format="%.2f", key="tab1_utilities")
        st.session_state.tab1_vars["sales_tax_aed"] = st.number_input("Sales Tax (AED)", value=st.session_state.tab1_vars["sales_tax_aed"], format="%.2f", key="tab1_sales_tax")
        st.session_state.tab1_vars["admin_aed"] = st.number_input("Admin (AED)", value=st.session_state.tab1_vars["admin_aed"], format="%.2f", key="tab1_admin")
        st.session_state.tab1_vars["licences_aed"] = st.number_input("Licences (AED)", value=st.session_state.tab1_vars["licences_aed"], format="%.2f", key="tab1_licences")
        st.session_state.tab1_vars["depreciation_aed"] = st.number_input("Depreciation (AED)", value=st.session_state.tab1_vars["depreciation_aed"], format="%.2f", key="tab1_depreciation")

# Sidebar remains hidden for Tab 2
if st.session_state.active_tab == 'tab2':
    st.sidebar.empty()
    
# Tab 1: Single Product Model
with tab1:
    st.header("Single Product Model")
    
    # Use variables from session state
    exw_cost = st.session_state.tab1_vars["exw_cost"]
    fob_cost = st.session_state.tab1_vars["fob_cost"]
    freight_cost = st.session_state.tab1_vars["freight_cost"]
    packaging_cost = st.session_state.tab1_vars["packaging_cost"]
    warehousing_cost = st.session_state.tab1_vars["warehousing_cost"]
    markup_percentage = st.session_state.tab1_vars["markup_percentage"]
    revenue_share_percentage = st.session_state.tab1_vars["revenue_share_percentage"]
    projected_units_sold = st.session_state.tab1_vars["projected_units_sold"]
    
    # Calculate Sales Price per Unit
    base_price = exw_cost + ((freight_cost + fob_cost) / projected_units_sold) + (packaging_cost + warehousing_cost)
    selling_price = base_price + (base_price * markup_percentage / 100)

    # Revenue Share per Unit
    revenue_share_per_unit = selling_price * (revenue_share_percentage / 100)

    # Calculations for single product
    direct_revenue = selling_price * projected_units_sold  # EUR
    total_revenue_share = revenue_share_per_unit * projected_units_sold  # EUR
    total_revenue = direct_revenue + total_revenue_share  # EUR

    # Cost of Goods Sold (COGS)
    total_freight_and_logistics = freight_cost + fob_cost
    total_cogs = (
        (exw_cost * projected_units_sold)
        + total_freight_and_logistics
        + (packaging_cost * projected_units_sold)
        + (warehousing_cost * projected_units_sold)
    )

    # Gross Profit
    gross_profit_direct = direct_revenue - total_cogs  # EUR
    gross_profit_total = total_revenue - total_cogs  # EUR
    gross_margin_direct = (gross_profit_direct / direct_revenue) * 100 if direct_revenue != 0 else 0
    gross_margin_total = (gross_profit_total / total_revenue) * 100 if total_revenue != 0 else 0

    # Operating Expenses
    operating_expenses_aed = (
        (st.session_state.tab1_vars["salaries_aed"] * 12) + (st.session_state.tab1_vars["rental_aed"] * 12) + (st.session_state.tab1_vars["utilities_aed"] * 12) + st.session_state.tab1_vars["sales_tax_aed"] + st.session_state.tab1_vars["admin_aed"] + st.session_state.tab1_vars["licences_aed"] + st.session_state.tab1_vars["depreciation_aed"]
    )
    operating_expenses_eur = operating_expenses_aed / conversion_rates["AED"]
    operating_expenses_sar = operating_expenses_aed / (conversion_rates["AED"] / conversion_rates["SAR"])

    # Net Profit
    net_profit_direct = gross_profit_direct - operating_expenses_eur  # EUR
    net_profit_total = gross_profit_total - operating_expenses_eur  # EUR
    net_profit_margin_direct = (net_profit_direct / direct_revenue) * 100 if direct_revenue != 0 else 0
    net_profit_margin_total = (net_profit_total / total_revenue) * 100 if total_revenue != 0 else 0

    # Display outputs in tables
    # Revenue Table
    st.header("Revenue and Selling Price")
    revenue_data = {
        "Metric": [
            "Selling Price per Unit",
            "Number of Units Sold",
            "Direct Revenue",
            "Revenue Share per Unit",
            "Revenue Share",
            "Total Revenue"
        ],
        "EUR": [
            f"{selling_price:,.2f} EUR",
            f"{projected_units_sold:,} units",
            f"{direct_revenue:,.2f} EUR",
            f"{revenue_share_per_unit:,.2f} EUR",
            f"{total_revenue_share:,.2f} EUR",
            f"{total_revenue:,.2f} EUR"
        ],
        "SAR": [
            f"{selling_price * conversion_rates['SAR']:,.2f} SAR",
            f"{projected_units_sold:,} units",
            f"{direct_revenue * conversion_rates['SAR']:,.2f} SAR",
            f"{revenue_share_per_unit * conversion_rates['SAR']:,.2f} SAR",
            f"{total_revenue_share * conversion_rates['SAR']:,.2f} SAR",
            f"{total_revenue * conversion_rates['SAR']:,.2f} SAR"
        ],
        "AED": [
            f"{selling_price * conversion_rates['AED']:,.2f} AED",
            f"{projected_units_sold:,} units",
            f"{direct_revenue * conversion_rates['AED']:,.2f} AED",
            f"{revenue_share_per_unit * conversion_rates['AED']:,.2f} AED",
            f"{total_revenue_share * conversion_rates['AED']:,.2f} AED",
            f"{total_revenue * conversion_rates['AED']:,.2f} AED"
        ]
    }
    st.table(revenue_data)

    # COGS Table
    st.header("Cost of Goods Sold (COGS)")
    cogs_data = {
        "Metric": [
            "EXW Cost per Unit",
            "Freight and Logistics Costs",
            "Packaging and Printing Cost per Unit",
            "Warehousing Cost per Unit",
            "Total COGS"
        ],
        "EUR": [
            f"{exw_cost:,.2f} EUR",
            f"{total_freight_and_logistics:,.2f} EUR",
            f"{packaging_cost:,.2f} EUR",
            f"{warehousing_cost:,.2f} EUR",
            f"{total_cogs:,.2f} EUR"
        ],
        "SAR": [
            f"{exw_cost * conversion_rates['SAR']:,.2f} SAR",
            f"{total_freight_and_logistics * conversion_rates['SAR']:,.2f} SAR",
            f"{packaging_cost * conversion_rates['SAR']:,.2f} SAR",
            f"{warehousing_cost * conversion_rates['SAR']:,.2f} SAR",
            f"{total_cogs * conversion_rates['SAR']:,.2f} SAR"
        ],
        "AED": [
            f"{exw_cost * conversion_rates['AED']:,.2f} AED",
            f"{total_freight_and_logistics * conversion_rates['AED']:,.2f} AED",
            f"{packaging_cost * conversion_rates['AED']:,.2f} AED",
            f"{warehousing_cost * conversion_rates['AED']:,.2f} AED",
            f"{total_cogs * conversion_rates['AED']:,.2f} AED"
        ]
    }
    st.table(cogs_data)

    # Gross Profit Table
    st.header("Gross Profit")
    gross_profit_data = {
        "Metric": [
            "Gross Profit (Direct Revenue only)",
            "Gross Margin (Direct Revenue only)",
            "Gross Profit (Direct + Revenue Share)",
            "Gross Margin (Direct + Revenue Share)"
        ],
        "EUR": [
            f"{gross_profit_direct:,.2f} EUR",
            f"{gross_margin_direct:.2f}%",
            f"{gross_profit_total:,.2f} EUR",
            f"{gross_margin_total:.2f}%"
        ],
        "SAR": [
            f"{gross_profit_direct * conversion_rates['SAR']:,.2f} SAR",
            "-",
            f"{gross_profit_total * conversion_rates['SAR']:,.2f} SAR",
            "-"
        ],
        "AED": [
            f"{gross_profit_direct * conversion_rates['AED']:,.2f} AED",
            "-",
            f"{gross_profit_total * conversion_rates['AED']:,.2f} AED",
            "-"
        ]
    }
    st.table(gross_profit_data)

    # Operating Expenses Table
    st.header("Operating Expenses")
    operating_expenses_data = {
        "Metric": [
            "Salaries",
            "Rental",
            "Utilities",
            "Sales Tax",
            "Admin",
            "Licences",
            "Depreciation",
            "Total Operating Expenses"
        ],
        "AED": [
            f"{st.session_state.tab1_vars['salaries_aed']:,.2f} AED",
            f"{st.session_state.tab1_vars['rental_aed']:,.2f} AED",
            f"{st.session_state.tab1_vars['utilities_aed']:,.2f} AED",
            f"{st.session_state.tab1_vars['sales_tax_aed']:,.2f} AED",
            f"{st.session_state.tab1_vars['admin_aed']:,.2f} AED",
            f"{st.session_state.tab1_vars['licences_aed']:,.2f} AED",
            f"{st.session_state.tab1_vars['depreciation_aed']:,.2f} AED",
            f"{operating_expenses_aed:,.2f} AED"
        ],
        "EUR": [
            f"{st.session_state.tab1_vars['salaries_aed'] / conversion_rates['AED']:,.2f} EUR",
            f"{st.session_state.tab1_vars['rental_aed'] / conversion_rates['AED']:,.2f} EUR",
            f"{st.session_state.tab1_vars['utilities_aed'] / conversion_rates['AED']:,.2f} EUR",
            f"{st.session_state.tab1_vars['sales_tax_aed'] / conversion_rates['AED']:,.2f} EUR",
            f"{st.session_state.tab1_vars['admin_aed'] / conversion_rates['AED']:,.2f} EUR",
            f"{st.session_state.tab1_vars['licences_aed'] / conversion_rates['AED']:,.2f} EUR",
            f"{st.session_state.tab1_vars['depreciation_aed'] / conversion_rates['AED']:,.2f} EUR",
            f"{operating_expenses_eur:,.2f} EUR"
        ],
        "SAR": [
            f"{st.session_state.tab1_vars['salaries_aed'] / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
            f"{st.session_state.tab1_vars['rental_aed'] / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
            f"{st.session_state.tab1_vars['utilities_aed'] / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
            f"{st.session_state.tab1_vars['sales_tax_aed'] / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
            f"{st.session_state.tab1_vars['admin_aed'] / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
            f"{st.session_state.tab1_vars['licences_aed'] / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
            f"{st.session_state.tab1_vars['depreciation_aed'] / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
            f"{operating_expenses_sar:,.2f} SAR"
        ]
    }
    st.table(operating_expenses_data)

    # Net Profit Table
    st.header("Net Profit")
    net_profit_data = {
        "Metric": [
            "Net Profit (Direct Revenue only)",
            "Net Profit Margin (Direct Revenue only)",
            "Net Profit (Direct + Revenue Share)",
            "Net Profit Margin (Direct + Revenue Share)"
        ],
        "EUR": [
            f"{net_profit_direct:,.2f} EUR",
            f"{net_profit_margin_direct:.2f}%",
            f"{net_profit_total:,.2f} EUR",
            f"{net_profit_margin_total:.2f}%"
        ],
        "SAR": [
            f"{net_profit_direct * conversion_rates['SAR']:,.2f} SAR",
            "-",
            f"{net_profit_total * conversion_rates['SAR']:,.2f} SAR",
            "-"
        ],
        "AED": [
            f"{net_profit_direct * conversion_rates['AED']:,.2f} AED",
            "-",
            f"{net_profit_total * conversion_rates['AED']:,.2f} AED",
            "-"
        ]
    }
    st.table(net_profit_data)

    # Prepare data for each section
    revenue_data = {
        "Metric": [
            "Selling Price per Unit",
            "Number of Units Sold",
            "Direct Revenue",
            "Revenue Share per Unit",
            "Revenue Share",
            "Total Revenue",
        ],
        "EUR": [
            f"{selling_price:,.2f} EUR",
            f"{projected_units_sold:,} units",
            f"{direct_revenue:,.2f} EUR",
            f"{revenue_share_per_unit:,.2f} EUR",
            f"{total_revenue_share:,.2f} EUR",
            f"{total_revenue:,.2f} EUR",
        ],
        "SAR": [
            f"{selling_price * conversion_rates['SAR']:,.2f} SAR",
            f"{projected_units_sold:,} units",
            f"{direct_revenue * conversion_rates['SAR']:,.2f} SAR",
            f"{revenue_share_per_unit * conversion_rates['SAR']:,.2f} SAR",
            f"{total_revenue_share * conversion_rates['SAR']:,.2f} SAR",
            f"{total_revenue * conversion_rates['SAR']:,.2f} SAR",
        ],
        "AED": [
            f"{selling_price * conversion_rates['AED']:,.2f} AED",
            f"{projected_units_sold:,} units",
            f"{direct_revenue * conversion_rates['AED']:,.2f} AED",
            f"{revenue_share_per_unit * conversion_rates['AED']:,.2f} AED",
            f"{total_revenue_share * conversion_rates['AED']:,.2f} AED",
            f"{total_revenue * conversion_rates['AED']:,.2f} AED",
        ],
    }

    cogs_data = {
        "Metric": [
            "EXW Cost per Unit",
            "Freight and Logistics Costs",
            "Packaging and Printing Cost per Unit",
            "Warehousing Cost per Unit",
            "Total COGS",
        ],
        "EUR": [
            f"{exw_cost:,.2f} EUR",
            f"{total_freight_and_logistics:,.2f} EUR",
            f"{packaging_cost:,.2f} EUR",
            f"{warehousing_cost:,.2f} EUR",
            f"{total_cogs:,.2f} EUR",
        ],
        "SAR": [
            f"{exw_cost * conversion_rates['SAR']:,.2f} SAR",
            f"{total_freight_and_logistics * conversion_rates['SAR']:,.2f} SAR",
            f"{packaging_cost * conversion_rates['SAR']:,.2f} SAR",
            f"{warehousing_cost * conversion_rates['SAR']:,.2f} SAR",
            f"{total_cogs * conversion_rates['SAR']:,.2f} SAR",
        ],
        "AED": [
            f"{exw_cost * conversion_rates['AED']:,.2f} AED",
            f"{total_freight_and_logistics * conversion_rates['AED']:,.2f} AED",
            f"{packaging_cost * conversion_rates['AED']:,.2f} AED",
            f"{warehousing_cost * conversion_rates['AED']:,.2f} AED",
            f"{total_cogs * conversion_rates['AED']:,.2f} AED",
        ],
    }

    gross_profit_data = {
        "Metric": [
            "Gross Profit (Direct Revenue only)",
            "Gross Margin (Direct Revenue only)",
            "Gross Profit (Direct + Revenue Share)",
            "Gross Margin (Direct + Revenue Share)",
        ],
        "EUR": [
            f"{gross_profit_direct:,.2f} EUR",
            f"{gross_margin_direct:.2f}%",
            f"{gross_profit_total:,.2f} EUR",
            f"{gross_margin_total:.2f}%",
        ],
        "SAR": [
            f"{gross_profit_direct * conversion_rates['SAR']:,.2f} SAR",
            "-",
            f"{gross_profit_total * conversion_rates['SAR']:,.2f} SAR",
            "-",
        ],
        "AED": [
            f"{gross_profit_direct * conversion_rates['AED']:,.2f} AED",
            "-",
            f"{gross_profit_total * conversion_rates['AED']:,.2f} AED",
            "-",
        ],
    }

    operating_expenses_data = {
        "Metric": [
            "Salaries",
            "Rental",
            "Utilities",
            "Sales Tax",
            "Admin",
            "Licences",
            "Depreciation",
            "Total Operating Expenses",
        ],
        "AED": [
            f"{st.session_state.tab1_vars['salaries_aed']:,.2f} AED",
            f"{st.session_state.tab1_vars['rental_aed']:,.2f} AED",
            f"{st.session_state.tab1_vars['utilities_aed']:,.2f} AED",
            f"{st.session_state.tab1_vars['sales_tax_aed']:,.2f} AED",
            f"{st.session_state.tab1_vars['admin_aed']:,.2f} AED",
            f"{st.session_state.tab1_vars['licences_aed']:,.2f} AED",
            f"{st.session_state.tab1_vars['depreciation_aed']:,.2f} AED",
            f"{operating_expenses_aed:,.2f} AED",
        ],
        "EUR": [
            f"{st.session_state.tab1_vars['salaries_aed'] / conversion_rates['AED']:,.2f} EUR",
            f"{st.session_state.tab1_vars['rental_aed'] / conversion_rates['AED']:,.2f} EUR",
            f"{st.session_state.tab1_vars['utilities_aed'] / conversion_rates['AED']:,.2f} EUR",
            f"{st.session_state.tab1_vars['sales_tax_aed'] / conversion_rates['AED']:,.2f} EUR",
            f"{st.session_state.tab1_vars['admin_aed'] / conversion_rates['AED']:,.2f} EUR",
            f"{st.session_state.tab1_vars['licences_aed'] / conversion_rates['AED']:,.2f} EUR",
            f"{st.session_state.tab1_vars['depreciation_aed'] / conversion_rates['AED']:,.2f} EUR",
            f"{operating_expenses_eur:,.2f} EUR",
        ],
        "SAR": [
            f"{st.session_state.tab1_vars['salaries_aed'] / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
            f"{st.session_state.tab1_vars['rental_aed'] / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
            f"{st.session_state.tab1_vars['utilities_aed'] / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
            f"{st.session_state.tab1_vars['sales_tax_aed'] / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
            f"{st.session_state.tab1_vars['admin_aed'] / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
            f"{st.session_state.tab1_vars['licences_aed'] / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
            f"{st.session_state.tab1_vars['depreciation_aed'] / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
            f"{operating_expenses_sar:,.2f} SAR",
        ],
    }

    net_profit_data = {
        "Metric": [
            "Net Profit (Direct Revenue only)",
            "Net Profit Margin (Direct Revenue only)",
            "Net Profit (Direct + Revenue Share)",
            "Net Profit Margin (Direct + Revenue Share)",
        ],
        "EUR": [
            f"{net_profit_direct:,.2f} EUR",
            f"{net_profit_margin_direct:.2f}%",
            f"{net_profit_total:,.2f} EUR",
            f"{net_profit_margin_total:.2f}%",
        ],
        "SAR": [
            f"{net_profit_direct * conversion_rates['SAR']:,.2f} SAR",
            "-",
            f"{net_profit_total * conversion_rates['SAR']:,.2f} SAR",
            "-",
        ],
        "AED": [
            f"{net_profit_direct * conversion_rates['AED']:,.2f} AED",
            "-",
            f"{net_profit_total * conversion_rates['AED']:,.2f} AED",
            "-",
        ],
    }

    # Save to Excel
    output_buffer = io.BytesIO()
    with pd.ExcelWriter(output_buffer, engine="xlsxwriter") as writer:
        pd.DataFrame(revenue_data).to_excel(writer, index=False, sheet_name="Revenue")
        pd.DataFrame(cogs_data).to_excel(writer, index=False, sheet_name="COGS")
        pd.DataFrame(gross_profit_data).to_excel(writer, index=False, sheet_name="Gross Profit")
        pd.DataFrame(operating_expenses_data).to_excel(writer, index=False, sheet_name="Operating Expenses")
        pd.DataFrame(net_profit_data).to_excel(writer, index=False, sheet_name="Net Profit")
        writer.close()  # Ensure the writer is closed
    output_buffer.seek(0)  # Reset buffer position

    # Move the Tab 1 download button inside tab1
    st.download_button(
        label="Download Tab 1 Results as Excel",
        data=output_buffer.getvalue(),
        file_name="tab1_analysis_results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    # Create PDF report
    def create_pdf(revenue_data, cogs_data, gross_profit_data, operating_expenses_data, net_profit_data):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Create custom style for main header
        main_header_style = styles['Heading1'].clone('MainHeader')
        main_header_style.textColor = colors.HexColor('#000080')
        main_header_style.alignment = 1
        main_header_style.spaceAfter = 20
        main_header_style.fontSize = 16
        
        # Add main header
        elements.append(Paragraph("P&L Globlex LLC-FZ", main_header_style))
        
        # Helper function to create formatted tables
        def create_table(data, title):
            # Smaller heading style
            heading_style = styles['Heading3'].clone('TableHeading')
            heading_style.fontSize = 10
            heading_style.spaceAfter = 4
            
            elements.append(Paragraph(title, heading_style))
            
            # Convert dictionary to list of lists for the table
            table_data = [list(data.keys())]  # Headers
            for i in range(len(list(data.values())[0])):
                row = [data[col][i] for col in data.keys()]
                table_data.append(row)
            
            # Calculate column widths based on content
            available_width = 500  # Approximate available width in points
            col_widths = [available_width * x for x in [0.4, 0.2, 0.2, 0.2]]  # 40% for first column, 20% for others
            
            table = Table(table_data, colWidths=col_widths, repeatRows=1)
            table.setStyle(TableStyle([
                # Header style
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#000080')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 7),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
                # Data rows style
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 8))

        # Create all tables in sequence
        create_table(revenue_data, "Revenue and Selling Price")
        create_table(cogs_data, "Cost of Goods Sold (COGS)")
        create_table(gross_profit_data, "Gross Profit")
        create_table(operating_expenses_data, "Operating Expenses")
        create_table(net_profit_data, "Net Profit")

        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer

    # Add PDF download button
    pdf_buffer = create_pdf(revenue_data, cogs_data, gross_profit_data, operating_expenses_data, net_profit_data)
    
    st.download_button(
        label="Download Tab 1 Results as PDF",
        data=pdf_buffer,
        file_name="tab1_analysis_results.pdf",
        mime="application/pdf",
    )




# In[ ]:


with tab2:  # Batch Product Analysis tab
    st.header("Batch Product Analysis")

    # Add a state variable to store current total if it doesn't exist
    if 'current_total_units' not in st.session_state:
        st.session_state.current_total_units = 0

    # Add total units display at the top
    st.write("### Current Total Units:", st.session_state.current_total_units)

    # Inputs for tab-specific configurations
    col1, col2 = st.columns(2)
    with col1:
        markup_percentage_tab2 = st.number_input("Markup Percentage (%)", value=21.5, format="%.2f", key="tab2_markup")
        revenue_share_percentage_tab2 = st.number_input("Revenue Share Percentage (%)", value=10.0, format="%.2f", key="tab2_revenue_share")
        freight_cost_tab2 = st.number_input("Freight Cost (EUR)", value=2850.0, format="%.2f", key="tab2_freight_cost")
    with col2:
        packaging_cost_tab2 = st.number_input("Packaging and Printing Cost per Unit (EUR)", value=0.0, format="%.2f", key="tab2_packaging_cost")
        warehousing_cost_tab2 = st.number_input("Warehousing Cost per Unit (EUR)", value=0.0, format="%.2f", key="tab2_warehousing_cost")
        fob_cost_tab2 = st.number_input("FOB Cost (EUR)", value=1100.0, format="%.2f", key="tab2_fob_cost")

    # Operating Expenses Inputs
    st.subheader("Operating Expenses (in AED)")
    salaries_tab2 = st.number_input("Salaries (AED)", value=0.0, format="%.2f", key="tab2_salaries")
    rental_tab2 = st.number_input("Rental (AED)", value=0.0, format="%.2f", key="tab2_rental")
    utilities_tab2 = st.number_input("Utilities (AED)", value=0.0, format="%.2f", key="tab2_utilities")
    sales_tax_tab2 = st.number_input("Sales Tax (AED)", value=0.0, format="%.2f", key="tab2_sales_tax")
    admin_tab2 = st.number_input("Admin (AED)", value=0.0, format="%.2f", key="tab2_admin")
    licences_tab2 = st.number_input("Licences (AED)", value=0.0, format="%.2f", key="tab2_licences")
    depreciation_tab2 = st.number_input("Depreciation (AED)", value=0.0, format="%.2f", key="tab2_depreciation")

    # File uploader
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

    # Conversion rates
    conversion_rates = {"SAR": 4.11, "AED": 3.91}

    if uploaded_file is not None:
        # Read the uploaded Excel file
        data = pd.read_excel(uploaded_file, usecols=[0, 1, 2], header=None)
        data.columns = ["Product Name", "EXW Cost", "Units"]

        # Convert columns to numeric where applicable
        data["EXW Cost"] = pd.to_numeric(data["EXW Cost"], errors="coerce")
        data["Units"] = pd.to_numeric(data["Units"], errors="coerce")

        # Drop rows with invalid EXW costs
        data = data.dropna(subset=["EXW Cost"])

        # Display editable input fields for "Units" with side-by-side layout
        st.write("### Adjust Product Units")
        adjusted_units = []
        for index, row in data.iterrows():
            col1, col2 = st.columns([4, 1])  # Define layout: Product name wider, Units smaller
            with col1:
                st.write(row["Product Name"])
            with col2:
                new_units = st.number_input(
                    "",
                    min_value=0,
                    value=int(row["Units"] if not pd.isna(row["Units"]) else 0),
                    step=1,
                    key=f"units_{index}",
                    label_visibility="collapsed",
                )
                adjusted_units.append(new_units)

        # Update the DataFrame with user inputs
        data["Units"] = adjusted_units

        # Filter out products with zero units
        data = data[data["Units"] > 0]
        total_non_zero_units = data["Units"].sum()

        # FOB and Freight Cost Distribution
        cost_per_unit = (freight_cost_tab2 + fob_cost_tab2) / total_non_zero_units if total_non_zero_units > 0 else 0

        # Process each product
        results = []

        for _, row in data.iterrows():
            product_name = row["Product Name"]
            exw_cost = row["EXW Cost"]
            units = row["Units"]

            # Calculations
            base_price = exw_cost + cost_per_unit + packaging_cost_tab2 + warehousing_cost_tab2
            selling_price = base_price + (base_price * markup_percentage_tab2 / 100)
            revenue_share_per_unit = selling_price * (revenue_share_percentage_tab2 / 100)
            direct_revenue = selling_price * units
            total_revenue_share = revenue_share_per_unit * units
            total_revenue = direct_revenue + total_revenue_share

            # COGS
            total_cogs = (
                (exw_cost * units)
                + (cost_per_unit * units)
                + (packaging_cost_tab2 * units)
                + (warehousing_cost_tab2 * units)
            )

            # Gross Profit
            gross_profit = total_revenue - total_cogs

            # Operating Expenses in EUR
            total_operating_expenses_aed = (
                (salaries_tab2 + rental_tab2 + utilities_tab2) * 12
                + sales_tax_tab2
                + admin_tab2
                + licences_tab2
                + depreciation_tab2
            )
            total_operating_expenses_eur = total_operating_expenses_aed / conversion_rates["AED"]

            # Net Profit
            net_profit = gross_profit - total_operating_expenses_eur

            # Append results for each product
            results.append({
                "Product Name": product_name,
                "Number of Units": units,
                "Selling Price per Unit (EUR)": selling_price,
                "Selling Price per Unit (SAR)": selling_price * conversion_rates["SAR"],
                "Selling Price per Unit (AED)": selling_price * conversion_rates["AED"],
                "Total Revenue (EUR)": total_revenue,
                "Total Revenue (SAR)": total_revenue * conversion_rates["SAR"],
                "Total Revenue (AED)": total_revenue * conversion_rates["AED"],
                "Total COGS (EUR)": total_cogs,
                "Total COGS (SAR)": total_cogs * conversion_rates["SAR"],
                "Total COGS (AED)": total_cogs * conversion_rates["AED"],
                "Gross Profit (EUR)": gross_profit,
                "Gross Profit (SAR)": gross_profit * conversion_rates["SAR"],
                "Gross Profit (AED)": gross_profit * conversion_rates["AED"],
                "Net Profit (EUR)": net_profit,
                "Net Profit (SAR)": net_profit * conversion_rates["SAR"],
                "Net Profit (AED)": net_profit * conversion_rates["AED"],
            })

        # Convert results to DataFrame
        results_df = pd.DataFrame(results)

        # Add a total row
        total_row = {col: results_df[col].sum() if pd.api.types.is_numeric_dtype(results_df[col]) else "Total" for col in results_df.columns}
        results_df = pd.concat([results_df, pd.DataFrame([total_row])], ignore_index=True)

        # Display results
        st.write("### Batch Analysis Results")
        st.dataframe(results_df)

        # Export results to Excel
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            results_df.to_excel(writer, index=False)
            writer.close()
        buffer.seek(0)

        st.download_button(
            label="Download Results as Excel",
            data=buffer,
            file_name="batch_analysis_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )


# In[ ]:


# Create tabs

# Assuming the data is available in the `results_df` DataFrame after analysis
with tab3:  # Dashboard Tab
    st.header("Dashboard")

    # Ensure the data exists before proceeding
    if "results_df" in locals() or "results_df" in globals():
        # Remove the total row if present to avoid skewing the visuals
        dashboard_data = results_df[results_df["Product Name"] != "Total"]

        # Display Summary Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_revenue = dashboard_data["Total Revenue (EUR)"].sum()
            st.metric("Total Revenue (EUR)", f"{total_revenue:,.2f}")
        with col2:
            total_units = dashboard_data["Number of Units"].sum()
            st.metric("Total Units Sold", f"{int(total_units)}")
        with col3:
            average_profit = dashboard_data["Net Profit (EUR)"].mean()
            st.metric("Average Net Profit (EUR)", f"{average_profit:,.2f}")
        with col4:
            gross_profit_margin = (dashboard_data["Gross Profit (EUR)"].sum() / total_revenue) * 100
            st.metric("Gross Profit Margin (%)", f"{gross_profit_margin:.2f}%")

        # Revenue by Product
        st.subheader("Revenue by Product")
        fig_revenue = px.bar(
            dashboard_data,
            x="Product Name",
            y="Total Revenue (EUR)",
            title="Revenue by Product",
            labels={"Total Revenue (EUR)": "Revenue (EUR)", "Product Name": "Product"},
        )
        st.plotly_chart(fig_revenue, use_container_width=True)

        # Profit by Product
        st.subheader("Net Profit by Product")
        fig_profit = px.bar(
            dashboard_data,
            x="Product Name",
            y="Net Profit (EUR)",
            title="Net Profit by Product",
            labels={"Net Profit (EUR)": "Net Profit (EUR)", "Product Name": "Product"},
        )
        st.plotly_chart(fig_profit, use_container_width=True)

        # Unit Distribution
        st.subheader("Units Sold Distribution")
        fig_units = px.pie(
            dashboard_data,
            names="Product Name",
            values="Number of Units",
            title="Units Sold by Product",
        )
        st.plotly_chart(fig_units, use_container_width=True)

        # Revenue vs. COGS
        st.subheader("Revenue vs. COGS (EUR)")
        fig_revenue_cogs = px.line(
            dashboard_data,
            x="Product Name",
            y=["Total Revenue (EUR)", "Total COGS (EUR)"],
            title="Revenue vs. COGS",
            labels={"value": "Amount (EUR)", "Product Name": "Product"},
        )
        st.plotly_chart(fig_revenue_cogs, use_container_width=True)
    else:
        st.warning("No data available. Please perform the batch analysis first.")

