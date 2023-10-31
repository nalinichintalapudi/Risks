import streamlit as st
import pandas as pd
import plotly.express as px

# Function to get data from Excel
@st.cache
def get_data_from_excel():
    df = pd.read_excel("causes.xlsx", engine="openpyxl", sheet_name="causes", usecols="A:H", nrows=818)
    return df

# Set the Streamlit app theme to light

st.set_page_config(page_title="Causes", page_icon=":bar_chart:", layout="centered")

# Load the data using the function
df = get_data_from_excel()

# Load the data using the function
df = get_data_from_excel()

# Add filter widgets for "Cause", "Age", "Country", and "Rank" in the four columns
Risk = st.multiselect("Select the  Risk Factor:", options=df["Risk"].unique(), default=df["Risk"].unique())

col1, col2, col3 = st.columns(3)

# Get the unique age values
age_options = sorted(df["Age"].unique())

# Define the indices to hide
indices_to_hide = [1, 3, 5, 7]

# Create a filtered list of age options without the specified indices
filtered_age_options = [age for index, age in enumerate(age_options) if index not in indices_to_hide]

with col1:
    Age = st.selectbox("Select an Age:", options=filtered_age_options, index=0)

with col2:
    Nationality = st.selectbox("Select a Nationality:", options=sorted(df["Nationality"].unique()), index=0)

with col3:
    Rank = st.selectbox("Select a Rank:", options=sorted(df["Rank"].unique()), index=2)

# Filter the data based on user selections
df_selection = df.query(
    "Risk==@Risk & Age==@Age & Rank==@Rank & Nationality==@Nationality"
)



title = f"Risk Factors, {Rank}"
st.markdown(f"<h3 style='black: red;text-align: center'> {title}</h3>", unsafe_allow_html=True)

if not df_selection.empty:
    # Create a bar chart with 'Age' as a subplot
    fig = px.bar(df_selection, x='Nationality', y='Count', color='Risk', text='Prevalence')

    # Set custom data for the hover label
    customdata = df_selection[['Nationality', 'Age', 'Risk', 'Rank']]
    fig.update_traces(customdata=customdata)

    # Define the hovertemplate with dynamic data
    hovertemplate = "<b>2022</b><br><b>Nationality</b>: %{customdata[0]}<br><b>Rank</b>: %{customdata[3]}<br><b>Age</b>: %{customdata[1]}<br><b>Prevalence</b>: %{text}"
    fig.update_traces(hovertemplate=hovertemplate)
    
    # Adjust the width of the bars to center-align them
    fig.update_traces(selector=dict(line=dict(width=3)) )  # Adjust the 'width' as needed
    fig.update_traces(hoverlabel_font_size=10, hoverlabel_bgcolor='white')
     
    left, middle, right = st.columns((1, 10, 1))
    with middle:
        st.write(fig, use_container_width=True)
else:
    st.warning('No data available for the selected options.')


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)



