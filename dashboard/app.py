
import streamlit as st
import pandas as pd
import plotly.express as px

from dashboard.db_connection import load_aggregate_data


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Hospitality Analytics Dashboard",
    page_icon="🏨",
    layout="wide"
)

st.title("🏨 Hospitality Analytics Dashboard")
st.caption("Hotel performance analysis | 2022–2026")


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data(ttl=300)
def get_dashboard_data():
    return {
        "performance": load_aggregate_data("monthly_performance"),
        "satisfaction": load_aggregate_data("monthly_satisfaction"),
        "turnover": load_aggregate_data("annual_turnover"),
    }


try:
    data = get_dashboard_data()

    performance = data["performance"]
    satisfaction = data["satisfaction"]
    turnover = data["turnover"]

except Exception as error:
    st.error(f"Unable to load dashboard data: {error}")
    st.stop()


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("Dashboard Filters")

cities = sorted(performance["location"].dropna().unique())

selected_city = st.sidebar.selectbox(
    "Select City",
    ["All Cities"] + cities
)

if selected_city == "All Cities":
    available_hotels = sorted(performance["hotel_name"].unique())
else:
    available_hotels = sorted(
        performance.loc[
            performance["location"] == selected_city,
            "hotel_name"
        ].unique()
    )

selected_hotel = st.sidebar.selectbox(
    "Select Hotel",
    ["All Hotels"] + available_hotels
)

years = sorted(performance["year"].unique())

selected_years = st.sidebar.multiselect(
    "Select Year",
    years,
    default=years
)

months = sorted(performance["month"].dropna().unique())

month_options = [
    performance.loc[
        performance["month"] == month,
        "month_name"
    ].iloc[0]
    for month in months
]

selected_months = st.sidebar.multiselect(
    "Select Month",
    month_options,
    default=month_options
)


# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

def apply_filters(df):
    filtered = df.copy()

    if selected_city != "All Cities":
        filtered = filtered[
            filtered["location"] == selected_city
        ]

    if selected_hotel != "All Hotels":
        filtered = filtered[
            filtered["hotel_name"] == selected_hotel
        ]

    filtered = filtered[
        filtered["year"].isin(selected_years)
    ]

    if "month_name" in filtered.columns:
        filtered = filtered[
            filtered["month_name"].isin(selected_months)
        ]

    return filtered


filtered_performance = apply_filters(performance)
filtered_satisfaction = apply_filters(satisfaction)
filtered_turnover = apply_filters(turnover)


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def get_trend_insight(df, value_column, metric_name, unit=""):
    """Generate a simple observation about monthly highs and lows."""

    if df.empty:
        return "No data available for the selected filters."

    highest = df.loc[df[value_column].idxmax()]
    lowest = df.loc[df[value_column].idxmin()]

    if highest["period"] == lowest["period"]:
        return (
            f"{metric_name} is {highest[value_column]:.2f}{unit} "
            f"in {highest['period'].strftime('%b %Y')}."
        )

    return (
        f"Highest {metric_name}: {highest[value_column]:.2f}{unit} "
        f"({highest['period'].strftime('%b %Y')}). "
        f"Lowest {metric_name}: {lowest[value_column]:.2f}{unit} "
        f"({lowest['period'].strftime('%b %Y')})."
    )


def configure_monthly_chart(fig, df):
    """Display readable month-year labels without overcrowding."""

    if df.empty:
        return fig

    date_range_months = (
        (df["period"].max().year - df["period"].min().year) * 12
        + df["period"].max().month
        - df["period"].min().month
    )

    # Adjust label frequency based on selected date range
    if date_range_months <= 24:
        interval = "M3"
    else:
        interval = "M6"

    fig.update_xaxes(
        tickformat="%b %Y",
        dtick=interval,
        tick0="2022-01-01",
        tickangle=-30,
        title_text="Month"
    )

    fig.update_layout(
        hovermode="x unified",
        margin=dict(b=80)
    )

    return fig


# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------

available_nights = filtered_performance[
    "available_room_nights"
].sum()

occupied_nights = filtered_performance[
    "occupied_room_nights"
].sum()

total_revenue = filtered_performance[
    "total_room_revenue"
].sum()

occupancy_rate = (
    occupied_nights / available_nights * 100
    if available_nights > 0 else 0
)

adr = (
    total_revenue / occupied_nights
    if occupied_nights > 0 else 0
)

revpar = (
    total_revenue / available_nights
    if available_nights > 0 else 0
)

