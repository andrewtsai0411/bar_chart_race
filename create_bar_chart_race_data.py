import sqlite3
import pandas as pd

class CreateBarChartRaceData:
    def adjust_datetome_format(self, x):
      date_part, time_part = x.split()
      date_part = '2024-01-13'
      datetime_iso_8601 = f'{date_part} {time_part}'
      return datetime_iso_8601
    
    def create_cumulative_votes_by_time_candidate(self):
      connection = sqlite3.connect('data/taiwan_presidential_election_2024.db')
      sql_query = '''
          SELECT pp.county,
                pp.polling_place,
                c.candidate,
                SUM(v.votes) AS sum_votes
            FROM votes v
            JOIN candidates c
              ON v.candidate_id = c.id
            JOIN polling_places pp
              ON v.polling_place_id = pp.id
          GROUP BY pp.county,
                  pp.polling_place,
                  c.candidate;'''
      votes_by_polling_place_candidate = pd.read_sql(con=connection, sql=sql_query)
      connection.close()

      votes_collected = pd.read_excel('data/113全國投開票所完成時間.xlsx', skiprows=[0,1,2])
      votes_collected.columns = ['county', 'town', 'polling_place', 'collected_at', 'number_of_voters']
      votes_collected = votes_collected[['county', 'town', 'polling_place', 'collected_at']]

      merged = votes_by_polling_place_candidate.merge(votes_collected, on=['county', 'polling_place'], how='left')

      # 每個時間點，每組候選人的得票數
      votes_by_collected_at_candidate = merged.groupby(['collected_at', 'candidate'])['sum_votes'].sum().reset_index()

      # cumulative sum
      cum_sum = votes_by_collected_at_candidate.groupby('candidate')['sum_votes'].cumsum()
      votes_by_collected_at_candidate['cumulative_sum_votes'] = cum_sum

      votes_by_collected_at_candidate['collected_at'] = votes_by_collected_at_candidate['collected_at'].apply(self.adjust_datetome_format)
      votes_by_collected_at_candidate['collected_at'] = pd.to_datetime(votes_by_collected_at_candidate['collected_at'])
      return votes_by_collected_at_candidate
    
    def create_covid_19_confirmed(self):
      connection = sqlite3.connect('data/covid_19.db')
      sql_query = '''
          SELECT reported_on,
                country,
                confirmed
            FROM time_series
            WHERE reported_on <= '2020-12-31';'''
      covid_19_confirmed = pd.read_sql(con=connection, sql=sql_query)
      connection.close()

      nlargest_index = covid_19_confirmed.groupby('reported_on')['confirmed'].nlargest(10).reset_index()['level_1']
      covid_19_confirmed = covid_19_confirmed.loc[nlargest_index, :].reset_index(drop=True)
      return covid_19_confirmed

create_bar_chart_race_data = CreateBarChartRaceData()
cumulative_votes_by_time_candidate = create_bar_chart_race_data.create_cumulative_votes_by_time_candidate()
covid_19_confirmed = create_bar_chart_race_data.create_covid_19_confirmed()