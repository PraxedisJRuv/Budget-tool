"""
This section has been mostly vibe-coded. The review of the code and further testing shows
a proppper implementation. The code does requiere some imporvment and minor adjusments as well
as some modularization but it pretty much achives the intent. 
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import List, Dict, Any

from dash_utils import normalize_date_for_api, format_date_series, make_request

# Set page config
st.set_page_config(
    page_title="Budget Manager",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 4px;
        padding: 12px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 4px;
        padding: 12px;
        margin: 10px 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 4px;
        padding: 12px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)


#BUY MANAGEMENT

def page_buys():
    st.title("💳 Buy Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Record Buy", "View Buys", "Update Buy", "Delete Buy"])
    
    # TAB 1: Record Buy (Atomic)
    with tab1:
        st.header("Record New Buy (with Items & Expense)")
        st.info("This will create a buy, add items/products, and create an expense in a single atomic transaction.")
        
        col1, col2 = st.columns(2)
        with col1:
            buy_date = st.date_input("Date", datetime.now())
            buy_local = st.text_input("Location/Store", placeholder="e.g., Supermarket, Pharmacy")
        with col2:
            buy_business_type = st.selectbox("Business Type", 
                ["Grocery", "Electronics", "Clothing", "Health", "Other"], 
                index=0)
            expense_concept = st.text_input("Expense Concept", 
                placeholder="e.g., Weekly groceries")
        
        expense_description = st.text_area("Expense Description (Optional)", 
            placeholder="Additional notes about the expense...")
        
        st.subheader("Items in this Buy")
        st.info("Add all items you purchased in this transaction")
        
        # Dynamic items input
        if "items_list" not in st.session_state:
            st.session_state.items_list = [{"product_name": "", "cost": 0.0, "quantity": 1}]
        
        items_data = []
        for i, item in enumerate(st.session_state.items_list):
            col1, col2, col3, col4 = st.columns([2, 1, 1, 0.5])
            with col1:
                product_name = st.text_input(f"Product Name", 
                    value=item["product_name"], 
                    key=f"product_{i}",
                    placeholder="e.g., Bread")
            with col2:
                cost = st.number_input(f"Cost ($)", 
                    value=item["cost"], 
                    key=f"cost_{i}",
                    min_value=0.0, 
                    step=0.01)
            with col3:
                quantity = st.number_input(f"Qty", 
                    value=item["quantity"], 
                    key=f"qty_{i}",
                    min_value=1, 
                    step=1)
            with col4:
                if st.button("❌", key=f"remove_{i}"):
                    st.session_state.items_list.pop(i)
                    st.rerun()
            
            if product_name and cost > 0:
                items_data.append({
                    "product_name": product_name,
                    "cost": cost,
                    "Quantity": quantity
                })
        
        if st.button("➕ Add Item"):
            st.session_state.items_list.append({"product_name": "", "cost": 0.0, "quantity": 1})
            st.rerun()
        
        # Calculate total
        if items_data:
            total_cost = sum(item["cost"] * item["Quantity"] for item in items_data)
            st.metric("Total Cost", f"${total_cost:.2f}")
        
        if st.button("🛒 Record Buy", type="primary"):
            if not items_data:
                st.error("❌ Please add at least one item")
            elif not expense_concept:
                st.error("❌ Please enter an expense concept")
            else:
                payload = {
                    "date": normalize_date_for_api(buy_date),
                    "local": buy_local if buy_local else None,
                    "business_type": buy_business_type.lower() if buy_business_type else None,
                    "items": items_data,
                    "expense_concept": expense_concept,
                    "expense_description": expense_description if expense_description else None
                }
                
                result = make_request("POST", "/buy/complete", data=payload)
                if result:
                    st.success("✅ Buy recorded successfully!")
                    st.json(result)
                    st.session_state.items_list = [{"product_name": "", "cost": 0.0, "quantity": 1}]
    
    # TAB 2: View Buys
    with tab2:
        st.header("View All Buys")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input("Search by location", placeholder="e.g., Supermarket")
        with col2:
            limit = st.number_input("Results per page", value=20, min_value=1, max_value=100)
        
        params = {"limit": limit}
        if search_term:
            params["search"] = search_term
        
        data = make_request("GET", "/buy", params=params)
        if data and data.get("items"):
            df = pd.DataFrame(data["items"])
            if "date" in df.columns:
                df["date"] = format_date_series(df["date"], include_time=True)
            df = df[["id", "date", "local", "business_type", "cost", "amount_products_type", "ID_expense"]]
            df.columns = ["ID", "Date", "Location", "Type", "Cost ($)", "Items Count", "Expense ID"]
            st.dataframe(df, width="stretch")
            st.caption(f"Total records: {data.get('total', 0)}")
        else:
            st.info("No buys found")
    
    # TAB 3: Update Buy
    with tab3:
        st.header("Update Buy")
        
        buy_id = st.number_input("Buy ID to update", min_value=1, step=1)
        
        col1, col2 = st.columns(2)
        with col1:
            new_date = st.date_input("New Date (optional)", value=None)
            new_local = st.text_input("New Location (optional)", placeholder="Leave empty to keep current")
        with col2:
            new_business_type = st.text_input("New Business Type (optional)", 
                placeholder="Leave empty to keep current")
            new_cost = st.number_input("New Cost (optional)", value=0.0, step=0.01)
        
        if st.button("🔄 Update Buy"):
            update_data = {}
            if new_date:
                update_data["date"] = normalize_date_for_api(new_date)
            if new_local:
                update_data["local"] = new_local
            if new_business_type:
                update_data["business_type"] = new_business_type
            if new_cost > 0:
                update_data["cost"] = new_cost
            
            if update_data:
                result = make_request("PUT", f"/buy/{buy_id}", data=update_data)
                if result:
                    st.success("✅ Buy updated successfully!")
                    st.json(result)
            else:
                st.warning("⚠️ No fields to update")
    
    # TAB 4: Delete Buy
    with tab4:
        st.header("Delete Buy")
        st.warning("⚠️ This action cannot be undone!")
        
        buy_id = st.number_input("Buy ID to delete", min_value=1, step=1)
        
        if st.button("🗑️ Delete Buy", type="secondary"):
            result = make_request("DELETE", f"/buy/{buy_id}")
            if result is not None:
                st.success("✅ Buy deleted successfully!")


#EXPENSE MANAGEMENT
    
def page_expenses():
    st.title("📊 Expense Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Record Expense", "View Expenses", "Update Expense", "Delete Expense"])
    
    # TAB 1: Record Expense
    with tab1:
        st.header("Record New Expense")
        
        col1, col2 = st.columns(2)
        with col1:
            exp_date = st.date_input("Date", datetime.now())
            exp_amount = st.number_input("Amount ($)", min_value=0.0, step=0.01)
        with col2:
            exp_concept = st.text_input("Concept", placeholder="e.g., Office supplies")
        
        exp_description = st.text_area("Description (Optional)", 
            placeholder="Additional details about this expense...")
        
        if st.button("💾 Record Expense", type="primary"):
            if not exp_concept:
                st.error("❌ Please enter a concept")
            elif exp_amount <= 0:
                st.error("❌ Amount must be greater than 0")
            else:
                payload = {
                    "date": normalize_date_for_api(exp_date),
                    "amount": exp_amount,
                    "concept": exp_concept,
                    "description": exp_description if exp_description else None
                }
                
                result = make_request("POST", "/expense", data=payload)
                if result:
                    st.success("✅ Expense recorded successfully!")
                    st.json(result)
    
    # TAB 2: View Expenses
    with tab2:
        st.header("View All Expenses")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input("Search by concept", placeholder="e.g., Groceries")
        with col2:
            limit = st.number_input("Results per page", value=20, min_value=1, max_value=100)
        
        params = {"limit": limit}
        if search_term:
            params["search"] = search_term
        
        data = make_request("GET", "/expense", params=params)
        if data and data.get("items"):
            df = pd.DataFrame(data["items"])
            if "date" in df.columns:
                df["date"] = format_date_series(df["date"])
            df = df[["id", "date", "amount", "concept", "description"]]
            df.columns = ["ID", "Date", "Amount ($)", "Concept", "Description"]
            st.dataframe(df, width="stretch")
            st.caption(f"Total records: {data.get('total', 0)}")
        else:
            st.info("No expenses found")
    
    # TAB 3: Update Expense
    with tab3:
        st.header("Update Expense")
        
        exp_id = st.number_input("Expense ID to update", min_value=1, step=1)
        
        col1, col2 = st.columns(2)
        with col1:
            new_date = st.date_input("New Date (optional)", value=None)
            new_amount = st.number_input("New Amount (optional)", value=0.0, step=0.01)
        with col2:
            new_concept = st.text_input("New Concept (optional)", placeholder="Leave empty to keep current")
        
        new_description = st.text_area("New Description (optional)", 
            placeholder="Leave empty to keep current")
        
        if st.button("🔄 Update Expense"):
            update_data = {}
            if new_date:
                update_data["date"] = normalize_date_for_api(new_date)
            if new_amount > 0:
                update_data["amount"] = new_amount
            if new_concept:
                update_data["concept"] = new_concept
            if new_description:
                update_data["description"] = new_description
            
            if update_data:
                result = make_request("PUT", f"/expense/{exp_id}", data=update_data)
                if result:
                    st.success("✅ Expense updated successfully!")
                    st.json(result)
            else:
                st.warning("⚠️ No fields to update")
    
    # TAB 4: Delete Expense
    with tab4:
        st.header("Delete Expense")
        st.warning("⚠️ This action cannot be undone!")
        
        exp_id = st.number_input("Expense ID to delete", min_value=1, step=1)
        
        if st.button("🗑️ Delete Expense", type="secondary"):
            result = make_request("DELETE", f"/expense/{exp_id}")
            if result is not None:
                st.success("✅ Expense deleted successfully!")


#INCOME MANAGEMENT


def page_income():
    st.title("💵 Income Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Record Income", "View Income", "Update Income", "Delete Income"])
    
    # TAB 1: Record Income
    with tab1:
        st.header("Record New Income")
        
        col1, col2 = st.columns(2)
        with col1:
            inc_date = st.date_input("Date", datetime.now())
            inc_amount = st.number_input("Amount ($)", min_value=0.0, step=0.01)
        with col2:
            inc_concept = st.text_input("Concept", placeholder="e.g., Salary, Freelance work")
        
        inc_description = st.text_area("Description (Optional)", 
            placeholder="Additional details about this income...")
        
        if st.button("💾 Record Income", type="primary"):
            if not inc_concept:
                st.error("❌ Please enter a concept")
            elif inc_amount <= 0:
                st.error("❌ Amount must be greater than 0")
            else:
                payload = {
                    "date": normalize_date_for_api(inc_date),
                    "amount": inc_amount,
                    "concept": inc_concept,
                    "description": inc_description if inc_description else None
                }
                
                result = make_request("POST", "/income", data=payload)
                if result:
                    st.success("✅ Income recorded successfully!")
                    st.json(result)
    
    # TAB 2: View Income
    with tab2:
        st.header("View All Income")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input("Search by concept", placeholder="e.g., Salary")
        with col2:
            limit = st.number_input("Results per page", value=20, min_value=1, max_value=100)
        
        params = {"limit": limit}
        if search_term:
            params["search"] = search_term
        
        data = make_request("GET", "/income", params=params)
        if data and data.get("items"):
            df = pd.DataFrame(data["items"])
            if "date" in df.columns:
                df["date"] = format_date_series(df["date"])
            df = df[["id", "date", "amount", "concept", "description"]]
            df.columns = ["ID", "Date", "Amount ($)", "Concept", "Description"]
            st.dataframe(df, width="stretch")
            st.caption(f"Total records: {data.get('total', 0)}")
        else:
            st.info("No income found")
    
    # TAB 3: Update Income
    with tab3:
        st.header("Update Income")
        
        inc_id = st.number_input("Income ID to update", min_value=1, step=1)
        
        col1, col2 = st.columns(2)
        with col1:
            new_date = st.date_input("New Date (optional)", value=None)
            new_amount = st.number_input("New Amount (optional)", value=0.0, step=0.01)
        with col2:
            new_concept = st.text_input("New Concept (optional)", placeholder="Leave empty to keep current")
        
        new_description = st.text_area("New Description (optional)", 
            placeholder="Leave empty to keep current")
        
        if st.button("🔄 Update Income"):
            update_data = {}
            if new_date:
                update_data["date"] = normalize_date_for_api(new_date)
            if new_amount > 0:
                update_data["amount"] = new_amount
            if new_concept:
                update_data["concept"] = new_concept
            if new_description:
                update_data["description"] = new_description
            
            if update_data:
                result = make_request("PUT", f"/income/{inc_id}", data=update_data)
                if result:
                    st.success("✅ Income updated successfully!")
                    st.json(result)
            else:
                st.warning("⚠️ No fields to update")
    
    # TAB 4: Delete Income
    with tab4:
        st.header("Delete Income")
        st.warning("⚠️ This action cannot be undone!")
        
        inc_id = st.number_input("Income ID to delete", min_value=1, step=1)
        
        if st.button("🗑️ Delete Income", type="secondary"):
            result = make_request("DELETE", f"/income/{inc_id}")
            if result is not None:
                st.success("✅ Income deleted successfully!")

#DEBT MANAGEMENT

def page_debt():
    st.title("💳 Debt Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Record Debt", "View Debt", "Update Debt", "Delete Debt"])
    
    # TAB 1: Record Debt
    with tab1:
        st.header("Record New Debt")
        
        col1, col2 = st.columns(2)
        with col1:
            debt_date = st.date_input("Date", datetime.now())
            debt_amount = st.number_input("Amount ($)", min_value=0.0, step=0.01)
        with col2:
            debt_borrower = st.text_input("Borrower", placeholder="Who are you borrowing from?")
            debt_borrowed = st.text_input("Borrowed", placeholder="What did you borrow?")
        
        col1, col2 = st.columns(2)
        with col1:
            debt_interest = st.number_input("Interest Rate (%) (Optional)", value=0.0, step=0.01)
        
        if st.button("💾 Record Debt", type="primary"):
            if not debt_borrower or not debt_borrowed:
                st.error("❌ Please enter both borrower and borrowed fields")
            elif debt_amount <= 0:
                st.error("❌ Amount must be greater than 0")
            else:
                payload = {
                    "date": normalize_date_for_api(debt_date),
                    "amount": debt_amount,
                    "borrower": debt_borrower,
                    "borrowed": debt_borrowed,
                    "interest": debt_interest if debt_interest > 0 else None
                }
                
                result = make_request("POST", "/debt", data=payload)
                if result:
                    st.success("✅ Debt recorded successfully!")
                    st.json(result)
    
    # TAB 2: View Debt
    with tab2:
        st.header("View All Debt")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input("Search by borrower", placeholder="e.g., Bank, Friend name")
        with col2:
            limit = st.number_input("Results per page", value=20, min_value=1, max_value=100)
        
        params = {"limit": limit}
        if search_term:
            params["search"] = search_term
        
        data = make_request("GET", "/debt", params=params)
        if data and data.get("items"):
            df = pd.DataFrame(data["items"])
            if "date" in df.columns:
                df["date"] = format_date_series(df["date"])
            df = df[["id", "date", "amount", "borrower", "borrowed", "interest"]]
            df.columns = ["ID", "Date", "Amount ($)", "Borrower", "Borrowed", "Interest (%)"]
            st.dataframe(df, width="stretch")
            st.caption(f"Total records: {data.get('total', 0)}")
        else:
            st.info("No debt records found")
    
    # TAB 3: Update Debt
    with tab3:
        st.header("Update Debt")
        
        debt_id = st.number_input("Debt ID to update", min_value=1, step=1)
        
        col1, col2 = st.columns(2)
        with col1:
            new_date = st.date_input("New Date (optional)", value=None)
            new_amount = st.number_input("New Amount (optional)", value=0.0, step=0.01)
        with col2:
            new_borrower = st.text_input("New Borrower (optional)", placeholder="Leave empty to keep current")
            new_borrowed = st.text_input("New Borrowed (optional)", placeholder="Leave empty to keep current")
        
        new_interest = st.number_input("New Interest Rate (optional)", value=0.0, step=0.01)
        
        if st.button("🔄 Update Debt"):
            update_data = {}
            if new_date:
                update_data["date"] = normalize_date_for_api(new_date)
            if new_amount > 0:
                update_data["amount"] = new_amount
            if new_borrower:
                update_data["borrower"] = new_borrower
            if new_borrowed:
                update_data["borrowed"] = new_borrowed
            if new_interest > 0:
                update_data["interest"] = new_interest
            
            if update_data:
                result = make_request("PUT", f"/debt/{debt_id}", data=update_data)
                if result:
                    st.success("✅ Debt updated successfully!")
                    st.json(result)
            else:
                st.warning("⚠️ No fields to update")
    
    # TAB 4: Delete Debt
    with tab4:
        st.header("Delete Debt")
        st.warning("⚠️ This action cannot be undone!")
        
        debt_id = st.number_input("Debt ID to delete", min_value=1, step=1)
        
        if st.button("🗑️ Delete Debt", type="secondary"):
            result = make_request("DELETE", f"/debt/{debt_id}")
            if result is not None:
                st.success("✅ Debt deleted successfully!")


#PRODUCTS & ITEMS MANAGEMENT


def page_products():
    st.title("📦 Products & Items")
    
    tab1, tab2 = st.tabs(["View Products", "View Items"])
    
    with tab1:
        st.header("Products List")
        st.info("Products are the types/categories of items you purchase")
        
        search_term = st.text_input("Search by product name", placeholder="e.g., Bread")
        limit = st.number_input("Results per page", value=20, min_value=1, max_value=100, key="products_limit")
        
        params = {"limit": limit}
        if search_term:
            params["search"] = search_term
        
        data = make_request("GET", "/product", params=params)
        if data and data.get("items"):
            df = pd.DataFrame(data["items"])
            df.columns = ["ID", "Name"]
            st.dataframe(df, width="stretch")
            st.caption(f"Total products: {data.get('total', 0)}")
        else:
            st.info("No products found")
    
    with tab2:
        st.header("Items in Purchases")
        st.info("Items are individual instances of products in a purchase")
        
        search_term = st.text_input("Search by item name", placeholder="e.g., Bread")
        limit = st.number_input("Results per page", value=20, min_value=1, max_value=100, key="items_limit")
        
        params = {"limit": limit}
        if search_term:
            params["search"] = search_term
        
        data = make_request("GET", "/Items", params=params)
        if data and data.get("items"):
            df = pd.DataFrame(data["items"])
            df = df[["id", "name", "cost", "Quantity", "ID_buy", "ID_expense"]]
            df.columns = ["ID", "Name", "Cost ($)", "Quantity", "Buy ID", "Expense ID"]
            st.dataframe(df, width="stretch")
            st.caption(f"Total items: {data.get('total', 0)}")
        else:
            st.info("No items found")

"""
ANALYTICS / VISUALIZATIONS
"""

def page_analytics():
    st.title("📊 Analytics & Visualizations")
    
    # Time period selector
    col1, col2, col3 = st.columns(3)
    with col1:
        time_period = st.selectbox(
            "Time Period",
            ["Last 7 Days", "Last 30 Days", "Last 90 Days", "All Time"],
            index=1
        )
    
    # Calculate date range
    today = datetime.now()
    if time_period == "Last 7 Days":
        start_date = today - timedelta(days=7)
    elif time_period == "Last 30 Days":
        start_date = today - timedelta(days=30)
    elif time_period == "Last 90 Days":
        start_date = today - timedelta(days=90)
    else:  # All Time
        start_date = datetime(2000, 1, 1)
    
    # Get all data
    expenses_data = make_request("GET", "/expense", params={"limit": 1000})
    income_data = make_request("GET", "/income", params={"limit": 1000})
    buys_data = make_request("GET", "/buy", params={"limit": 1000})
    
    # Filter by date
    def filter_by_date(data_list, start_dt):
        if not data_list:
            return []
        filtered = []
        for item in data_list:
            try:
                raw_date = str(item.get("date", "")).strip()
                if not raw_date:
                    continue
                if not raw_date:
                    continue
                if "T" in raw_date or " " in raw_date:
                    item_date = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
                else:
                    item_date = datetime.strptime(raw_date[:10], "%Y-%m-%d")
                if item_date >= start_dt:
                    filtered.append(item)
            except (TypeError, ValueError):
                pass
        return filtered
    
    expenses_filtered = filter_by_date(expenses_data.get("items", []) if expenses_data else [], start_date) if expenses_data else []
    income_filtered = filter_by_date(income_data.get("items", []) if income_data else [], start_date) if income_data else []
    buys_filtered = filter_by_date(buys_data.get("items", []) if buys_data else [], start_date) if buys_data else []
    
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["Expenses Breakdown", "Income Breakdown", "Income vs Expenses", "Buys Overview"])
    
    # TAB 1: Expenses by Concept (Pie Chart)
    with tab1:
        st.subheader("Expenses by Category")
        
        if expenses_filtered:
            exp_df = pd.DataFrame(expenses_filtered)
            expense_summary = exp_df.groupby("concept")["amount"].sum().reset_index()
            expense_summary = expense_summary.sort_values("amount", ascending=False)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig = px.pie(
                    expense_summary,
                    values="amount",
                    names="concept",
                    title=f"Expense Distribution ({time_period})",
                    hole=0.3,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_traces(textposition="inside", textinfo="percent+label")
                st.plotly_chart(fig, width="stretch")
            
            with col2:
                st.metric("Total Expenses", f"${expense_summary['amount'].sum():.2f}")
                st.divider()
                st.write("**Top Expenses:**")
                for idx, row in expense_summary.head(5).iterrows():
                    st.write(f"• {row['concept']}: ${row['amount']:.2f}")
        else:
            st.info("No expense data for this period")
    
    # TAB 2: Income by Concept (Pie Chart)
    with tab2:
        st.subheader("Income by Source")
        
        if income_filtered:
            inc_df = pd.DataFrame(income_filtered)
            income_summary = inc_df.groupby("concept")["amount"].sum().reset_index()
            income_summary = income_summary.sort_values("amount", ascending=False)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig = px.pie(
                    income_summary,
                    values="amount",
                    names="concept",
                    title=f"Income Distribution ({time_period})",
                    hole=0.3,
                    color_discrete_sequence=px.colors.qualitative.Pastel
                )
                fig.update_traces(textposition="inside", textinfo="percent+label")
                st.plotly_chart(fig, width="stretch")
            
            with col2:
                st.metric("Total Income", f"${income_summary['amount'].sum():.2f}")
                st.divider()
                st.write("**Top Income Sources:**")
                for idx, row in income_summary.head(5).iterrows():
                    st.write(f"• {row['concept']}: ${row['amount']:.2f}")
        else:
            st.info("No income data for this period")
    
    # TAB 3: Income vs Expenses (Bar Chart)
    with tab3:
        st.subheader("Income vs Expenses Over Time")
        
        if expenses_filtered or income_filtered:
            # Prepare data by date
            exp_dict = {}
            inc_dict = {}
            
            for exp in expenses_filtered:
                try:
                    exp_date = datetime.fromisoformat(exp.get("date", "").replace("Z", "+00:00")).date()
                    if exp_date not in exp_dict:
                        exp_dict[exp_date] = 0
                    exp_dict[exp_date] += exp.get("amount", 0)
                except:
                    pass
            
            for inc in income_filtered:
                try:
                    inc_date = datetime.fromisoformat(inc.get("date", "").replace("Z", "+00:00")).date()
                    if inc_date not in inc_dict:
                        inc_dict[inc_date] = 0
                    inc_dict[inc_date] += inc.get("amount", 0)
                except:
                    pass
            
            # Create comparison data
            all_dates = sorted(set(list(exp_dict.keys()) + list(inc_dict.keys())))
            comparison_data = {
                "Date": all_dates,
                "Income": [inc_dict.get(d, 0) for d in all_dates],
                "Expenses": [exp_dict.get(d, 0) for d in all_dates]
            }
            
            comp_df = pd.DataFrame(comparison_data)
            
            fig = px.bar(
                comp_df,
                x="Date",
                y=["Income", "Expenses"],
                title=f"Income vs Expenses ({time_period})",
                barmode="group",
                color_discrete_map={"Income": "#90EE90", "Expenses": "#FF6B6B"},
                labels={"value": "Amount ($)", "variable": "Type"}
            )
            fig.update_layout(hovermode="x unified")
            st.plotly_chart(fig, width="stretch")
            
            # Summary stats
            col1, col2, col3 = st.columns(3)
            total_income = sum(inc_dict.values())
            total_expenses = sum(exp_dict.values())
            balance = total_income - total_expenses
            
            with col1:
                st.metric("Total Income", f"${total_income:.2f}")
            with col2:
                st.metric("Total Expenses", f"${total_expenses:.2f}")
            with col3:
                st.metric("Net Balance", f"${balance:.2f}", 
                        delta_color="off" if balance >= 0 else "inverse")
        else:
            st.info("No data available for this period")
    
    # TAB 4: Buys Overview
    with tab4:
        st.subheader("Shopping Overview")
        
        if buys_filtered:
            # Buys by location
            buys_df = pd.DataFrame(buys_filtered)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Pie chart by location
                if not buys_df["local"].isna().all():
                    location_summary = buys_df.groupby("local")["cost"].sum().reset_index()
                    location_summary = location_summary[location_summary["local"].notna()]
                    
                    if not location_summary.empty:
                        fig = px.pie(
                            location_summary,
                            values="cost",
                            names="local",
                            title="Spending by Store",
                            color_discrete_sequence=px.colors.qualitative.Plotly
                        )
                        fig.update_traces(textposition="inside", textinfo="percent+label")
                        st.plotly_chart(fig, width="stretch")
                    else:
                        st.info("No location data available")
                else:
                    st.info("No location data available")
            
            with col2:
                # Summary statistics
                st.metric("Total Buys", len(buys_filtered))
                st.metric("Total Spent", f"${buys_df['cost'].sum():.2f}")
                st.metric("Average Per Buy", f"${buys_df['cost'].mean():.2f}")
                
                st.divider()
                st.write("**By Business Type:**")
                if not buys_df["business_type"].isna().all():
                    type_summary = buys_df.groupby("business_type")["cost"].agg(["count", "sum"]).reset_index()
                    type_summary.columns = ["Type", "Count", "Total"]
                    for idx, row in type_summary.iterrows():
                        st.write(f"• {row['Type']}: {int(row['Count'])} buys - ${row['Total']:.2f}")
                else:
                    st.info("No business type data")
        else:
            st.info("No buy data for this period")


#DASHBOARD / HOME


def page_dashboard():
    st.title("📈 Dashboard")
    
    # Get summary data
    buys = make_request("GET", "/buy", params={"limit": 1000})
    expenses = make_request("GET", "/expense", params={"limit": 1000})
    income = make_request("GET", "/income", params={"limit": 1000})
    debt = make_request("GET", "/debt", params={"limit": 1000})
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_buys = buys.get("total", 0) if buys else 0
        st.metric("Total Buys", total_buys, "transactions")
    
    with col2:
        total_expenses = sum(item["amount"] for item in expenses.get("items", [])) if expenses else 0
        st.metric("Total Expenses", f"${total_expenses:.2f}")
    
    with col3:
        total_income = sum(item["amount"] for item in income.get("items", [])) if income else 0
        st.metric("Total Income", f"${total_income:.2f}")
    
    with col4:
        total_debt = sum(item["amount"] for item in debt.get("items", [])) if debt else 0
        st.metric("Total Debt", f"${total_debt:.2f}")
    
    # Summary balance
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        balance = total_income - total_expenses
        st.metric("Balance (Income - Expenses)", f"${balance:.2f}", 
                 delta=f"${total_income:.2f}", delta_color="off")
    
    with col2:
        net_balance = total_income - total_expenses - total_debt
        st.metric("Net Balance (minus Debt)", f"${net_balance:.2f}",
                 delta=f"-${total_debt:.2f}" if total_debt > 0 else None)
    
    # Recent activity
    st.divider()
    st.subheader("Recent Activity")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Recent Buys**")
        if buys and buys.get("items"):
            recent_buys = sorted(buys["items"], 
                                key=lambda x: x.get("date", ""), 
                                reverse=True)[:5]
            for buy in recent_buys:
                st.write(f"• {buy['local']} - ${buy.get('cost', 0):.2f}")
        else:
            st.info("No buys yet")
    
    with col2:
        st.write("**Recent Expenses**")
        if expenses and expenses.get("items"):
            recent_expenses = sorted(expenses["items"], 
                                    key=lambda x: x.get("date", ""), 
                                    reverse=True)[:5]
            for exp in recent_expenses:
                st.write(f"• {exp['concept']} - ${exp.get('amount', 0):.2f}")
        else:
            st.info("No expenses yet")


#MAIN APP


def main():
    # Sidebar navigation
    with st.sidebar:
        st.title("💰 Budget Manager")
        st.divider()
        
        page = st.radio(
            "Navigation",
            ["Dashboard", "📊 Analytics", "💳 Buys", "📊 Expenses", "💵 Income", "💳 Debt", "📦 Products & Items"],
            label_visibility="collapsed"
        )
        
        st.divider()
        st.caption("Made with Streamlit + FastAPI")
        st.caption("API: http://127.0.0.1:8000")
    
    # Page routing
    if page == "Dashboard":
        page_dashboard()
    elif page == "📊 Analytics":
        page_analytics()
    elif page == "💳 Buys":
        page_buys()
    elif page == "📊 Expenses":
        page_expenses()
    elif page == "💵 Income":
        page_income()
    elif page == "💳 Debt":
        page_debt()
    elif page == "📦 Products & Items":
        page_products()

if __name__ == "__main__":
    main()