total_feedback = filtered_satisfaction[
    "total_feedback"
].sum()

satisfaction_score = (
    (
        filtered_satisfaction["avg_satisfaction_score"]
        * filtered_satisfaction["total_feedback"]
    ).sum() / total_feedback
    if total_feedback > 0 else 0
)

total_exits = filtered_turnover[
    "total_employee_exits"
].sum()

average_employee_count = filtered_turnover[
    "avg_monthly_employee_count"
].sum()

turnover_rate = (
    total_exits / average_employee_count * 100
    if average_employee_count > 0 else 0
)


# --------------------------------------------------
# KEY PERFORMANCE INDICATORS
# --------------------------------------------------

st.divider()
st.subheader("Key Performance Indicators")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Occupancy Rate", f"{occupancy_rate:.2f}%")
    st.caption("Percentage of available rooms occupied.")

with col2:
    st.metric("ADR", f"₹{adr:,.2f}")
    st.caption("Average revenue earned per occupied room.")

with col3:
    st.metric("RevPAR", f"₹{revpar:,.2f}")
    st.caption("Revenue earned per available room.")

with col4:
    st.metric("Guest Satisfaction", f"{satisfaction_score:.2f}/5")
    st.caption("Average guest feedback rating.")

with col5:
    st.metric("Employee Turnover", f"{turnover_rate:.2f}%")
    st.caption("Annual employee exits relative to average workforce.")


# --------------------------------------------------
# MONTHLY HOTEL PERFORMANCE
# --------------------------------------------------

st.divider()
st.subheader("Hotel Performance Trends")

st.caption(
    "These charts show how room occupancy, pricing and revenue "
    "change over time. Use them to identify seasonal demand and "
    "revenue patterns."
)

if not filtered_performance.empty:

    monthly = (
        filtered_performance
        .groupby(["year", "month", "month_name"], as_index=False)
        .agg({
            "available_room_nights": "sum",
            "occupied_room_nights": "sum",
            "total_room_revenue": "sum"
        })
    )

    monthly["period"] = pd.to_datetime(
        monthly["year"].astype(str)
        + "-"
        + monthly["month"].astype(str).str.zfill(2)
        + "-01"
    )

    monthly["occupancy_rate"] = (
        monthly["occupied_room_nights"]
        / monthly["available_room_nights"] * 100
    )

    monthly["ADR"] = (
        monthly["total_room_revenue"]
        / monthly["occupied_room_nights"]
    )

    monthly["RevPAR"] = (
        monthly["total_room_revenue"]
        / monthly["available_room_nights"]
    )

    monthly = monthly.sort_values("period")

    col1, col2 = st.columns(2)

    with col1:
        fig = px.line(
            monthly,
            x="period",
            y="occupancy_rate",
            markers=True,
            title="Monthly Occupancy Rate",
            labels={
                "period": "Month",
                "occupancy_rate": "Occupancy (%)"
            }
        )

        fig = configure_monthly_chart(fig, monthly)

        st.plotly_chart(fig, use_container_width=True)

        st.caption(
            "Business meaning: Shows the proportion of available room "
            "nights occupied each month. Peaks may indicate strong "
            "tourism demand, holidays or local events."
        )

        st.info(
            get_trend_insight(
                monthly,
                "occupancy_rate",
                "Occupancy",
                "%"
            )
        )

    with col2:
        fig = px.line(
            monthly,
            x="period",
            y="ADR",
            markers=True,
            title="Monthly Average Daily Rate",
            labels={
                "period": "Month",
                "ADR": "ADR (₹)"
            }
        )

        fig = configure_monthly_chart(fig, monthly)

        st.plotly_chart(fig, use_container_width=True)

        st.caption(
            "Business meaning: Shows the average revenue earned per "
            "occupied room night. Higher values may reflect peak-season "
            "pricing or changes in room demand."
        )

        st.info(
            get_trend_insight(
                monthly,
                "ADR",
                "ADR",
                " ₹"
            )
        )

    fig = px.line(
        monthly,
        x="period",
        y="RevPAR",
        markers=True,
        title="Monthly Revenue Per Available Room",
        labels={
            "period": "Month",
            "RevPAR": "RevPAR (₹)"
        }
    )

    fig = configure_monthly_chart(fig, monthly)

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Business meaning: Combines room occupancy and pricing to show "
        "how effectively available room capacity generates revenue. "
        "A higher RevPAR indicates stronger room revenue performance."
    )

    st.info(
        get_trend_insight(
            monthly,
            "RevPAR",
            "RevPAR",
            " ₹"
        )
    )

