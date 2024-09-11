from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px


# clean data
df = (
    pd.read_csv('games.csv')
    .replace('tbd', pd.NA)
    .dropna()
    .query("Year_of_Release>=2000 and Year_of_Release<2022"))
# remove rows with 'RP' ('Rating Pending') in the 'Rating' column and 'tbd' ('to be determined') in any column
# because these data gaps influences the overall metrics.
df = df[df['Rating'] != 'RP']

# constants for layout visuals
all_games_number = df.shape[0]
df["User_Score"] = pd.to_numeric(df["User_Score"], errors='coerce')
all_average_user_score = round(df["User_Score"].mean(numeric_only=True),2)
df["Critic_Score"] = pd.to_numeric(df["Critic_Score"], errors='coerce')
all_average_critic_score = df["Critic_Score"].mean(numeric_only=True)
platforms_list = df["Platform"].unique().tolist()
genres_list = df["Genre"].unique().tolist()
genres_color_sequence = px.colors.qualitative.Plotly
genres_color_map = {genre: genres_color_sequence[i % len(genres_color_sequence)] for i, genre in enumerate(genres_list)}

# initialize the dashboard app
app = Dash(meta_tags=[{"content": "width=device-width"}])

# dashboard layout
app.layout = html.Div(style={'backgroundColor': '#0F0F0F',
                             'color': 'black',
                             'padding': '20px'},
                      children=[
                          html.Div(children=[
                              html.H4(
                                  "Analysis of the gaming industry based on games released from 2000 to 2022",
                                  style={
                                      'width': '100%',
                                      'margin-bottom': '5px',
                                      'margin-top': '0px',
                                      'padding': '0px',
                                      'textAlign': 'center',
                                      'color': '#CECCE3',
                                      'fontSize': 35
                                  }
                              ),
                              html.Div(
                                  children=[
                                      html.Div(
                                          children=[
                                              dcc.Markdown(
                                                  '''
                                                  
                                                  #### 1. **Filters**
                                                  - **Platforms:** 
                                                      - Select one or more platforms.
                                                      - If not selected, all available ones are used.
                                                  - **Genres:** 
                                                      - Select one or more genres.
                                                      - If not selected, all available genres are used.
                                                  - **Year of release:**
                                                      - Select the start and end years.
                                                      - If not selected, the entire period (2000-2022) is analysed.
                                                  ''',
                                                  style={
                                                      'color': '#CECCE3',
                                                      'fontSize': 14,
                                                      'margin-bottom': '5px',
                                                      'margin-top': '0px',
                                                      'padding': '0px'
                                                  }
                                              )
                                          ],
                                          style={
                                              'width': '30%',
                                              'margin-bottom': '5px',
                                              'margin-top': '0px',
                                              'padding': '0px',
                                              'box-sizing': 'border-box'
                                          }
                                      ),
                                      html.Div(
                                          children=[
                                              dcc.Markdown(
                                                  '''
                                                  #### 2. **Metrics**
                                                  - **Total number of games:** 
                                                      - Displays the number of games matching the selected filters.
                                                  - **Total Average Player Rating:** 
                                                      - Shows the average player rating for the selected games.
                                                  - **Total Average Critics Rating:** 
                                                      - Displays the average critic rating for the selected games.

                                                  ''',
                                                  style={
                                                      'color': '#CECCE3',
                                                      'fontSize': 14,
                                                      'margin-bottom': '5px',
                                                      'margin-top': '0px',
                                                      'padding': '0px',
                                                  }
                                              )
                                          ],
                                          style={
                                              'width': '30%',
                                              'margin-bottom': '5px',
                                              'margin-top': '0px',
                                              'padding': '0px',
                                              'box-sizing': 'border-box'
                                          }
                                      ),
                                      html.Div(
                                          children=[
                                              dcc.Markdown(
                                                  '''
                                      
                                                  #### 3. **Graphs**
                                                  - **Graph of the number of games released by year and platform.** 
                                                  - **Point chart of the relationship between player and critic ratings by genre.** 
                                                  - **Histogram of average age rating by genre.** 
                                                  ''',
                                                  style={
                                                      'color': '#CECCE3',
                                                      'fontSize': 14,
                                                      'margin-bottom': '5px',
                                                      'margin-top': '0px',
                                                      'padding': '0px',
                                                  }
                                              )
                                          ],
                                          style={
                                              'width': '30%',
                                              'margin-bottom': '5px',
                                              'margin-top': '0px',
                                              'padding': '0px',
                                              'box-sizing': 'border-box'
                                          }
                                      ),
                                  ],
                                  style={
                                      'display': 'flex',
                                      'justify-content': 'space-between',
                                      'align-items': 'flex-start',
                                      'width': '100%',
                                      'margin-bottom': '5px',
                                      'margin-top': '0px',
                                      'padding': '0px',
                                  })
                          ],
                              style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center',
                                     'margin-bottom': '5px',
                                     'margin-top': '0px',
                                     'padding': '0px',
                                     }
                          ),

                                html.Div(children=[
                                    html.Div(
                                        dcc.Dropdown(
                                            id='platforms',
                                            options=[{'label': platform, 'value': platform} for platform in
                                                     platforms_list],
                                            placeholder="Select platform(s)",
                                            multi=True,
                                            value=None,
                                            style={'backgroundColor': '#1e1e1e','borderColor': '#CECCE3'}
                                        ), style={'flex': '2',
                                                  'margin-right': '10px',
                                                  'width': '48%'}
                                    ),
                                    html.Div(
                                        dcc.Dropdown(
                                            id='genres',
                                            options=[{'label': genre, 'value': genre} for genre in genres_list],
                                            placeholder="Select genre(s)",
                                            multi=True,
                                            value=None,
                                            style={'backgroundColor': '#1e1e1e','borderColor': '#CECCE3'}
                                        ), style={'flex': '2', 'margin-right': '10px', 'width': '48%'}
                                    ),
                                    html.Div(children=[
                                        dcc.Dropdown(
                                            id='start-year',
                                            options=[{'label': str(year), 'value': year} for year in range(2000, 2023)],
                                            placeholder="Select start year",
                                            style={'backgroundColor': '#1e1e1e',
                                                   'flex': '1',
                                                   'margin-right': '10px',
                                                   'borderColor': '#CECCE3'}
                                        ),
                                        dcc.Dropdown(
                                            id='end-year',
                                            options=[{'label': str(year), 'value': year} for year in range(2000, 2023)],
                                            placeholder="Select end year",
                                            style={'backgroundColor': '#1e1e1e','borderColor': '#CECCE3','flex': '1'}
                                        )
                                    ],
                                        style={'display': 'flex', 'flex': '2'}

                                )],
                                style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center', 'margin-bottom': '20px'}
                                ),
                                html.Div([
                                    html.Div([
                                        html.H6(children='Total Number of Games',
                                                style={'textAlign': 'center',
                                                       'color': '#CECCE3',
                                                       'fontSize': 20,
                                                       'margin-bottom': '5px',
                                                       'margin-top': '0px',
                                                       'padding': '0px'
                                                       }
                                                ),

                                        html.P(id='games_number',children=str(all_games_number),
                                               style={'textAlign': 'center',
                                                      'color': '#CECCE3',
                                                      'fontSize': 40,
                                                      'margin-bottom': '5px',
                                                      'margin-top': '0px',
                                                      'padding': '0px'
                                                      }
                                               )
                                    ],
                                        style={'width': '33%', 'display': 'inline-block'}
                                    ),
                                    html.Div([
                                        html.H6(children='Total Average Player Rating',
                                                style={
                                                    'textAlign': 'center',
                                                    'color': '#CECCE3',
                                                    'fontSize': 20,
                                                    'margin-bottom': '5px',
                                                    'margin-top': '0px',
                                                    'padding': '0px'
                                                }
                                                ),

                                        html.P(id='average-user-score',children=str(all_average_user_score),
                                               style={
                                                   'textAlign': 'center',
                                                   'color': '#CECCE3',
                                                   'fontSize': 40,
                                                   'margin-bottom': '5px',
                                                   'margin-top': '0px',
                                                   'padding': '0px'
                                               }
                                               )
                                    ],
                                    style={'width': '33%', 'display': 'inline-block'}
                                    ),
                                    html.Div([
                                        html.H4(children='Total Average Critics Rating',
                                                style={
                                                    'textAlign': 'center',
                                                    'color': '#CECCE3',
                                                    'fontSize': 20,
                                                    'margin-bottom': '5px',
                                                    'margin-top': '0px',
                                                    'padding': '0px'
                                                }
                                                ),

                                        html.P(id='average-critic-score',children=str(all_average_critic_score),
                                               style={
                                                   'textAlign': 'center',
                                                   'color': '#CECCE3',
                                                   'fontSize': 40,
                                                   'margin-bottom': '5px',
                                                   'margin-top': '0px',
                                                   'padding': '0px'
                                               }
                                               )
                                    ],
                                    style={'width': '33%',
                                           'display': 'inline-block',}
                                    )],
                                    className="row flex-display"),
                                html.Div([
                                    dcc.Graph(id="stacked-area-plot",
                                              style={'width': '32%',
                                                     'display': 'inline-block',
                                                     'backgroundColor': '#CECCE3',
                                                     'margin-bottom': '5px',
                                                     'margin-top': '0px',
                                                     'padding': '1px',
                                                     }),
                                    dcc.Graph(id="scatter-plot",
                                              style={'width': '32%',
                                                     'display': 'inline-block',
                                                     'backgroundColor': '#CECCE3',
                                                     'margin-bottom': '5px',
                                                     'margin-top': '0px',
                                                     'padding': '1px',
                                                     }),
                                    dcc.Graph(id="bar-chart",
                                              style={'width': '32%',
                                                     'display': 'inline-block',
                                                     'backgroundColor': '#CECCE3',
                                                     'margin-bottom': '5px',
                                                     'margin-top': '0px',
                                                     'padding': '1px'
                                                     })],
                                    style={
                                        'display': 'flex',
                                        'justify-content': 'space-between',
                                        'align-items': 'flex-start',
                                        'width': '100%',
                                        'margin-bottom': '5px',
                                        'margin-top': '0px',
                                        'padding': '0px',
                                    })

                                ])


