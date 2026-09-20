import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("📊 Sales Dashboard")
st.write("Automated Excel Sales Analysis")


# =========================================================
# EXCEL UPLOAD
# =========================================================

uploaded_file = st.file_uploader(
    "Upload your Excel file",
    type=["xlsx", "xls"]
)


# =========================================================
# MAIN APP
# =========================================================

if uploaded_file is not None:

    try:

        # -------------------------------------------------
        # READ EXCEL
        # -------------------------------------------------

        df = pd.read_excel(uploaded_file)

        # Clean column names
        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        st.success("✅ Excel file loaded successfully!")

        # -------------------------------------------------
        # SHOW EXCEL COLUMNS
        # -------------------------------------------------

        with st.expander("📋 View Excel Columns"):

            st.write(list(df.columns))

        # -------------------------------------------------
        # COLUMN DETECTION
        # -------------------------------------------------

        def find_column(possible_names):

            for name in possible_names:

                for actual_column in df.columns:

                    if actual_column.lower().strip() == name.lower().strip():

                        return actual_column

            return None


        # Detect columns from your Excel

        region_col = find_column([
            "Region",
            "region"
        ])

        product_col = find_column([
            "Product",
            "product"
        ])

        quantity_col = find_column([
            "Quantity",
            "quantity"
        ])

        unit_price_col = find_column([
            "UnitPrice",
            "Unit Price",
            "unitprice"
        ])

        total_price_col = find_column([
            "TotalPrice",
            "Total Price",
            "Sales",
            "Sales_USD",
            "Revenue"
        ])

        payment_col = find_column([
            "PaymentMethod",
            "Payment Method"
        ])

        category_col = find_column([
            "ProductCategory",
            "Product Category",
            "Category"
        ])

        customer_col = find_column([
            "CustomerType",
            "Customer Type"
        ])

        store_col = find_column([
            "StoreLocation",
            "Store Location"
        ])

        salesperson_col = find_column([
            "Salesperson",
            "Sales Person"
        ])

        date_col = find_column([
            "Date",
            "OrderDate",
            "Order Date"
        ])


        # =================================================
        # CREATE TOTAL SALES IF NOT AVAILABLE
        # =================================================

        if total_price_col is None:

            if quantity_col is not None and unit_price_col is not None:

                df["_CalculatedSales"] = (
                    pd.to_numeric(
                        df[quantity_col],
                        errors="coerce"
                    ).fillna(0)
                    *
                    pd.to_numeric(
                        df[unit_price_col],
                        errors="coerce"
                    ).fillna(0)
                )

                total_price_col = "_CalculatedSales"


        # =================================================
        # CONVERT NUMERIC COLUMNS
        # =================================================

        if quantity_col is not None:

            df[quantity_col] = pd.to_numeric(
                df[quantity_col],
                errors="coerce"
            ).fillna(0)


        if total_price_col is not None:

            df[total_price_col] = pd.to_numeric(
                df[total_price_col],
                errors="coerce"
            ).fillna(0)


        # =================================================
        # FILTERS
        # =================================================

        st.header("🎛️ Dashboard Filters")

        filter1, filter2, filter3 = st.columns(3)


        # -------------------------------------------------
        # REGION FILTER
        # -------------------------------------------------

        if region_col is not None:

            with filter1:

                region_list = (
                    df[region_col]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                region_options = ["All"] + sorted(region_list)

                selected_region = st.selectbox(
                    "🌎 Region",
                    region_options
                )

        else:

            selected_region = "All"


        # -------------------------------------------------
        # PRODUCT FILTER
        # -------------------------------------------------

        if product_col is not None:

            with filter2:

                product_list = (
                    df[product_col]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                product_options = ["All"] + sorted(product_list)

                selected_product = st.selectbox(
                    "🛍️ Product",
                    product_options
                )

        else:

            selected_product = "All"


        # -------------------------------------------------
        # PAYMENT FILTER
        # -------------------------------------------------

        if payment_col is not None:

            with filter3:

                payment_list = (
                    df[payment_col]
                    .dropna()
                    .astype(str)
                    .unique()
                    .tolist()
                )

                payment_options = ["All"] + sorted(payment_list)

                selected_payment = st.selectbox(
                    "💳 Payment Method",
                    payment_options
                )

        else:

            selected_payment = "All"


        # =================================================
        # APPLY FILTERS
        # =================================================

        filtered_df = df.copy()


        if (
            region_col is not None
            and selected_region != "All"
        ):

            filtered_df = filtered_df[
                filtered_df[region_col]
                .astype(str)
                == selected_region
            ]


        if (
            product_col is not None
            and selected_product != "All"
        ):

            filtered_df = filtered_df[
                filtered_df[product_col]
                .astype(str)
                == selected_product
            ]


        if (
            payment_col is not None
            and selected_payment != "All"
        ):

            filtered_df = filtered_df[
                filtered_df[payment_col]
                .astype(str)
                == selected_payment
            ]


        # =================================================
        # KPIs
        # =================================================

        st.header("📈 Key Performance Indicators")


        if total_price_col is not None:

            total_sales = filtered_df[
                total_price_col
            ].sum()

        else:

            total_sales = 0


        if quantity_col is not None:

            quantity_sold = filtered_df[
                quantity_col
            ].sum()

        else:

            quantity_sold = 0


        total_orders = len(filtered_df)


        if total_orders > 0:

            avg_order_value = (
                total_sales / total_orders
            )

        else:

            avg_order_value = 0


        kpi1, kpi2, kpi3, kpi4 = st.columns(4)


        with kpi1:

            st.metric(
                "💰 Total Sales",
                f"${total_sales:,.2f}"
            )


        with kpi2:

            st.metric(
                "🧾 Total Orders",
                f"{total_orders:,}"
            )


        with kpi3:

            st.metric(
                "📦 Quantity Sold",
                f"{quantity_sold:,.0f}"
            )


        with kpi4:

            st.metric(
                "💵 Avg Order Value",
                f"${avg_order_value:,.2f}"
            )


        # =================================================
        # SALES BY REGION
        # =================================================

        if (
            region_col is not None
            and total_price_col is not None
        ):

            st.header("🌎 Sales by Region")

            region_sales = (
                filtered_df
                .groupby(region_col)[total_price_col]
                .sum()
                .reset_index()
                .sort_values(
                    total_price_col,
                    ascending=False
                )
            )


            fig_region = px.bar(
                region_sales,
                x=region_col,
                y=total_price_col,
                title="Total Sales by Region",
                text_auto=".2s"
            )


            fig_region.update_layout(
                xaxis_title="Region",
                yaxis_title="Sales"
            )


            st.plotly_chart(
                fig_region,
                use_container_width=True
            )


        # =================================================
        # SALES BY PRODUCT
        # =================================================

        if (
            product_col is not None
            and total_price_col is not None
        ):

            st.header("🛍️ Sales by Product")

            product_sales = (
                filtered_df
                .groupby(product_col)[total_price_col]
                .sum()
                .reset_index()
                .sort_values(
                    total_price_col,
                    ascending=False
                )
            )


            fig_product = px.bar(
                product_sales,
                x=product_col,
                y=total_price_col,
                title="Total Sales by Product",
                text_auto=".2s"
            )


            fig_product.update_layout(
                xaxis_title="Product",
                yaxis_title="Sales"
            )


            st.plotly_chart(
                fig_product,
                use_container_width=True
            )


        # =================================================
        # SALES BY PRODUCT CATEGORY
        # =================================================

        if (
            category_col is not None
            and total_price_col is not None
        ):

            st.header("🏷️ Sales by Product Category")

            category_sales = (
                filtered_df
                .groupby(category_col)[total_price_col]
                .sum()
                .reset_index()
                .sort_values(
                    total_price_col,
                    ascending=False
                )
            )


            fig_category = px.bar(
                category_sales,
                x=category_col,
                y=total_price_col,
                title="Total Sales by Product Category",
                text_auto=".2s"
            )


            fig_category.update_layout(
                xaxis_title="Category",
                yaxis_title="Sales"
            )


            st.plotly_chart(
                fig_category,
                use_container_width=True
            )


        # =================================================
        # PAYMENT METHOD
        # =================================================

        if (
            payment_col is not None
            and total_price_col is not None
        ):

            st.header("💳 Sales by Payment Method")

            payment_sales = (
                filtered_df
                .groupby(payment_col)[total_price_col]
                .sum()
                .reset_index()
                .sort_values(
                    total_price_col,
                    ascending=False
                )
            )


            fig_payment = px.pie(
                payment_sales,
                names=payment_col,
                values=total_price_col,
                title="Sales by Payment Method"
            )


            st.plotly_chart(
                fig_payment,
                use_container_width=True
            )


        # =================================================
        # CUSTOMER TYPE
        # =================================================

        if (
            customer_col is not None
            and total_price_col is not None
        ):

            st.header("👥 Sales by Customer Type")

            customer_sales = (
                filtered_df
                .groupby(customer_col)[total_price_col]
                .sum()
                .reset_index()
                .sort_values(
                    total_price_col,
                    ascending=False
                )
            )


            fig_customer = px.bar(
                customer_sales,
                x=customer_col,
                y=total_price_col,
                title="Sales by Customer Type",
                text_auto=".2s"
            )


            st.plotly_chart(
                fig_customer,
                use_container_width=True
            )


        # =================================================
        # STORE LOCATION
        # =================================================

        if (
            store_col is not None
            and total_price_col is not None
        ):

            st.header("🏪 Sales by Store Location")

            store_sales = (
                filtered_df
                .groupby(store_col)[total_price_col]
                .sum()
                .reset_index()
                .sort_values(
                    total_price_col,
                    ascending=False
                )
            )


            fig_store = px.bar(
                store_sales,
                x=store_col,
                y=total_price_col,
                title="Sales by Store Location",
                text_auto=".2s"
            )


            st.plotly_chart(
                fig_store,
                use_container_width=True
            )


        # =================================================
        # SALES BY SALESPERSON
        # =================================================

        if (
            salesperson_col is not None
            and total_price_col is not None
        ):

            st.header("👤 Sales by Salesperson")

            salesperson_sales = (
                filtered_df
                .groupby(salesperson_col)[total_price_col]
                .sum()
                .reset_index()
                .sort_values(
                    total_price_col,
                    ascending=False
                )
            )


            fig_salesperson = px.bar(
                salesperson_sales,
                x=salesperson_col,
                y=total_price_col,
                title="Sales by Salesperson",
                text_auto=".2s"
            )


            st.plotly_chart(
                fig_salesperson,
                use_container_width=True
            )


        # =================================================
        # RAW DATA
        # =================================================

        st.header("📋 Detailed Sales Data")

        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=400
        )


        # =================================================
        # DOWNLOAD FILTERED DATA
        # =================================================

        csv_data = filtered_df.to_csv(
            index=False
        ).encode("utf-8")


        st.download_button(
            label="⬇️ Download Filtered Data",
            data=csv_data,
            file_name="filtered_sales_data.csv",
            mime="text/csv"
        )


    except Exception as e:

        st.error("❌ Something went wrong while processing the Excel file.")

        st.exception(e)


else:

    st.info(
        "👆 Upload an Excel file above to generate the dashboard."
    )