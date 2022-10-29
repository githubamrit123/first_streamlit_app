import streamlit
import pandas
from urllib.error import URLError
import requests
import snowflake.connector

streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Grapes','Avocado'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
# streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)


streamlit.header("Fruityvice Fruit Advice!")
#try:
fruit_choice = streamlit.text_input('What fruit would you like information about?')
#if not fruit_choice:
        streamlit.error("please select a fruit to get the information")
 #      error:  
            #streamlit.write('The user entered ', fruit_choice)
            #import requests
            fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
            # streamlit.text(fruityvice_response.json())
            fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
            streamlit.dataframe(fruityvice_normalized)
#except URLError as e:
 # streamlit.error()

streamlit.stop()
#import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)

my_cur.execute("Select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("Hello from Snowflake:")
streamlit.dataframe(my_data_rows)

fruit_choice = streamlit.text_input('What fruit would you like to add?','Kiwi')
streamlit.write('Thanks for adding  ', fruit_choice)

my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')")