# define a function for filtering the dataset based on selected filters
def apply_filters(selected_platforms,
                  selected_genres,
                  selected_start_year,
                  selected_end_year):
    if not selected_platforms and not selected_genres and not selected_start_year and not selected_end_year:
        return df.copy()

    if not selected_platforms:
        selected_platforms = df['Platform'].unique()

    if not selected_genres:
        selected_genres = df['Genre'].unique()

    if not selected_start_year:
        selected_start_year = '2000'

    if not selected_end_year:
        selected_end_year = '2022'

    if isinstance(selected_platforms, str):
        selected_platforms = [selected_platforms]

    if isinstance(selected_genres, str):
        selected_genres = [selected_genres]

    filtered_df_by_platform = df[df['Platform'].isin(selected_platforms)]
    filtered_df_by_platform_genre = filtered_df_by_platform[filtered_df_by_platform['Genre'].isin(selected_genres)]
    filtered_df_by_platform_genre_year = (
        filtered_df_by_platform_genre.query(f"Year_of_Release>={selected_start_year} and Year_of_Release<={selected_end_year}"))
    if filtered_df_by_platform_genre_year.empty:
        return pd.DataFrame()
    return filtered_df_by_platform_genre_year.copy()

# define callback for the 'Total Number of Games' metric
@callback(
    Output(component_id='games_number', component_property='children'),
    Input(component_id='platforms', component_property='value'),
    Input(component_id='genres', component_property='value'),
    Input(component_id='start-year', component_property='value'),
    Input(component_id='end-year', component_property='value'),
)
def apply_filters_to_games_number(selected_platforms,
                                  selected_genres,
                                  selected_start_year,
                                  selected_end_year):
    # call the apply_filters() function that returns filtered dataset
    filtered_df_by_platform_genre_year = apply_filters(selected_platforms,
                                                       selected_genres,
                                                       selected_start_year,
                                                       selected_end_year)

    # handle the case where the returned dataset is empty
    if filtered_df_by_platform_genre_year.empty:
        return str(0)

    # calculate the metric
    games_number = filtered_df_by_platform_genre_year.shape[0]
    return str(games_number)

