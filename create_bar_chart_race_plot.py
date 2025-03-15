from create_bar_chart_race_data import CreateBarChartRaceData
import pandas as pd
import plotly.express as px
from raceplotly.plots import barplot

create_bar_chart_race_data = CreateBarChartRaceData()

# votes
cumulative_votes_by_time_candidate = create_bar_chart_race_data.create_cumulative_votes_by_time_candidate()
early_collected = cumulative_votes_by_time_candidate[cumulative_votes_by_time_candidate['collected_at'] < pd.to_datetime('2024-01-13 17:30')]
max_cumulative_votes = early_collected['cumulative_sum_votes'].max()

# plot with plotly.express
fig = px.bar(early_collected,
             x='cumulative_sum_votes', y='candidate', color='candidate',
             color_discrete_map={'侯友宜/趙少康':'#00009E', '柯文哲/吳欣盈':'#5AB0B2', '賴清德/蕭美琴':'#429329'},
             animation_frame='collected_at', animation_group='candidate',
             range_x=[0,max_cumulative_votes],template='seaborn')
fig.update_traces(width=.5)
fig.show()

# plot with raceplotly.plots
vote_raceplot = barplot(early_collected, item_column='candidate', value_column='cumulative_sum_votes',
                         time_column='collected_at', top_entries=3, item_color= {'賴清德/蕭美琴':'rgb(66,147,41)','侯友宜/趙少康':'rgb(0,0,158)', '柯文哲/吳欣盈':'rgb(90,176,178)'})
fig = vote_raceplot.plot(item_label='Votes collected by candidate', value_label='Cumulative votes', frame_duration=50)
fig.write_html('bar_chart_race_votes.html')


# covid_19_confirmed
covid_19_confirmed = create_bar_chart_race_data.create_covid_19_confirmed()
max_confirmed = covid_19_confirmed['confirmed'].max()

# plot with plotly.express
fig = px.bar(covid_19_confirmed,
             x='confirmed', y='country', color='country',
             color_discrete_sequence=px.colors.qualitative.Antique,
             animation_frame='reported_on', animation_group='country',
             range_x=[0,max_confirmed],template='seaborn')
fig.update_yaxes(categoryorder='total ascending')
fig.show()

# plot with raceplotly.plots
confirmed_raceplot = barplot(covid_19_confirmed, item_column='country', value_column='confirmed',
                         time_column='reported_on')
fig = confirmed_raceplot.plot(item_label='Confirmed by country', value_label='Number of cases', frame_duration=50)
fig.write_html('bar_chart_race_confirmed.html')