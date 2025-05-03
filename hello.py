from preswald import text, table, plotly, connect, get_df, selectbox, slider, sidebar
import plotly.express as px
import pandas as pd

# 🌐 Sidebar Initialization
sidebar(defaultopen=True)

# 🔌 Connect to Dataset
connect()
df = get_df("video_game_sales")

# text(f"""# 🎮 **Video Game Sales Explorer**
# Use the sidebar to select a game genre and set a minimum global sales threshold to explore relevant video game sales data interactively.
# """)


# 🧹 Data Cleaning
df = df.dropna(subset=["Name", "Year", "Genre", "Global_Sales"])
df["Global_Sales"] = pd.to_numeric(df["Global_Sales"], errors="coerce")

# 🎮 Dropdown for Genre Selection
unique_genres = sorted(df["Genre"].unique())
selected_genre = selectbox("🎯 Choose a Game Genre", options=unique_genres, default=unique_genres[0])

# 📊 Slider for Sales Filter
min_sales = slider("💰 Minimum Global Sales (in Millions)", min_val=0, max_val=50, step=1, default=10)

# 🔍 Data Filtering Based on Selections
filtered_df = df[(df["Genre"] == selected_genre) & (df["Global_Sales"] >= min_sales)]

# 🧾 Beautiful Header
text(f"""
# 🎮 **Video Game Sales Explorer**
### 📂 Genre: **{selected_genre}**  
### 📈 Minimum Global Sales: **≥ {min_sales}M**
""")

# 🧠 Show Equivalent SQL Query
sql_query = f"""
SELECT * FROM video_game_sales
WHERE Genre = '{selected_genre}'
AND Global_Sales >= {min_sales}
"""

text("### 🧠 Equivalent SQL Query")
text(f"""```sql
{sql_query}
```""")


# 📈 Interactive Scatter Plot
fig = px.scatter(
    filtered_df,
    x="Year",
    y="Global_Sales",
    # text="Name",
    hover_name="Name",
    color="Platform",
    hover_data={"Global_Sales": True, "Year": True, "Platform": True},
    labels={
        "Year": "Release Year",
        "Global_Sales": "Global Sales (Millions)",
        "Name": "Game Title",
        "Platform": "Gaming Platform"
    },
    title=f"📊 Global Sales Trend for '{selected_genre}' Games (≥ {min_sales}M)",
    template="plotly_white"
)

fig.update_traces(marker=dict(size=12, opacity=0.7), textposition='top center')
fig.update_layout(
    title_font_size=20,
    margin=dict(l=40, r=40, t=80, b=40),
    xaxis=dict(tickangle=0),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)

# 📉 Display Plot
plotly(fig)

# 🧾 Display Table of Filtered Results
text("### 📋 Top 20 Games Matching Your Filter")
table(filtered_df.sort_values("Global_Sales", ascending=False).head(20))