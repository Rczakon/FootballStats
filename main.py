from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Match import Match
from Team import Team

leagues = ["Jupiler Pro League", "Premier League", "Bundesliga", "Ekstraklasa"]

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

driver.get("https://www.flashscore.com/")


wanted_leagues = ['Ligue 1', 'Serie A', 'LaLiga']
team_list = []

string = '//*[@id="g_1_xABkClNH"]'
event_ids = []

todays_matches_list = []


# This function gets all ids, adds them to a list and proceed with actions on teams
def get_match_details():
    current_league = driver.find_element(By.CLASS_NAME, "event__header")
    matches = driver.find_elements(By.CLASS_NAME, "event__match")
    # Next day button class: calendar__direction--tomorrow
    for match in matches:
        event_ids.append(match.get_attribute("id")[4:])
    get_all_teams()
    for team in team_list:
        team.calculate_avg_goals()
    team_list.sort(key=lambda x: x.avg_goals_in_last5, reverse=True)
    for team in team_list:
        print(team.name + " avg: " + str(team.avg_goals_in_last5))

# First version of getting the matches by a team
def get_all_h2h_matches(event_id):
    # Creating link based on passed event id
    match_link = "https://www.flashscore.com/match/" + event_id + "/#h2h/overall"
    # Accessing website
    driver.get(match_link)
    # Finding all elements with given class name
    participants = driver.find_elements(By.CLASS_NAME, "participant__participantName")
    # Printing both teams of the match being checked(both appear twice, host: 0, 1 guests: 2, 3)
    print(participants[1].text + " - " + participants[2].text)
    # Getting participants in every h2h match
    h2h_participants = driver.find_elements(By.CLASS_NAME, "h2h__participantInner")
    # Getting all h2h results
    h2h_results = driver.find_elements(By.CLASS_NAME, "h2h__regularTimeResult")
    # Showing length of participants list
    print(len(h2h_participants))
    # Printing all h2h matches with result
    for x in range(0, len(h2h_participants), 2):
        result_index = int(x / 2)
        print(h2h_participants[x].text + " " + h2h_results[result_index].text + " " + h2h_participants[x+1].text)


# This function created Team objects for every team with corresponding matches by analyzing sections in the h2h tab
def get_h2h_matches_by_section(event_id):
    # Creating link based on passed event id
    match_link = "https://www.flashscore.com/match/" + event_id + "/#h2h/overall"
    # Accessing website
    driver.get(match_link)
    # Getting access to the league information
    current_league = driver.find_element(By.CLASS_NAME, "tournamentHeader__country").text
    # Getting access to the element showing if the match is postponed/finished
    status_content = driver.find_element(By.CLASS_NAME, "detailScore__status").text
    print(status_content)
    if status_content == "FINISHED" or status_content == "POSTPONED":
        match_status = "incorrect"
    else:
        match_status = "correct"
    if match_status == "correct" and "Club Friendly" not in current_league:
        # Finding all elements with given class name
        participants = driver.find_elements(By.CLASS_NAME, "participant__participantName")
        # Printing both teams of the match being checked(both appear twice, host: 0, 1 guests: 2, 3)
        hosts = participants[1].text
        guests = participants[2].text
        # Creating new Team objects and adding them to a list
        team1 = Team(hosts)
        team2 = Team(guests)
        # Getting all h2h sections as a list
        h2h_sections = driver.find_elements(By.CLASS_NAME, "h2h__section")
        # Creating list with all sections and their matches
        h2h_sections_list = []
        h2h_results = []
        match_list = []
        # Getting all matches by section
        for section in h2h_sections:
            h2h_sections_list.append(section.find_elements(By.CLASS_NAME, "h2h__participant"))
        # Getting all h2h results
        for section in h2h_sections:
            h2h_results.append(section.find_elements(By.CLASS_NAME, "h2h__result"))
        # Printing matches with results
        # Printing all h2h matches by section
        for section in h2h_sections_list:
            for x in range(0, len(section), 2):
                result_index = int(x / 2)
                section_index = h2h_sections_list.index(section)
                new_match = Match(section[x].text, section[x+1].text, h2h_results[section_index][result_index].text)
                match_list.append(new_match)
                # print(section[x].text + " " + h2h_results[section_index][result_index].text + " " + section[x+1].text)
                # Adding matches to corresponding team objects
                if h2h_sections_list.index(section) == 0:
                    team1.matches.append(new_match)
                if h2h_sections_list.index(section) == 1:
                    team2.matches.append(new_match)
        team_list.append(team1)
        team_list.append(team2)


# This function prints all the matches from the corresponding team
def show_team_matches(team):
    print(team.name + " matches:")
    for match in team.matches:
        print(match.team1 + " " + match.result + " " + match.team2)

# This function calls the get_h2h_matches_by_section() for every ID
def get_all_teams():
    for id in event_ids:
        get_h2h_matches_by_section(id)

def get_single_match(id):
    get_h2h_matches_by_section(event_ids[id])


get_match_details()

# Cele na dzisiaj:
# Nie brać pod uwagę przełożonych meczów: class fixedHeaderDuel__detailStatus
# Nie brać pod uwagę zakończonych meczów: class fixedHeaderDuel__detailStatus
# Nie brać pod uwagę meczów towarzyskich: class tournamentHeader__country (info o meczu towarzyskim jest w <a> wewnątrz a nie bezpośrednio!)