# define callback for the 'Total Average Player Rating' metric
@callback(
    Output(component_id='average-user-score', component_property='children'),
    Input(component_id='platforms', component_property='value'),
    Input(component_id='genres', component_property='value'),
    Input(component_id='start-year', component_property='value'),
    Input(component_id='end-year', component_property='value'),
)
def apply_filters_to_average_user_score(selected_platforms,
                                        selected_genres,
                                        selected_start_year,
                                        selected_end_year):
    filtered_df_by_platform_genre_year = apply_filters(selected_platforms,
                                                       selected_genres,
                                                       selected_start_year,
                                                       selected_end_year)

    if filtered_df_by_platform_genre_year.empty:
        return str(0)

    filtered_df_by_platform_genre_year["User_Score"] = pd.to_numeric(filtered_df_by_platform_genre_year["User_Score"],
                                                                     errors='coerce')
    average_user_score = round(filtered_df_by_platform_genre_year["User_Score"].mean(), 2)
    return str(average_user_score)

# define callback for the 'Total Average Critic Rating' metric
@callback(
    Output(component_id='average-critic-score', component_property='children'),
    Input(component_id='platforms', component_property='value'),
    Input(component_id='genres', component_property='value'),
    Input(component_id='start-year', component_property='value'),
    Input(component_id='end-year', component_property='value'),
)
def apply_filters_to_average_critic_score(selected_platforms,
                                        selected_genres,
                                        selected_start_year,
                                        selected_end_year):
    filtered_df_by_platform_genre_year = apply_filters(selected_platforms,
                                                       selected_genres,
                                                       selected_start_year,
                                                       selected_end_year)

    if filtered_df_by_platform_genre_year.empty:
        return str(0)

    filtered_df_by_platform_genre_year["Critic_Score"] = pd.to_numeric(filtered_df_by_platform_genre_year["Critic_Score"],
                                                                     errors='coerce')
    average_critic_score = round(filtered_df_by_platform_genre_year["Critic_Score"].mean(), 2)
    return str(average_critic_score)


