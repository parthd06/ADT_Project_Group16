import streamlit as st
import mysql.connector
import matplotlib.pyplot as plt

# Function to create a connection and cursor
def create_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="final_project"
    )
    return conn, conn.cursor()

# Function to search for athlete data
def search_athlete_data(name):
    conn, c = create_connection()
    c.execute("SELECT * FROM Team WHERE Name LIKE %s", ('%' + name + '%',))
    athlete_data = c.fetchall()
    conn.close()
    return athlete_data


# Function to search for medals earned by the athlete
def search_medals_earned_by_athlete(athlete_name):
    conn, c = create_connection()
    c.execute("SELECT Medal, COUNT(*) FROM Medals WHERE Name LIKE %s GROUP BY Medal", ('%' + athlete_name + '%',))
    medal_data = c.fetchall()
    conn.close()
    return medal_data

# Function to create pie chart for medals earned by the athlete
def create_pie_chart(medal_data, athlete_name):
    labels = [medal[0] for medal in medal_data]
    sizes = [medal[1] for medal in medal_data]
    colors = ['gold', 'silver', 'peru']
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title(f"Medals Earned by {athlete_name}")
    st.pyplot()


# Function to search for country-wise medal tally
def search_country_medal_tally(country):
    conn, c = create_connection()
    c.execute("SELECT Medal, COUNT(*) FROM Medals WHERE NOC LIKE %s GROUP BY Medal", ('%' + country + '%',))
    medal_tally_data = c.fetchall()
    conn.close()
    return medal_tally_data

# Function to create bar chart for country-wise medal tally
def create_bar_chart(medal_tally_data, country):
    medals = ["Gold", "Silver", "Bronze"]
    counts = [0, 0, 0]
    for medal, count in medal_tally_data:
        if medal == "Gold":
            counts[0] = count
        elif medal == "Silver":
            counts[1] = count
        elif medal == "Bronze":
            counts[2] = count

    plt.figure(figsize=(8, 6))
    plt.bar(medals, counts, color=['gold', 'silver', 'peru'])
    plt.xlabel('Medal Type')
    plt.ylabel('Number of Medals')
    plt.title(f"Medal Distribution for {country}")
    st.pyplot()







# Main function
def main():
    st.title("Search Page")

    # Sidebar option to choose between searching for athlete data, medals earned, or country-wise medal tally
    search_option = st.sidebar.radio("Search for:", ("Athlete Data", "Medals Earned", "Country-wise Medal Tally"))

    if search_option == "Athlete Data":
        st.header("Search for Athlete Data")
        athlete_name = st.text_input("Enter Athlete Name:")
        if st.button("Search"):
            athlete_data = search_athlete_data(athlete_name)
            if athlete_data:
                st.subheader("Athlete Data:")
                st.table(athlete_data)
            else:
                st.write("No athlete data found.")

    elif search_option == "Medals Earned":
        st.header("Search for Medals Earned")
        athlete_name = st.text_input("Enter Athlete Name:")
        if st.button("Search"):
            medal_data = search_medals_earned_by_athlete(athlete_name)
            if medal_data:
                st.subheader("Medals Earned:")
                st.write("Athlete:", athlete_name)
                st.write("Medals Earned:")
                for medal, count in medal_data:
                    st.write(f"{medal}: {count}")

                # Visualize medal distribution using pie chart
                create_pie_chart(medal_data, athlete_name)
            else:
                st.write("No medal data found for the athlete.")

    elif search_option == "Country-wise Medal Tally":
        st.header("Search for Country-wise Medal Tally")
        country = st.text_input("Enter Country NOC (e.g., USA, RUS, GER):")
        if st.button("Search"):
            medal_tally_data = search_country_medal_tally(country)
            if medal_tally_data:
                st.subheader("Country-wise Medal Tally:")
                st.write("Country:", country)
                st.write("Medal Tally:")
                for medal, count in medal_tally_data:
                    st.write(f"{medal}: {count}")

                # Visualize medal distribution using bar chart
                create_bar_chart(medal_tally_data, country)
            else:
                st.write("No medal tally data found.")

if __name__ == '__main__':
    main()
