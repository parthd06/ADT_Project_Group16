import streamlit as st
import mysql.connector

# Function to create a connection and cursor
def create_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="final_project"
    )
    return conn, conn.cursor()


# CRUD operations for Medals table
def create_medal(name, noc, sport, event, medal):
    conn, c = create_connection()
    c.execute("INSERT INTO Medals (Name, NOC, Sport, Event, Medal) VALUES (%s, %s, %s, %s, %s)", (name, noc, sport, event, medal))
    conn.commit()
    conn.close()

def read_medals():
    conn, c = create_connection()
    c.execute("SELECT * FROM Medals")
    medals = c.fetchall()
    column_names = [description[0] for description in c.description]
    medals_with_column_names = [dict(zip(column_names, medal)) for medal in medals]
    conn.close()
    return medals_with_column_names

#Update Operations
def update_medal(medal_id, name, noc, sport, event, medal):
    conn, c = create_connection()
    c.execute("UPDATE Medals SET Name=%s, NOC=%s, Sport=%s, Event=%s, Medal=%s WHERE Medal_id=%s",
              (name, noc, sport, event, medal, medal_id))
    conn.commit()
    conn.close()



# Medals Page
def medal_data():
    st.title("Medals Data")
    st.sidebar.write("### Navigate to perform Operations:")
    operation = st.sidebar.selectbox(
        "", ["Add Medals Won", "View existing medals", "Update Medal results"])

    if operation == "Add Medals Won":
        st.subheader("Add Medal records:")
        st.image('../images/Podium.jpg', width=100)
        # Input fields for creating a new medal
        name = st.text_input("Name")
        noc = st.text_input("NOC")
        sport = st.text_input("Sport")
        event = st.text_input("Event")
        medal = st.selectbox("Medal", ["Gold", "Silver", "Bronze"])
        if st.button("Add Medal"):
            create_medal(name, noc, sport, event, medal)
            st.success("Medal added successfully!")
        
    elif operation == "View existing medals":
        st.subheader("Show Medals received")
        # Display existing medals
        medals = read_medals()
        if medals:
            st.table(medals)
        else:
            st.write("No medals available.")

    elif operation == "Update Medal results":
        st.subheader("Update medal details 📝:")
        medal_id = st.text_input("Enter Medal ID")
        name = st.text_input("Enter associated name")
        noc = st.text_input("Enter NOC")
        sport = st.text_input("Enter sport")
        event = st.text_input("Enter event")
        medal = st.selectbox("Select new medal", ["Gold", "Silver", "Bronze"])
        if st.button("Update Details"):
            update_medal(medal_id, name, noc, sport, event, medal)
            st.success("Medal details updated successfully!")


if __name__ == "__main__":
    medal_data()