# define callback for the 'Number of games released by Year and Platform' stacked area plot
@callback(
    Output(component_id="stacked-area-plot", component_property="figure"),
    Input(component_id='platforms', component_property='value'),
    Input(component_id='genres', component_property='value'),
    Input(component_id='start-year', component_property='value'),
    Input(component_id='end-year', component_property='value'),
)
def display_stacked_area_plot(selected_platforms,
                              selected_genres,
                              selected_start_year,
                              selected_end_year):
    filtered_df_by_platform_genre_year = apply_filters(selected_platforms,
                                                       selected_genres,
                                                       selected_start_year,
                                                       selected_end_year)
    if filtered_df_by_platform_genre_year.empty:
        fig = px.area(title="No data")
        fig.update_layout(
            paper_bgcolor='#1e1e1e',
            plot_bgcolor='#1e1e1e',
            font=dict(color='#CECCE3'),
            xaxis_title_font=dict(color='#CECCE3'),
            yaxis_title_font=dict(color='#CECCE3'),
            title_font=dict(color='#CECCE3'))
        return fig

    grouped_df = filtered_df_by_platform_genre_year.groupby(['Year_of_Release', 'Platform']).size().reset_index(
        name='Game_Count')
    fig = px.area(grouped_df,
                  x="Year_of_Release",
                  y="Game_Count",
                  color="Platform",
                  color_discrete_sequence=px.colors.qualitative.G10,
                  labels={"Game_Count": "Number of games", "Year_of_Release": "Year of release"},
                  markers=True,
                  title="Number of games released by Year and Platform")
    fig.update_layout(
        paper_bgcolor='#1e1e1e',
        plot_bgcolor='#1e1e1e',
        font=dict(color='#CECCE3'),
        xaxis_title_font=dict(color='#CECCE3'),
        yaxis_title_font=dict(color='#CECCE3'),
        title_font=dict(color='#CECCE3',size=15))

    return fig

