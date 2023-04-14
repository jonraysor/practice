import json
from datetime import datetime, timedelta

with open("data/report.json", "r") as f:
    data = json.load(f)


def get_avg_audio(week):
    totalaudio = 0
    count = 0
    for item in data:
        if data[item] and data[item]['audio']:
            for key in data[item]['audio']:
                if week in key:
                    totalaudio += data[item]['audio'][key]
                    count += 1

    return totalaudio / count


def get_consumption(sales, audio, video):
    """

    :param sales:
    :param audio:
    :param video:
    :return: the total consumption
    """
    return sales + (audio / 125) + (video / 375)


def get_second_highest(week):
    """

    :param week:
    :return: second-highest consumption for the week
    """
    total = {}
    for item in data:
        if data[item] and data[item]['audio']:
            for key in data[item]['audio']:
                if week in key:
                    consumption = {
                        data[item]['song']: get_consumption(data[item]['sales'][key], data[item]['audio'][key],
                                                            data[item]['video'][key])}
                    total.update(consumption)
                    final = sorted(total.items(), key=lambda top: top[1])
    return final[-2]


def get_atd_percentage(song, atd):
    """

    :param song:
    :param atd:
    :return: the atd consumption for videos (375(consumption-sales-(audio/125))=videos
    """
    for key in data[song]['video']:
        if 'ATD' in key and atd in key:
            return (100 / (data[song]['video'][key]) / get_consumption(data[song]['sales'][key],
                                                                       data[song]['audio'][key],
                                                                       data[song]['video'][key]))
            #                                data[song]['video'][key])))
            # return (375 * (get_consumption(data[song]['sales'][key], data[song]['audio'][key],
            #                                data[song]['video'][key]) - data[song]['sales'][key] - (
            #                        data[song]['audio'][key] / 125)))


def get_previous_week(date):
    """

    :param date:
    :return: the previous week
    """
    date_format = "%m/%d/%Y"
    date_object = datetime.strptime(date, date_format)
    one_week = date_object - timedelta(days=7)
    return one_week.strftime("%m/%d/%Y")


def difference(x, y):
    """

    :param x:
    :param y:
    :return: if x is 3% bigger than y
    """
    return x > y * 1.03


def get_increase(week, atd):
    """

    :param week:
    :param atd:
    :return: a list of all the songs with 3% or higher increases in video
    """
    previous_week = get_previous_week(atd)
    increased = {}
    totalvideothisweek, totalvideolastweek = 0, 0
    for item in data:
        if data[item] and data[item]['video']:
            for key in data[item]['video']:
                if week in key:
                    totalvideothisweek += data[item]['video'][key]
                if previous_week in key:
                    totalvideothisweek += data[item]['video'][key]
            if difference(totalvideothisweek, totalvideolastweek):
                increased = data[item]['song']
    return increased
