#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd

# Title of the application
st.title("Financial Analysis Tool")

# Create tabs at the top for different functionalities
tab1, tab2 = st.tabs(["Single Product Model", "Batch Product Analysis"])

# Tab 1: Single Product Model
with tab1:
    st.header("Single Product Model")

    # Sidebar for inputs
    with st.sidebar:
        st.header("Input Parameters")

        # Conversion rates for SAR and AED
        conversion_rates = {
            "SAR": 3.75,
            "AED": 3.67
        }

        # COGS inputs
        st.subheader("Cost Parameters")
        exw_cost = st.number_input("EXW Cost per Unit (EUR)", value=0.64, format="%.2f")
        fob_cost = st.number_input("FOB Cost (Total, EUR)", value=1100.0, format="%.2f")
        freight_cost = st.number_input("Freight Cost (Total, EUR)", value=2850.0, format="%.2f")
        packaging_cost = st.number_input("Packaging and Printing Cost per Unit (EUR)", value=0.0, format="%.2f")
        warehousing_cost = st.number_input("Warehousing Cost per Unit (EUR)", value=0.0, format="%.2f")

        # Markup percentage
        markup_percentage = st.number_input("Markup Percentage (%)", value=21.5, format="%.2f")

        # Revenue Share Percentage
        revenue_share_percentage = st.number_input("Revenue Share Percentage (%)", value=10.0, format="%.2f")

        # Operating Expenses (in AED)
        st.subheader("Operating Expenses (in AED)")
        salaries_aed = st.number_input("Salaries (AED)", value=0.0, format="%.2f")
        rental_aed = st.number_input("Rental (AED)", value=0.0, format="%.2f")
        utilities_aed = st.number_input("Utilities (AED)", value=0.0, format="%.2f")
        sales_tax_aed = st.number_input("Sales Tax (AED)", value=0.0, format="%.2f")
        admin_aed = st.number_input("Admin (AED)", value=0.0, format="%.2f")
        licences_aed = st.number_input("Licences (AED)", value=0.0, format="%.2f")
        depreciation_aed = st.number_input("Depreciation (AED)", value=0.0, format="%.2f")

        # Calculate Sales Price per Unit
        projected_units_sold = st.number_input("Projected Units Sold", value=26250)
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
        (salaries_aed * 12) + (rental_aed * 12) + (utilities_aed * 12) + sales_tax_aed + admin_aed + licences_aed + depreciation_aed
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
            f"{salaries_aed:,.2f} AED",
            f"{rental_aed:,.2f} AED",
            f"{utilities_aed:,.2f} AED",
            f"{sales_tax_aed:,.2f} AED",
            f"{admin_aed:,.2f} AED",
            f"{licences_aed:,.2f} AED",
            f"{depreciation_aed:,.2f} AED",
            f"{operating_expenses_aed:,.2f} AED"
        ],
        "EUR": [
            f"{salaries_aed / conversion_rates['AED']:,.2f} EUR",
            f"{rental_aed / conversion_rates['AED']:,.2f} EUR",
            f"{utilities_aed / conversion_rates['AED']:,.2f} EUR",
            f"{sales_tax_aed / conversion_rates['AED']:,.2f} EUR",
            f"{admin_aed / conversion_rates['AED']:,.2f} EUR",
            f"{licences_aed / conversion_rates['AED']:,.2f} EUR",
            f"{depreciation_aed / conversion_rates['AED']:,.2f} EUR",
            f"{operating_expenses_eur:,.2f} EUR"
        ],
        "SAR": [
            f"{salaries_aed / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
            f"{rental_aed / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
            f"{utilities_aed / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
            f"{sales_tax_aed / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
            f"{admin_aed / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
            f"{licences_aed / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
            f"{depreciation_aed / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
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
import io
import pandas as pd

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
        f"{salaries_aed:,.2f} AED",
        f"{rental_aed:,.2f} AED",
        f"{utilities_aed:,.2f} AED",
        f"{sales_tax_aed:,.2f} AED",
        f"{admin_aed:,.2f} AED",
        f"{licences_aed:,.2f} AED",
        f"{depreciation_aed:,.2f} AED",
        f"{operating_expenses_aed:,.2f} AED",
    ],
    "EUR": [
        f"{salaries_aed / conversion_rates['AED']:,.2f} EUR",
        f"{rental_aed / conversion_rates['AED']:,.2f} EUR",
        f"{utilities_aed / conversion_rates['AED']:,.2f} EUR",
        f"{sales_tax_aed / conversion_rates['AED']:,.2f} EUR",
        f"{admin_aed / conversion_rates['AED']:,.2f} EUR",
        f"{licences_aed / conversion_rates['AED']:,.2f} EUR",
        f"{depreciation_aed / conversion_rates['AED']:,.2f} EUR",
        f"{operating_expenses_eur:,.2f} EUR",
    ],
    "SAR": [
        f"{salaries_aed / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
        f"{rental_aed / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
        f"{utilities_aed / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
        f"{sales_tax_aed / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
        f"{admin_aed / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
        f"{licences_aed / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
        f"{depreciation_aed / (conversion_rates['AED'] / conversion_rates['SAR']):,.2f} SAR",
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

# Add download button
st.download_button(
    label="Download Tab 1 Results as Excel",
    data=output_buffer.getvalue(),
    file_name="tab1_analysis_results.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)



# Tab 2: Batch Product Analysis
# Tab 2: Batch Product Analysis
with tab2:
    st.header("Batch Product Analysis")

    # File uploader
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

    if uploaded_file is not None:
        # Read the uploaded Excel file
        data = pd.read_excel(uploaded_file, usecols=[0, 1, 2], header=None)
        data.columns = ["Product Name", "EXW Cost", "Units"]

        # Convert columns to numeric where applicable
        data["EXW Cost"] = pd.to_numeric(data["EXW Cost"], errors="coerce")
        data["Units"] = pd.to_numeric(data["Units"], errors="coerce")

        # Drop rows with invalid data
        data = data.dropna(subset=["EXW Cost", "Units"])

        # Input for global parameters with unique keys
        markup_percentage = st.number_input("Markup Percentage (%)", value=21.5, format="%.2f", key="batch_markup")
        revenue_share_percentage = st.number_input("Revenue Share Percentage (%)", value=10.0, format="%.2f", key="batch_revenue_share")
        freight_cost = st.number_input("Freight Cost (Total, EUR)", value=2850.0, format="%.2f", key="batch_freight_cost")
        fob_cost = st.number_input("FOB Cost (Total, EUR)", value=1100.0, format="%.2f", key="batch_fob_cost")
        packaging_cost = st.number_input("Packaging and Printing Cost per Unit (EUR)", value=0.0, format="%.2f", key="batch_packaging_cost")
        warehousing_cost = st.number_input("Warehousing Cost per Unit (EUR)", value=0.0, format="%.2f", key="batch_warehousing_cost")
        salaries_aed = st.number_input("Salaries (AED)", value=0.0, format="%.2f", key="batch_salaries")
        rental_aed = st.number_input("Rental (AED)", value=0.0, format="%.2f", key="batch_rental")
        utilities_aed = st.number_input("Utilities (AED)", value=0.0, format="%.2f", key="batch_utilities")
        sales_tax_aed = st.number_input("Sales Tax (AED)", value=0.0, format="%.2f", key="batch_sales_tax")
        admin_aed = st.number_input("Admin (AED)", value=0.0, format="%.2f", key="batch_admin")
        licences_aed = st.number_input("Licences (AED)", value=0.0, format="%.2f", key="batch_licences")
        depreciation_aed = st.number_input("Depreciation (AED)", value=0.0, format="%.2f", key="batch_depreciation")

        # Operating expenses
        operating_expenses_aed = (
            (salaries_aed * 12)
            + (rental_aed * 12)
            + (utilities_aed * 12)
            + sales_tax_aed
            + admin_aed
            + licences_aed
            + depreciation_aed
        )
        operating_expenses_eur = operating_expenses_aed / conversion_rates["AED"]
        operating_expenses_sar = operating_expenses_aed / (conversion_rates["AED"] / conversion_rates["SAR"])

        # Process each product
        results = []

        for _, row in data.iterrows():
            product_name = row["Product Name"]
            exw_cost = row["EXW Cost"]
            units = row["Units"]

            # Calculations
            base_price = exw_cost + ((freight_cost + fob_cost) / units) + (packaging_cost + warehousing_cost)
            selling_price = base_price + (base_price * markup_percentage / 100)
            revenue_share_per_unit = selling_price * (revenue_share_percentage / 100)
            direct_revenue = selling_price * units
            total_revenue_share = revenue_share_per_unit * units
            total_revenue = direct_revenue + total_revenue_share

            # COGS
            total_freight_and_logistics = freight_cost + fob_cost
            total_cogs = (
                (exw_cost * units)
                + total_freight_and_logistics
                + (packaging_cost * units)
                + (warehousing_cost * units)
            )

            # Gross Profit
            gross_profit_direct = direct_revenue - total_cogs
            gross_profit_total = total_revenue - total_cogs

            # Net Profit
            net_profit_direct = gross_profit_direct - operating_expenses_eur
            net_profit_total = gross_profit_total - operating_expenses_eur

            # Append results for each product
            results.append({
                "Product Name": product_name,
                # Revenue Section
                "Selling Price per Unit (EUR)": selling_price,
                "Selling Price per Unit (SAR)": selling_price * conversion_rates["SAR"],
                "Selling Price per Unit (AED)": selling_price * conversion_rates["AED"],
                "Direct Revenue (EUR)": direct_revenue,
                "Direct Revenue (SAR)": direct_revenue * conversion_rates["SAR"],
                "Direct Revenue (AED)": direct_revenue * conversion_rates["AED"],
                "Revenue Share (EUR)": total_revenue_share,
                "Revenue Share (SAR)": total_revenue_share * conversion_rates["SAR"],
                "Revenue Share (AED)": total_revenue_share * conversion_rates["AED"],
                "Total Revenue (EUR)": total_revenue,
                "Total Revenue (SAR)": total_revenue * conversion_rates["SAR"],
                "Total Revenue (AED)": total_revenue * conversion_rates["AED"],
                # COGS Section
                "Total COGS (EUR)": total_cogs,
                "Total COGS (SAR)": total_cogs * conversion_rates["SAR"],
                "Total COGS (AED)": total_cogs * conversion_rates["AED"],
                # Gross Profit Section
                "Gross Profit (Direct Revenue only, EUR)": gross_profit_direct,
                "Gross Profit (Direct Revenue only, SAR)": gross_profit_direct * conversion_rates["SAR"],
                "Gross Profit (Direct Revenue only, AED)": gross_profit_direct * conversion_rates["AED"],
                "Gross Profit (Direct + Revenue Share, EUR)": gross_profit_total,
                "Gross Profit (Direct + Revenue Share, SAR)": gross_profit_total * conversion_rates["SAR"],
                "Gross Profit (Direct + Revenue Share, AED)": gross_profit_total * conversion_rates["AED"],
                # Operating Expenses Section
                "Operating Expenses (EUR)": operating_expenses_eur,
                "Operating Expenses (SAR)": operating_expenses_sar,
                "Operating Expenses (AED)": operating_expenses_aed,
                # Net Profit Section
                "Net Profit (Direct Revenue only, EUR)": net_profit_direct,
                "Net Profit (Direct Revenue only, SAR)": net_profit_direct * conversion_rates["SAR"],
                "Net Profit (Direct Revenue only, AED)": net_profit_direct * conversion_rates["AED"],
                "Net Profit (Direct + Revenue Share, EUR)": net_profit_total,
                "Net Profit (Direct + Revenue Share, SAR)": net_profit_total * conversion_rates["SAR"],
                "Net Profit (Direct + Revenue Share, AED)": net_profit_total * conversion_rates["AED"],
            })

        # Convert results to DataFrame
        results_df = pd.DataFrame(results)

        # Display results
        st.write("### Batch Analysis Results")
        st.dataframe(results_df)

        # Export results to Excel
        output_file = "batch_analysis_results.xlsx"
        results_df.to_excel(output_file, index=False)
        st.download_button(
            label="Download Results as Excel",
            data=open(output_file, "rb"),
            file_name="batch_analysis_results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