else:
    st.info("No performance data available for the selected filters.")


# --------------------------------------------------
# GUEST SATISFACTION
# --------------------------------------------------

st.divider()
st.subheader("Guest Satisfaction Trend")

st.caption(
    "Tracks changes in guest feedback scores over time. "
    "Use this chart to identify months with stronger or weaker "
    "guest experiences."
)

if not filtered_satisfaction.empty:

    satisfaction_trend = filtered_satisfaction.copy()

    satisfaction_trend["weighted_score"] = (
        satisfaction_trend["avg_satisfaction_score"]
        * satisfaction_trend["total_feedback"]
    )

    satisfaction_trend = (
        satisfaction_trend
        .groupby(["year", "month", "month_name"], as_index=False)
        .agg({
            "weighted_score": "sum",
            "total_feedback": "sum"
        })
    )

    satisfaction_trend = satisfaction_trend[
        satisfaction_trend["total_feedback"] > 0
    ]

    if not satisfaction_trend.empty:

        satisfaction_trend["avg_satisfaction"] = (
            satisfaction_trend["weighted_score"]
            / satisfaction_trend["total_feedback"]
        )

        satisfaction_trend["period"] = pd.to_datetime(
            satisfaction_trend["year"].astype(str)
            + "-"
            + satisfaction_trend["month"].astype(str).str.zfill(2)
            + "-01"
        )

        satisfaction_trend = satisfaction_trend.sort_values("period")

        fig = px.line(
            satisfaction_trend,
            x="period",
            y="avg_satisfaction",
            markers=True,
            title="Monthly Guest Satisfaction Score",
            labels={
                "period": "Month",
                "avg_satisfaction": "Average Rating"
            }
        )

        fig.update_yaxes(range=[1, 5])

        fig = configure_monthly_chart(fig, satisfaction_trend)

        st.plotly_chart(fig, use_container_width=True)

        st.caption(
            "Business meaning: Shows the average guest rating on a "
            "scale of 1 to 5. A decline may indicate service issues, "
            "crowding or longer waiting times."
        )

        st.info(
            get_trend_insight(
                satisfaction_trend,
                "avg_satisfaction",
                "Guest satisfaction"
            )
        )

    else:
        st.info("No feedback records available for the selected filters.")

else:
    st.info("No satisfaction data available for the selected filters.")


# --------------------------------------------------
# EMPLOYEE TURNOVER
# --------------------------------------------------

st.divider()
st.subheader("Employee Turnover Analysis")

st.caption(
    "Shows annual employee turnover for the selected hotels and years. "
    "The month filter does not apply because employee turnover is "
    "stored as an annual aggregate."
)

if not filtered_turnover.empty:

    annual_turnover = (
        filtered_turnover
        .groupby("year", as_index=False)
        .agg({
            "total_employee_exits": "sum",
            "avg_monthly_employee_count": "sum"
        })
    )

    annual_turnover["turnover_rate"] = (
        annual_turnover["total_employee_exits"]
        / annual_turnover["avg_monthly_employee_count"]
        * 100
    )

    annual_turnover = annual_turnover.sort_values("year")

    fig = px.bar(
        annual_turnover,
        x="year",
        y="turnover_rate",
        text="turnover_rate",
        title="Weighted Annual Employee Turnover Rate",
        labels={
            "year": "Year",
            "turnover_rate": "Turnover Rate (%)"
        }
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig.update_layout(
        yaxis_title="Turnover Rate (%)",
        xaxis_title="Year"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Business meaning: Compares annual employee exits against "
        "the stored average monthly employee-count measure. "
        "Increasing turnover may indicate retention or workforce "
        "management challenges."
    )

    highest_turnover = annual_turnover.loc[
        annual_turnover["turnover_rate"].idxmax()
    ]

    lowest_turnover = annual_turnover.loc[
        annual_turnover["turnover_rate"].idxmin()
    ]

    st.info(
        f"Highest turnover: {highest_turnover['turnover_rate']:.2f}% "
        f"in {int(highest_turnover['year'])}. "
        f"Lowest turnover: {lowest_turnover['turnover_rate']:.2f}% "
        f"in {int(lowest_turnover['year'])}."
    )

else:
    st.info("No employee turnover data available for the selected filters.")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Hospitality Analytics Project | "
    "Data sourced from MySQL aggregate tables | "
    "2022–2026"
)
