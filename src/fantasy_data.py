import http.client
import urllib.parse
import urllib.error
import os
import json

from concurrent.futures import ThreadPoolExecutor


headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': os.environ['FANTASY_DATA_KEY'],
}

params = urllib.parse.urlencode({
})

class FantasySchedule:

    def __init__(self, season=2018):
        self.season = season
        self.schedule = []

    def run(self):
        self.get_schedule()
        self.write_to_file()

    def get_schedule(self):

        conn = http.client.HTTPSConnection('api.fantasydata.net')
        try:
            conn.request("GET", "/v3/nfl/scores/json/Schedules/{}".format(self.season), "{body}", headers)
            response = conn.getresponse()
            data = response.read()
            self.schedule += json.loads(data)
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))
        conn.close()

    def write_to_file(self):
        with open("../data/season_{}_schedule.json".format(self.season), 'w') as file:
            json.dump(self.schedule, file)


class FantasyData:

    def __init__(self, season=2018, week=17):
        self.data = []
        self.season = season
        self.week = week

    def run(self):
        self.get_stats()
        self.write_to_file()

    def get_stats(self):

        conn = http.client.HTTPSConnection('api.fantasydata.net')
        for week in range(1, self.week + 1):
            try:
                conn.request("GET", "/v3/nfl/stats/JSON/TeamGameStats/{}/{}".format(self.season, week), "{body}", headers)
                response = conn.getresponse()
                data = response.read()
                self.data += json.loads(data)
            except Exception as e:
                print("[Errno {0}] {1}".format(e.errno, e.strerror))
        conn.close()

    def write_to_file(self):
        with open("../data/season_{}.json".format(self.season), 'w') as file:
            json.dump(self.data, file)


def main():

    # seasons = [FantasyData(season) for season in range(2012, 2018)] + [FantasyData(2018, 4)]

    # with ThreadPoolExecutor as executor:
    #     executor.map(lambda x: x.run(), seasons)

    schedules = [FantasySchedule(season) for season in range(2012, 2019)]

    for schedule in schedules:
        schedule.run()



if __name__ == '__main__':
    main()