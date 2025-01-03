import pandas as pd
import streamlit as st

# st.write("Hello World")
# x = st.text_input("Favorite Movie?")
# st.write(f"Your favorite movie is {x}")

data = pd.read_csv("movies.csv")
st.write(data)