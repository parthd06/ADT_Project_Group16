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

# CRUD operations for Events_2016 table
def create_event(event_name):
    conn, c = create_connection()
    c.execute("INSERT INTO Events_2016 (Event_Name) VALUES (%s)", (event_name,))
    conn.commit()
    conn.close()


def read_events():
    conn, c = create_connection()
    c.execute("SELECT Event_id, Event_Name FROM Events_2016")
    events = c.fetchall()
    column_names = [description[0] for description in c.description]
    events_with_column_names = [dict(zip(column_names, event)) for event in events]
    conn.close()
    return events_with_column_names

#Delete Operations
def delete_event(event_id):
    conn, c = create_connection()
    c.execute("DELETE FROM Events_2016 WHERE event_id=%s", (event_id,))
    conn.commit()
    conn.close()



# Event Page
def event_data():
    st.title("Events Data")
    st.sidebar.write("### Navigate to perform Operations:")
    operation = st.sidebar.selectbox(
        "", ["Create Sports event", "View existing Events", "Delete events"])

    if operation == "Create Sports event":
        st.subheader("Enter sport event details:")
        st.image('../images/events.webp', width= 350)
        # Input field for creating a new event
        event_name = st.text_input("Event type")
        if st.button("Add Event"):
            create_event(event_name)
            st.success("Event added successfully!")
        
    elif operation == "View existing Events":
        st.header("Show existing Events")
        # Display existing events
        events = read_events()
        if events:
            st.table(events)
        else:
            st.write("No events available.")

    elif operation == "Delete events":
        st.header("Delete existing Events")
        # Input field for deleting event data
        event_id = st.number_input("Event ID", min_value=1)
        if st.button("Delete event"):
            delete_event(event_id)
            st.success("Sports event deleted successfully!")


if __name__ == "__main__":
    event_data()