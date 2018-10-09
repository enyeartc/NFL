from bs4 import BeautifulSoup
from datetime import datetime
import requests
import numpy as np
import csv

from concurrent.futures import ThreadPoolExecutor

BASE_URL = "http://www.vegasinsider.com"
TRANSLATE = str.maketrans({'\n': '', '\t': '', '\r': '', '\xa0': ''})
COLUMN_TITLES = ['week', 'season', 'home_city', 'home_team', 'away_city', 'away_team', 'casino', 'date', 'favorite',
                 'fav_spread', 'fav_line', 'underdog', 'dog_spread', 'dog_line', 'over', 'over_line', 'under',
                 'under_line']

DEFAULT_DATE = datetime(1999, 9, 1)


class Soup:

    def __init__(self, url):
        content = requests.get(BASE_URL + url).content
        self.soup_ = BeautifulSoup(content, 'html.parser')


class VegasInsiderWebScrapper:

    def __init__(self, season=2018, week=17):
        self.season = season
        self.week = week
        self.data = []

    def run(self):
        weeks = [self.WeekData(self, url, season, week) for url, season, week in self._get_week_urls()]

        for week in weeks:
            week.run()

        self.write_to_file()

    def _get_week_urls(self):
        '''
        Returns a list of URLs to the Line Movements for each game on the scoreboard
        :return: Returns a list of URLs as strings
        '''
        return [("/nfl/scoreboard/scores.cfm/week/{}/season/{}".format(week, self.season), self.season, week) for week in range(1, self.week + 1)]

    def write_to_file(self):
        with open("../data/season_{}.csv".format(self.season), 'w') as file:

            cvs_writer = csv.writer(file)
            for row in [COLUMN_TITLES] + self.data:
                cvs_writer.writerow(row)

    class WeekData(Soup):

        def __init__(self, outer, url, season, week):
            Soup.__init__(self, url)
            self.outer = outer
            self.url = url
            self.season = season
            self.week = week
            self.games = []

        def run(self):
            self.get_data_for_all_games()

        def _get_game_urls(self):
            '''
            Returns a list of URLs to the Line Movements for each game on the scoreboard
            :return: Returns a list of URLs as strings
            '''
            return [link['href'] for link in self.soup_.findAll('a', {'class': 'white'}) if link.text == "Line Movements"]

        def get_data_for_all_games(self):

            games = [self.GameData(self.outer, url, self.season, self.week) for url in self._get_game_urls()]

            for game in games:
                print(game)
                game.run()

        class GameData(Soup):

            def __init__(self, outer, url, season, week):
                Soup.__init__(self, url)

                self.url = url
                self.outer_ = outer

                self.week = week
                self.season = season

                self.date = self.get_game_date()
                self.home_city, self.home_team, self.away_city, self.away_team = self.get_teams()

            def run(self):
                if self.date != DEFAULT_DATE:
                    self.get_data_for_game()

            def get_data_for_game(self):
                self.get_casino_money_lines_for_game()

            def get_teams(self):
                home, away = tuple(self.soup_.find('td', {'class': 'page_title'}).text.strip('\n').split(' @ '))
                home, away = home.split(' '), away.split(' ')
                home_city, home_team = (home[0], home[1]) if len(home) == 2 else (' '.join(home[:2]), home[2])
                away_city, away_team = (away[0], away[1]) if len(away) == 2 else (' '.join(away[:2]), away[2])

                return home_city, home_team, away_city, away_team

            def get_game_date(self):
                date = self.soup_.find('div', {'class': 'SLTables1'}).findAll('tbody')[1].findAll('td')
                date = ' '.join([item.text.translate(TRANSLATE).split('e:')[1] for item in date])
                try:
                    return datetime.strptime(date, '%A, %B %d, %Y %I:%M %p ')
                except ValueError:
                    return DEFAULT_DATE

            def get_casino_money_lines_for_game(self):
                '''
                Iterates through all of the casino money line tables and returns a list of lists
                containing data of the money lines right before the beginning of the game for each casino
                :return: list of lists
                '''

                money_lines = []
                elements = self.soup_.findAll('td', {'class': 'rt_railbox_border'})

                for element in elements:
                    casino_name = '_'.join(element.find('tr', {'class': 'component_head'}).text.translate(TRANSLATE).split(" ")[:-2])
                    data = [[td.text.translate(TRANSLATE) for td in tr.findAll('td')] for tr in element.findAll('tr')[3:]]

                    game = self.get_money_line_from_before_game(data)

                    money_lines.append([self.week, self.season] + [self.home_city, self.home_team, self.away_city, self.away_team] + [casino_name] + game)

                self.outer_.data += money_lines

                return money_lines

            def get_money_line_from_before_game(self, data):
                '''
                Returns the money line from right before the game begins

                This function currently utilizes the fact that the money line from right before the game begins
                is the last row to have an empty value in the last column. Consequently, this function recursively
                checks the last element of the last row and returns the first one that has an empty value. This
                is not the best approach as this may not be consistent for every game.

                The next iteration of this function will use the time the game starts to filter out rows that were
                added afterwards and return the last remaining row which will be the money line from right before the game begins.
                :param data: Lists of Lists
                :return: List
                '''

                if not data:
                    return []

                if self.date < self.get_date(data[-1], self.season):
                    return self.get_money_line_from_before_game(data[:-1])
                else:
                    return self.parse_row(list(np.array(data[-1])[[0, 1, 4, 5, 6, 7]]))

            def parse_row(self, row):
                if len(row) != 6: return row
                fav = row[2].split(' ')
                dog = row[3].split(' ')
                over = row[4].split(' ')
                under = row[5].split(' ')

                return [self.get_date(row, self.season)] + self.get_lines(fav) + self.get_lines(dog) + over + under

            @staticmethod
            def get_date(data, season):
                return datetime.strptime("{}/{} {}".format(data[0], season, data[1]).upper(), "%m/%d/%Y %I:%M%p")

            @staticmethod
            def get_lines(data):
                if len(data) < 2:
                    return [''] * 3

                if data[0][3:] == "PK":
                    spread = 0
                elif data[0][3:] == "XX" or data[0][3:] == '':
                    spread = None
                else:
                    spread = float(data[0][3:])

                if data[1] == "XX":
                    line = None
                else:
                    line = float(data[1])
                return [data[0][:3], spread, line]

            def __str__(self):
                return "Home: {} Away: {} Week: {} Season: {} Path: {}"\
                    .format(self.home_team, self.away_team, self.week, self.season, self.url)


def main():

    seasons = [VegasInsiderWebScrapper(season=year) for year in range(2012, 2018)] + [VegasInsiderWebScrapper(season=2018, week=4)]

    with ThreadPoolExecutor() as executor:
        executor.map(lambda season: season.run(), seasons)



if __name__ == '__main__':
    main()