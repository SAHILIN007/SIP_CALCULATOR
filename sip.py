import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from io import BytesIO

# Page config
st.set_page_config(page_title="SIPSense – Smart SIP Planner", layout="wide")

# Header
st.markdown("<h1 style='text-align: center; color:#4CAF50;'>💰 SIPSense – Smart SIP Planner</h1>", unsafe_allow_html=True)
st.markdown("### 📈 Grow your wealth wisely with monthly SIP insights and smart suggestions!")

# Sidebar Inputs
st.sidebar.header("📥 Enter Your SIP Details")
monthly_investment = st.sidebar.number_input("💸 Monthly Investment (₹)", min_value=500, step=500, value=5000)
years = st.sidebar.slider("🕒 Investment Duration (Years)", 1, 40, 10)
expected_return = st.sidebar.slider("📊 Expected Annual Return (%)", 1, 20, 12)
goal_amount = st.sidebar.number_input("🎯 Future Goal Amount (Optional)", min_value=0, step=10000, value=0)

# Calculations
months = years * 12
monthly_rate = expected_return / 12 / 100
invested_amount = monthly_investment * months
future_value = monthly_investment * (((1 + monthly_rate) ** months - 1) * (1 + monthly_rate) / monthly_rate)
returns = future_value - invested_amount

# Forecasts
def calculate_future_value(rate):
    r = rate / 12 / 100
    return monthly_investment * (((1 + r) ** months - 1) * (1 + r) / r)

fv_pess = calculate_future_value(max(1, expected_return - 2))
fv_opt = calculate_future_value(expected_return + 2)

# SIP Suggestion if Goal is Given
if goal_amount > 0:
    r = monthly_rate
    target_sip = goal_amount * r / (((1 + r) ** months - 1) * (1 + r))
    st.warning(f"🎯 To reach ₹{goal_amount:,.0f} in {years} years, invest approx ₹{target_sip:,.0f} monthly.")

    # Goal Progress
    progress = min(future_value / goal_amount, 1.0)
    st.progress(progress, text=f"Goal Achievement: {progress*100:.1f}%")

# Forecast Cards
st.subheader("🔮 Investment Scenarios")
colF1, colF2, colF3 = st.columns(3)
colF1.metric("📉 Pessimistic", f"₹{fv_pess:,.0f}", f"{max(1, expected_return - 2)}%")
colF2.metric("📈 Expected", f"₹{future_value:,.0f}", f"{expected_return}%")
colF3.metric("🚀 Optimistic", f"₹{fv_opt:,.0f}", f"{expected_return + 2}%")

# SIP Summary
st.subheader("📊 SIP Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Invested", f"₹{invested_amount:,.0f}")
col2.metric("Returns Earned", f"₹{returns:,.0f}")
col3.metric("Maturity Amount", f"₹{future_value:,.0f}")

# Pie Chart
st.subheader("📊 Investment vs Returns")
fig1, ax1 = plt.subplots()
labels = ['Invested', 'Returns']
sizes = [invested_amount, returns]
colors = ['#4CAF50', '#FFC107']
explode = (0, 0.05)
ax1.pie(sizes, labels=labels, autopct=lambda p: f'{p:.1f}%\n(₹{p*sum(sizes)/100:,.0f})', colors=colors, startangle=90, explode=explode)
ax1.axis('equal')
st.pyplot(fig1)

# Monthly Growth Data
values = []
total = 0
for i in range(months):
    total = total * (1 + monthly_rate) + monthly_investment
    values.append(total)

# Interactive Growth Graph
st.subheader("📈 Interactive Growth Chart")
df_plot = pd.DataFrame({
    "Month": list(range(1, months + 1)),
    "Value": values
})
chart = alt.Chart(df_plot).mark_line(color='blue').encode(
    x='Month',
    y='Value',
    tooltip=['Month', 'Value']
).interactive()
st.altair_chart(chart, use_container_width=True)

# Year-wise Summary
st.subheader("📆 Year-wise SIP Summary")
yearly_data = []
for y in range(1, years + 1):
    month_index = y * 12 - 1
    yearly_data.append({
        "Year": y,
        "Invested (₹)": monthly_investment * 12 * y,
        "Value (₹)": round(values[month_index])
    })
st.dataframe(pd.DataFrame(yearly_data), use_container_width=True)

# Monthly Statement
st.subheader("📄 Monthly SIP Statement (First 12 Months)")
data = []
value = 0
for i in range(months):
    value = value * (1 + monthly_rate) + monthly_investment
    data.append({
        "Month": i + 1,
        "Invested Till Now (₹)": monthly_investment * (i + 1),
        "Value (₹)": round(value)
    })
df = pd.DataFrame(data)
st.dataframe(df.head(12), use_container_width=True)

# Download Excel
excel_buffer = BytesIO()
with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
    df.to_excel(writer, index=False, sheet_name="SIP Statement")

st.download_button(
    label="📥 Download Full SIP Statement (Excel)",
    data=excel_buffer.getvalue(),
    file_name="SIP_Statement.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Inspirational Quote
quotes = [
    "💡 The best time to invest was yesterday. The next best time is now.",
    "💬 Do not save what is left after spending, spend what is left after saving. — Warren Buffett",
    "🌱 Wealth is the ability to fully experience life. — Thoreau"
]
st.markdown(f"<div style='background-color: #e8f5e9; padding: 15px; border-radius: 10px;'><i>{quotes[years % len(quotes)]}</i></div>", unsafe_allow_html=True)