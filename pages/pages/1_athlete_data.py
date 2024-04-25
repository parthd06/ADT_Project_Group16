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

# CRUD operations for Team table


def create_team(name, sex, age, height, weight, team, noc, year, season):
    conn, c = create_connection()
    c.execute("INSERT INTO Team (Name, sex, Age, Height, Weight, Team, NOC, Year, season) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
              (name, sex, age, height, weight, team, noc, year, season))
    conn.commit()
    conn.close()


def read_teams():
    conn, c = create_connection()
    c.execute(
        "SELECT Athlete_id, Name, sex, Age, Height, Weight, Team, NOC, Year, season FROM Team")
    teams = c.fetchall()
    column_names = [description[0] for description in c.description]
    teams_with_column_names = [dict(zip(column_names, team)) for team in teams]
    conn.close()
    return teams_with_column_names

# Update operations
def edit_athlete(athlete_id, name, sex, age, height, weight, team, noc, year, season):
    conn, c = create_connection()
    c.execute("""UPDATE Team SET Name = %s, sex = %s, Age = %s, Height = %s, Weight = %s, Team = %s, NOC = %s, Year = %s, season = %s
    WHERE athlete_id = %s """, (name, sex, age, height, weight, team, noc, year, season, athlete_id))
    conn.commit()
    conn.close()

#Delete Operations
def delete_team(athlete_id):
    conn, c = create_connection()
    c.execute("DELETE FROM Team WHERE Athlete_id=%s", (athlete_id,))
    conn.commit()
    conn.close()


# Athlete Page
def athlete_data():
    st.title("Athlete Data")
    st.sidebar.write("### Navigate to perform Operations:")
    operation = st.sidebar.selectbox(
        "", ["Create Athlete", "Read Athletes", "Update Athlete", "Delete Athlete"])

    if operation == "Create Athlete":
        st.subheader("Create Athlete Data:")
        st.image('../images/Athletes_Icon.jpg', width=100)
        # Input fields for creating a new team
        name = st.text_input("Name")
        sex = st.selectbox("Sex", ["M", "F"])
        age = st.number_input("Age", min_value=13, max_value=150, value=13)
        height = st.number_input(
            "Height in Cm", min_value=0, max_value=300, value=0)
        weight = st.number_input(
            "Weight in Kg", min_value=0, max_value=500, value=0)
        team = st.text_input("Representing Country")
        noc = st.text_input("Team NOC")
        year = st.number_input("Year", value=2016)
        season = st.selectbox("Season", ["Summer", "Winter"])
        if st.button("Add Details"):
            create_team(name, sex, age, height, weight,
                        team, noc, year, season)
            st.success("Athlete details added successfully!")

    elif operation == "Read Athletes":
        st.header("Read Athlete details 📃")
        # Display existing athlete data
        teams = read_teams()
        if teams:
            st.table(teams)
        else:
            st.write("No details available.")

    elif operation == "Update Athlete":
        st.subheader("Update athlete details 📝:")
        athlete_id = st.text_input("Enter Athlete id")
        name = st.text_input("Enter new name")
        sex = st.selectbox("Sex", ["M", "F"])
        age = st.number_input("Age", min_value=13, max_value=150, value=13)
        height = st.number_input(
            "Height in Cm", min_value=0, max_value=300, value=0)
        weight = st.number_input(
            "Weight in Kg", min_value=0, max_value=500, value=0)
        team = st.text_input("Representing Country")
        noc = st.text_input("Team NOC")
        year = st.number_input("Year", value=2016)
        season = st.selectbox("Season", ["Summer", "Winter"])
        if st.button("Update Details"):
            edit_athlete(athlete_id, name, sex, age, height,
                         weight, team, noc, year, season)
            st.success("Athlete details updated successfully!")

    elif operation == "Delete Athlete":
        st.header("Delete Athlete Data")
        # Input field for deleting athlete data
        athlete_id = st.number_input("Athlete ID", min_value=1)
        if st.button("Delete Athlete"):
            delete_team(athlete_id)
            st.success("Athlete data deleted successfully!")


if __name__ == "__main__":
    athlete_data()
