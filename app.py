import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import warnings
warnings.filterwarnings('ignore')

# =============================================
# PAGE CONFIGURATION
# =============================================
st.set_page_config(
    page_title='UAC Care System Analytics',
    page_icon='🏥',
    layout='wide'
)

# =============================================
# LOAD DATA
# =============================================
@st.cache_data
def load_data():
    df = pd.read_csv('uac_cleaned.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# =============================================
# TITLE
# =============================================
st.title('🏥 System Capacity & Care Load Analytics')
st.subheader('U.S Department of Health and Human Services')
st.markdown('---')

# =============================================
# SIDEBAR FILTERS
# =============================================
st.sidebar.title('🔧 Filters')

# Date range selector
min_date = df['Date'].min()
max_date = df['Date'].max()

start_date, end_date = st.sidebar.date_input(
    'Select Date Range',
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

st.sidebar.markdown('---')

# Time Granularity Filter
st.sidebar.subheader('⏱️ Time Granularity')
granularity = st.sidebar.selectbox(
    'Select Granularity',
    options=['Daily', 'Weekly', 'Monthly']
)

st.sidebar.markdown('---')

# Metric Toggles
st.sidebar.subheader('📊 Metric Toggles')
show_cbp       = st.sidebar.checkbox('Show CBP Custody',          value=True)
show_hhs       = st.sidebar.checkbox('Show HHS Care',             value=True)
show_7day      = st.sidebar.checkbox('Show 7-Day Rolling Avg',    value=True)
show_14day     = st.sidebar.checkbox('Show 14-Day Rolling Avg',   value=True)
show_threshold = st.sidebar.checkbox('Show High Load Threshold',  value=True)
show_anomalies = st.sidebar.checkbox('Show Anomaly Points',       value=True)

st.sidebar.markdown('---')

# Filter dataframe by date
df_filtered = df[
    (df['Date'] >= pd.to_datetime(start_date)) &
    (df['Date'] <= pd.to_datetime(end_date))
]

st.sidebar.write(f"📅 Showing {len(df_filtered)} days of data")

# Apply Time Granularity
if granularity == 'Weekly':
    df_plot = df_filtered.resample('W', on='Date').mean(numeric_only=True).reset_index()
elif granularity == 'Monthly':
    df_plot = df_filtered.resample('ME', on='Date').mean(numeric_only=True).reset_index()
else:
    df_plot = df_filtered.copy()

# =============================================
# KPI CARDS
# =============================================
st.subheader('📊 Key Performance Indicators')

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label='Avg Daily Children Under Care',
        value=f"{df_filtered['Total System Load'].mean():.0f}"
    )

with col2:
    st.metric(
        label='Net Intake Pressure',
        value=f"{df_filtered['Net Daily Intake'].mean():.2f}"
    )

with col3:
    st.metric(
        label='Volatility Index',
        value=f"{df_filtered['Total System Load'].std():.2f}"
    )

with col4:
    st.metric(
        label='Backlog Accumulation',
        value=f"{df_filtered['Backlog Indicator'].iloc[-1]:.0f}"
    )

with col5:
    discharge_ratio = (
        df_filtered['Children discharged from HHS Care'].sum() /
        df_filtered['Children transferred out of CBP custody'].sum()
    )
    st.metric(
        label='Discharge Offset Ratio',
        value=f"{discharge_ratio:.2f}"
    )

st.markdown('---')

# =============================================
# SYSTEM LOAD OVERVIEW
# =============================================
st.subheader('📈 System Load Overview')

fig, ax = plt.subplots(figsize=(15, 5))

ax.plot(df_plot['Date'], df_plot['Total System Load'],
        color='steelblue', linewidth=0.8,
        alpha=0.5, label='Total System Load')

if show_7day:
    ax.plot(df_plot['Date'], df_plot['7day Rolling Avg'],
            color='orange', linewidth=2, label='7-Day Avg')

if show_14day:
    ax.plot(df_plot['Date'], df_plot['14day Rolling Avg'],
            color='red', linewidth=2, label='14-Day Avg')

if show_threshold:
    threshold = df_plot['Total System Load'].quantile(0.80)
    ax.axhline(y=threshold, color='darkred', linestyle='--',
               linewidth=1.5,
               label=f'High Load Threshold ({threshold:.0f})')
    ax.fill_between(df_plot['Date'],
                    df_plot['Total System Load'], threshold,
                    where=df_plot['Total System Load'] > threshold,
                    alpha=0.2, color='red', label='High Load Period')

if show_anomalies:
    anomaly_data = df_plot[df_plot['Anomaly Flag'] == True]
    ax.scatter(anomaly_data['Date'],
               anomaly_data['Total System Load'],
               color='red', s=20, zorder=5,
               label=f'Anomalies ({len(anomaly_data)})')

ax.set_title(f'Total System Load Over Time ({granularity} View)',
             fontweight='bold', fontsize=14)
ax.set_xlabel('Date')
ax.set_ylabel('Total Children')
ax.legend()
ax.grid(True, alpha=0.3)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

st.markdown('---')

# =============================================
# CBP VS HHS COMPARISON
# =============================================
st.subheader('⚖️ CBP vs HHS Load Comparison')

fig, ax = plt.subplots(figsize=(15, 5))

if show_cbp:
    ax.plot(df_plot['Date'],
            df_plot['Children in CBP custody'],
            color='steelblue', linewidth=1.5,
            label='CBP Custody')

if show_hhs:
    ax.plot(df_plot['Date'],
            df_plot['Children in HHS Care'],
            color='orange', linewidth=1.5,
            label='HHS Care')

ax.set_title(f'CBP vs HHS Care Load Comparison ({granularity} View)',
             fontweight='bold', fontsize=14)
ax.set_xlabel('Date')
ax.set_ylabel('Total Children')
ax.legend()
ax.grid(True, alpha=0.3)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

st.markdown('---')

# =============================================
# NET INTAKE & BACKLOG TRENDS
# =============================================
st.subheader('📉 Net Intake & Backlog Trends')

fig, axes = plt.subplots(2, 1, figsize=(15, 10))

# Net Daily Intake
axes[0].bar(df_plot['Date'], df_plot['Net Daily Intake'],
            color=df_plot['Net Daily Intake'].apply(
                lambda x: 'red' if x > 0 else 'green'),
            alpha=0.7, width=1)
axes[0].axhline(y=0, color='black', linewidth=1)
axes[0].set_title('Net Daily Intake — Red: Pressure | Green: Relief',
                  fontweight='bold', fontsize=14)
axes[0].set_xlabel('Date')
axes[0].set_ylabel('Net Children')
axes[0].grid(True, alpha=0.3)
axes[0].xaxis.set_major_locator(mdates.MonthLocator(interval=2))
axes[0].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.setp(axes[0].xaxis.get_majorticklabels(), rotation=45)

# Backlog Indicator
axes[1].plot(df_plot['Date'], df_plot['Backlog Indicator'],
             color='purple', linewidth=1.5)
axes[1].fill_between(df_plot['Date'],
                     df_plot['Backlog Indicator'],
                     alpha=0.2, color='purple')
axes[1].axhline(y=0, color='black', linewidth=1, linestyle='--')
axes[1].set_title('Cumulative Backlog Indicator',
                  fontweight='bold', fontsize=14)
axes[1].set_xlabel('Date')
axes[1].set_ylabel('Cumulative Net Intake')
axes[1].grid(True, alpha=0.3)
axes[1].xaxis.set_major_locator(mdates.MonthLocator(interval=2))
axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=45)

plt.tight_layout()
st.pyplot(fig)

st.markdown('---')

# =============================================
# FOOTER
# =============================================
st.markdown(
    """
    <div style='text-align: center; color: grey;'>
    UAC Care System Analytics | 
    </div>
    """,
    unsafe_allow_html=True
)