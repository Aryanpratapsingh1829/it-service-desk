"""
charts.py
Creates 4 charts from the tickets data using Matplotlib
and saves them as PNG files inside the 'charts' folder.
"""

from pathlib import Path
import matplotlib.pyplot as plt
from analysis import load_data, generate_report

# Create a 'charts' folder next to this file (if it doesn't exist)
CHART_DIR = Path(__file__).parent / "charts"
CHART_DIR.mkdir(exist_ok=True)


def save_bar_chart(series, title, xlabel, filename, color, horizontal=False):
    """
    Draw a bar chart from a Pandas Series and save it as a PNG.
    series: index = labels, values = counts
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    kind = "barh" if horizontal else "bar"
    series.plot(kind=kind, ax=ax, color=color)

    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xlabel(xlabel if not horizontal else "Number of tickets")
    ax.set_ylabel("Number of tickets" if not horizontal else xlabel)

    # Write the count on top of every bar
    for container in ax.containers:
        ax.bar_label(container)

    if not horizontal:
        plt.xticks(rotation=0)

    plt.tight_layout()
    fig.savefig(CHART_DIR / filename, dpi=150)
    plt.close(fig)          # free memory
    print("Saved:", filename)


def chart_status(report):
    """Chart 1: Ticket status distribution (pie chart)."""
    data = report["by_status"]
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(
        data.values,
        labels=data.index,
        autopct="%1.1f%%",          # show percentage on each slice
        startangle=90,
        colors=["#4CAF50", "#FFC107", "#F44336"],
    )
    ax.set_title("Ticket Status Distribution", fontsize=14, fontweight="bold")
    plt.tight_layout()
    fig.savefig(CHART_DIR / "1_status_distribution.png", dpi=150)
    plt.close(fig)
    print("Saved: 1_status_distribution.png")


def chart_category(report):
    """Chart 2: Issue category distribution."""
    save_bar_chart(
        report["by_category"],
        "Tickets by Issue Category",
        "Category",
        "2_category_distribution.png",
        "#2196F3",
    )


def chart_department(report):
    """Chart 3: Department-wise tickets (horizontal bars)."""
    # sort so the biggest department appears on top
    data = report["by_department"].sort_values()
    save_bar_chart(
        data,
        "Tickets by Department",
        "Department",
        "3_department_tickets.png",
        "#9C27B0",
        horizontal=True,
    )


def chart_priority(report):
    """Chart 4: Priority distribution in a logical order."""
    order = ["Low", "Medium", "High", "Critical"]
    data = report["by_priority"].reindex(order, fill_value=0)
    save_bar_chart(
        data,
        "Tickets by Priority",
        "Priority",
        "4_priority_distribution.png",
        ["#8BC34A", "#FFC107", "#FF9800", "#F44336"],
    )


def create_all_charts():
    """Load data, build the report, and draw all 4 charts."""
    df = load_data()
    report = generate_report(df)
    chart_status(report)
    chart_category(report)
    chart_department(report)
    chart_priority(report)
    print("\nAll charts saved in:", CHART_DIR)


if __name__ == "__main__":
    create_all_charts()