# define callback for the 'Relationship between player and critic scores by genre' scatter plot
@callback(
    Output(component_id="scatter-plot", component_property="figure"),
    Input(component_id='platforms', component_property='value'),
    Input(component_id='genres', component_property='value'),
    Input(component_id='start-year', component_property='value'),
    Input(component_id='end-year', component_property='value'),
)
def display_scatter_plot(selected_platforms,
                              selected_genres,
                              selected_start_year,
                              selected_end_year):
    filtered_df_by_platform_genre_year = apply_filters(selected_platforms,
                                                       selected_genres,
                                                       selected_start_year,
                                                       selected_end_year)
    if filtered_df_by_platform_genre_year.empty:
        fig = px.scatter(title="No data")
        fig.update_layout(
            paper_bgcolor='#1e1e1e',
            plot_bgcolor='#1e1e1e',
            font=dict(color='#CECCE3'),
            xaxis_title_font=dict(color='#CECCE3'),
            yaxis_title_font=dict(color='#CECCE3'),
            title_font=dict(color='#CECCE3'))
        return fig

    fig = px.scatter(filtered_df_by_platform_genre_year,
                     x="User_Score",
                     y="Critic_Score",
                     color="Genre",
                     color_discrete_map=genres_color_map,
                     hover_name="Name",
                     labels={"Name": "Name", "User_Score": "User Score", "Critic_Score": "Critic Score", "Genre": "Genre"},
                     title="Relationship between player and critic scores by genre",
                     )
    fig.update_layout(
        paper_bgcolor='#1e1e1e',
        plot_bgcolor='#1e1e1e',
        font=dict(color='#CECCE3'),
        xaxis_title_font=dict(color='#CECCE3'),
        yaxis_title_font=dict(color='#CECCE3'),
        title_font=dict(color='#CECCE3',size=13))
    return fig

# define callback for the 'Average Age Rating by genre' bar chart
@callback(
    Output(component_id="bar-chart", component_property="figure"),
    Input(component_id='platforms', component_property='value'),
    Input(component_id='genres', component_property='value'),
    Input(component_id='start-year', component_property='value'),
    Input(component_id='end-year', component_property='value'),
)
def display_bar_chart(selected_platforms,
                              selected_genres,
                              selected_start_year,
                              selected_end_year):
    filtered_df_by_platform_genre_year = apply_filters(selected_platforms,
                                                       selected_genres,
                                                       selected_start_year,
                                                       selected_end_year)
    if filtered_df_by_platform_genre_year.empty:
        fig = px.bar(title="No data")
        fig.update_layout(
            paper_bgcolor='#1e1e1e',
            plot_bgcolor='#1e1e1e',
            font=dict(color='#CECCE3'),
            xaxis_title_font=dict(color='#CECCE3'),
            yaxis_title_font=dict(color='#CECCE3'),
            title_font=dict(color='#CECCE3'))
        return fig

    rating_to_age = {
        'AO': 18,
        'M': 17,
        'T': 13,
        'E10+': 10,
        'E': 6,
        'K-A': 6,
        'EC': 3
    }

    filtered_df_by_platform_genre_year['Age_Rating'] = filtered_df_by_platform_genre_year['Rating'].map(rating_to_age)
    # Group by Genre and calculate the average age rating
    average_age_rating = (filtered_df_by_platform_genre_year
                          .groupby('Genre')['Age_Rating']
                          .mean()
                          .reset_index()
                          .sort_values(by='Age_Rating'))
    average_age_rating['Age_Rating'] = average_age_rating['Age_Rating'].astype(int)

    fig = px.bar(average_age_rating,
                 x='Genre',
                 y='Age_Rating',
                 labels={'Genre':'Genre','Age_Rating': 'Age'},
                 title='Average Age Rating by genre',
                 text='Age_Rating',
                 color='Genre',
                 color_discrete_map=genres_color_map)
    fig.update_layout(
        paper_bgcolor='#1e1e1e',
        plot_bgcolor='#1e1e1e',
        font=dict(color='#CECCE3'),
        xaxis_title_font=dict(color='#CECCE3'),
        yaxis_title_font=dict(color='#CECCE3'),
        title_font=dict(color='#CECCE3',size=15)
    )

    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)