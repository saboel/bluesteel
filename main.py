import requests as r 
import pandas as pd


def fetch_team_roster(team_id):
    url = f'https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}?enable=roster'
    response = r.get(url)
    try: 
        response.raise_for_status()  # Check for HTTP errors
        return response.status_code, response.json()
    except r.HTTPError as e:
        print(f"HTTP Error: {response.status_code} - {response.text}")  # Print status code and error text
        return None, None  # Return None for both status code and data
    except Exception as e: 
          print(f"Error: {e}")  # Print the error if it occurs 
          return None, None 



def fetch (url): 
    response = r.get(url) 
    try: 
        response.raise_for_status()  # Check for HTTP errors
        return response.status_code, response.json()
    except r.HTTPError as e:
        print(f"HTTP Error: {response.status_code} - {response.text}")  # Print status code and error text
        return None, None  # Return None for both status code and data
    except Exception as e: 
          print(f"Error: {e}")  # Print the error if it occurs 
          return None, None 

# Function to extract the first injury's status and shortComment
def extract_injury_info(injury_list):
    if isinstance(injury_list, list) and len(injury_list) > 0:
        first_injury = injury_list[0]  # Get the first injury
        return first_injury.get('status'), first_injury.get('shortComment'), first_injury.get('date')
    return None, None  # Return None if no injuries
    


def main (): 
    api_url = 'http://site.api.espn.com/apis/site/v2/sports/football/nfl/teams'
    status_code, data = fetch(api_url)
    team_map = {}
    player_map = {}
    player_info = {}


###### List of Dicts 

    if 'sports' in data and isinstance(data['sports'], list) and len(data['sports']) > 0:
        leagues = data['sports'][0].get('leagues', [])
        teams = leagues[0].get('teams', [])  # Default to an empty list if 'teams' doesn't exist
        for team in teams:
            if isinstance(team, dict):
                team_data = team['team']
                team_name = team_data.get('name', 'Unknown')
                team_id  = team_data.get('id', 'Unknown')
                team_map[team_name] = team_id
             ##   print(f"Processing team: {team_name} (ID: {team_id})") troubleshooting
    
    ##print(team_map)
    ##print(team_map.get('Texans'))
    team_name = 'Texans'  # Replace with the desired team name
    team_id = team_map.get(team_name)
    print(team_id)
    status_code, roster = fetch_team_roster(team_id)



#### dict of lists     
    if roster:
        ##print(roster)  # Print the entire roster; customize this as needed
        team = roster.get('team', {})      
        athletes = team.get('athletes', [])  # Access the athletes list
        player_df = pd.DataFrame(athletes)  # Create DataFrame from the list of athletes
        pd.set_option('display.max_rows', None)  # None means display all rows
        player_df['birthplace_city'] = player_df['birthPlace'].apply(lambda x: x.get('city') if isinstance(x, dict) else None)
        player_df[['injury_status', 'injury_comment','date']] = player_df['injuries'].apply(extract_injury_info).apply(pd.Series)
        player_df['position'] = player_df['position'].apply(lambda x: x.get('abbreviation') if isinstance(x, dict) else None)
        selected_columns = ['id', 'displayName', 'displayHeight', 'displayWeight', 'age', 'birthplace_city', 'position']  # Specify the columns you want
        all_player_info = player_df[selected_columns]

        #    Filter players who are injured
        injured_players = player_df[player_df['injury_status'].isin (['Questionable', 'Injured Reserve', 'Out'])]  # Adjust 'Injured' as necessary based on your data
        merged_df = pd.merge(all_player_info, injured_players, on='id', how='inner')
        ##print(merged_df.columns)
        filtered_column = ['displayName_x','injury_status',  'injury_comment', 'date']

        # Create a new DataFrame with only the selected columns
        filtered_df = merged_df[filtered_column]
        sorted_df = filtered_df.sort_values(by='date', ascending=False)

        print(sorted_df)


  

if __name__ == '__main__':
    main()


##Store all players into the player_map of all teams 
##We include the team id in that map so we can distinguish players based on that 