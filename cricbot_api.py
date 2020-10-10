from dateutil import tz
from datetime import datetime
import unicodedata

# all filters for getting data


class Filter:
    # for live status
    filter_status = 'cb-font-16 cb-col-rt'

    # for schedule
    filter_schedule_head = 'cb-mtch-lst cb-col cb-col-100 cb-tms-itm'
    filter_schedule_1 = 'text-hvr-underline text-bold'
    filter_schedule_2 = 'text-gray'
    filter_schedule_3 = 'MMM dd'

    # for live score
    filter_live_forward = 'cb-lv-scrs-well cb-lv-scrs-well-live'
    filter_live_forward_exp = 'cb-lv-scrs-well cb-lv-scrs-well-complete'
    filter_live_head = 'cb-lv-grn-strip text-bold cb-lv-scr-mtch-hdr'
    filter_live_1 = 'text-hvr-underline text-bold'
    filter_live_0 = 'cb-col-100 cb-col cb-schdl'
    filter_live_2 = 'cb-ovr-flo cb-hmscg-tm-nm'
    filter_live_3 = 'cb-text-live'
    filter_live_3_exp = 'cb-text-complete'

    # for scorecard
    filter_scorecard_title_ext = 'cb-col cb-scrcrd-status cb-col-100 cb-text-complete'
    filter_scorecard_title = 'cb-col cb-scrcrd-status cb-col-100 cb-text-live'
    filter_scorecard_inning_header = 'cb-col cb-col-100 cb-scrd-hdr-rw'
    filter_scorecard_el_names = 'cb-col cb-col-100 cb-scrd-sub-hdr cb-bg-gray'
    filter_scorecard_el_value = 'cb-col cb-col-100 cb-scrd-itms'

# function to get current live status for given match index


def get_match_status(soup):
    status = soup.findAll('div', {'class': Filter.filter_status})[0]
    return status.text

# function to get upcoming matches schedule for given index


def get_match_schedule(i, soup):
    # double-filtering to avoid duplicacy errors
    data = soup.findAll('div', {'class': Filter.filter_schedule_head})[i]

    # getting title of the match
    title = data.find('a', {'class': Filter.filter_schedule_1})

    # getting match type or number
    match_id = data.findAll('span', {'class': Filter.filter_schedule_2})[0]

    # using timestamp to get the match timing
    # converting timestamp to seconds from milliseconds
    timestamp = data.find(
        'span', {'format': Filter.filter_schedule_3}).get('timestamp')[0:10]

    # converting time acc. indian standard time
    utc = datetime.fromtimestamp(int(timestamp))
    date = str(utc.astimezone(tz.gettz('Asia/Kolkata')))[5:16]

    # getting place of match being played
    place = data.findAll('span', {'class': Filter.filter_schedule_2})[1]

    # NOTE: unicode data is used to avoid '/xa0' type of output with the match id
    return title.text, unicodedata.normalize("NFKD", match_id.text), date, place.text

# function to get live score of given match index


def get_live_status(i, soup):
    # trying either if any RUNNING match is available for the given match index
    try:
        main_link = soup.findAll('a', {'class': Filter.filter_live_forward})[
            i].get('href')

    # trying either if the match is OVER.
    except:
        main_link = soup.findAll('a', {'class': Filter.filter_live_forward_exp})[
            i].get('href')

    # getting heading of the match
    heading = soup.findAll('h2', {'class': Filter.filter_live_head})[i]

    # getting title of the match
    title = soup.findAll('a', {'class': Filter.filter_live_1})[i]

    # getting match index
    # double-filtering to get duplicacy errors
    overview = soup.findAll('div', {'class': Filter.filter_live_0})[i]
    match_id = overview.findAll('span', {'class': Filter.filter_schedule_2})[i]

    # getting time from timestamp
    timestamp = soup.find(
        'span', {'format': Filter.filter_schedule_3}).get('timestamp')[0:10]
    utc = datetime.fromtimestamp(int(timestamp))
    date = str(utc.astimezone(tz.gettz('Asia/Kolkata')))[5:16]

    # getting place of the match
    place = soup.findAll('span', {'class': Filter.filter_schedule_2})[i+1]

    # getting both playing teams
    team1 = soup.findAll('div', {'class': Filter.filter_live_2})[i]
    team2 = soup.findAll('div', {'class': Filter.filter_live_2})[i+1]

    # getting inning status
    # trying if match is RUNNING
    try:
        status = soup.findAll('div', {'class': Filter.filter_live_3})[i]

    # trying if match is OVER
    except:
        status = soup.findAll('div', {'class': Filter.filter_live_3_exp})[i]

    # NOTE: unicode data is used to avoid '/xa0' type of output with the match id
    return main_link, heading.text, title.text, unicodedata.normalize("NFKD", match_id.text), date, place.text, team1.text, team2.text, status.text

