from data_extractor import get_data
from script import get_avg_audio, get_second_highest, get_atd_percentage, get_increase

get_data('data/trend_report_sample.xlsx')

week = '11/02/2018 - 11/08/2018'
atd = '11/22/2018'
print('Average Audio: ',get_avg_audio(week))
print('Second Highest Consumption: ', get_second_highest(week))
print('Videos percentage of One Kiss ATD: ', get_atd_percentage('OneKissCalvinHarrisDuaLipa', atd))
print('Songs with video consumption that increased by at least 3%: ', get_increase(week, atd))

