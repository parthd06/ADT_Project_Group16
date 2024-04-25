import streamlit as st
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns

st.set_option('deprecation.showPyplotGlobalUse', False)

# Function to create a connection and cursor
def create_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="final_project"
    )
    return conn, conn.cursor()

# Function to fetch data from the tables
def fetch_data(table_name):
    conn, c = create_connection()
    c.execute(f"SELECT * FROM {table_name}")
    data = c.fetchall()
    conn.close()
    return data

# Function to create a histogram of athlete ages
def visualize_athlete_age_distribution():
    athletes = fetch_data("Team")
    ages = [athlete[3] for athlete in athletes] 
    plt.hist(ages, bins=20, color='skyblue', edgecolor='black')
    plt.xlabel('Age')
    plt.ylabel('Frequency')
    plt.title('Distribution of Athlete Ages')
    st.pyplot()

# Function to create a bar chart of medal counts by country
def visualize_medal_counts_by_country():
    medals = fetch_data("Medals")
    countries = [medal[2] for medal in medals] 
    medal_counts = {}
    for country in countries:
        if country in medal_counts:
            medal_counts[country] += 1
        else:
            medal_counts[country] = 1
    sns.barplot(x=list(medal_counts.keys()), y=list(medal_counts.values()))
    plt.xlabel('Country')
    plt.ylabel('Medal Count')
    plt.title('Medal Counts by Country')
    plt.xticks(rotation=90)
    st.pyplot()

# Function to create a pie chart of medal distribution
def visualize_medal_distribution(medals):
    medal_types = [medal[3] for medal in medals] 
    medal_counts = {}
    for medal_type in medal_types:
        if medal_type in medal_counts:
            medal_counts[medal_type] += 1
        else:
            medal_counts[medal_type] = 1
    
    # Create a pie chart
    fig, ax = plt.subplots()
    ax.pie(list(medal_counts.values()), labels=list(medal_counts.keys()), autopct='%1.1f%%')
    ax.set_title('Medal Distribution')
    
    # Show the chart in Streamlit
    st.pyplot(fig)



def visualize_height_weight_scatter():
    conn, c = create_connection()
    c.execute("SELECT Height, Weight FROM Team")
    data = c.fetchall()
    conn.close()

    heights = [row[0] for row in data]
    weights = [row[1] for row in data]

    plt.scatter(heights, weights)
    plt.xlabel("Height (cm)")
    plt.ylabel("Weight (kg)")
    plt.title("Athlete Height vs. Weight")
    st.pyplot()


def visualize_event_medal_distribution(top_n=10):
    st.subheader("Event-wise Medal Distribution")
    conn, c = create_connection()
    c.execute("SELECT Event, Medal, COUNT(*) FROM Medals GROUP BY Event, Medal")
    data = c.fetchall()
    conn.close()

    event_counts = {}
    for event, medal, count in data:
        if event not in event_counts:
            event_counts[event] = {'Gold': 0, 'Silver': 0, 'Bronze': 0}
        event_counts[event][medal] += count

    # Sort events by total medal count
    sorted_events = sorted(event_counts.keys(), key=lambda x: sum(event_counts[x].values()), reverse=True)
    top_events = sorted_events[:top_n]

    gold_counts = [sum(event_counts[event]['Gold'] for event in top_events)]
    silver_counts = [sum(event_counts[event]['Silver'] for event in top_events)]
    bronze_counts = [sum(event_counts[event]['Bronze'] for event in top_events)]

    plt.bar(top_events, gold_counts, label='Gold', color='gold')
    plt.bar(top_events, silver_counts, bottom=gold_counts, label='Silver', color='silver')
    plt.bar(top_events, bronze_counts, bottom=[sum(x) for x in zip(gold_counts, silver_counts)], label='Bronze', color='peru')
    plt.xlabel("Event")
    plt.ylabel("Number of Medals")
    plt.title(f"Top {top_n} Event-wise Medal Distribution")

    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right')

    plt.legend()
    st.pyplot()


def main():
    page = st.sidebar.selectbox("Choose a page", ["Athlete Age Distribution", "Medal Counts by Country", "Medal Distribution", "Athlete Height vs. Weight", "Eventwise Medals"])

    if page == "Athlete Age Distribution":
        st.subheader("Athlete Age Distribution")
        visualize_athlete_age_distribution()

    elif page == "Medal Counts by Country":
        st.subheader("Medal Counts by Country")
        visualize_medal_counts_by_country()

    elif page == "Medal Distribution":
        st.subheader("Medal Distribution")
        medals = fetch_data("medals")
        visualize_medal_distribution(medals)
    
    elif page == "Athlete Height vs. Weight":
        st.subheader("Height vs. Weight")
        visualize_height_weight_scatter()

    elif page == "Eventwise Medals":
        visualize_event_medal_distribution()

if __name__ == '__main__':
    main()