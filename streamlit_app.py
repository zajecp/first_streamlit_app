import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.header('🥣Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal🥑')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg🐔')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Grapes','Orange'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

# get fruit data from API
def ger_fruit_data(local_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + local_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())  
    return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select fruit")
  else:
    streamlit.dataframe(ger_fruit_data(fruit_choice))

except URLError as e:
  streamlit.error()


streamlit.header("The Fruit Load List")
def get_fruit_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()

if streamlit.button('Get fruit list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_list()
    streamlit.dataframe(my_data_rows)







