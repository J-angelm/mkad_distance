"""
    Moscow Automobile Ring Road (MKAD) Distance Calculator.

    date:   08/17/2021
    author: J.Angel
"""
from flask import render_template, request, Blueprint, session, url_for, flash, redirect
import requests
import urllib.parse
from geopy import distance

bp = Blueprint("mkad_distance", __name__)

@bp.route('/')
def home():
    """
    Home page
    """
    if 'api_key' in session.keys():
        return render_template('home.html', api_key=session['api_key'])
    else:
        return render_template('home.html', api_key=None)

@bp.route('/clear_key')
def clear_key():
    """
    Clear Yandex API Key stored in session (cache)
    """
    if 'api_key' in session.keys():
        del session['api_key']
    return redirect(url_for('mkad_distance.home'))

@bp.route('/clear_log')
def clear_log():
    """
    Clear Log stored in session (cache)
    """
    if "address_log" in session.keys():
        del session['address_log']
    return redirect(url_for('mkad_distance.home'))

@bp.route('/log')
def log():
    """
    Go to log page and see the list of logged results
    """
    if 'address_log' in session.keys():
        return render_template('log.html', log_recs=session['address_log'])
    else:
        return render_template('log.html')

@bp.route('/get_distance')
def get_distance():
    """
    Get the distance from a given address to the Moscow Ring Road (MKAD).
    
    Algorithm Description:
    ---------------------
    1. Get an address from user with an HTTP GET request
    2. If the address is inside the MKAD, then flash banner of error
    3. Else, the address is outside the MKAD, so calculate distance in kms
    4. Save the distance in the session (cache) and flash banner of success
    """
    # if the location is inside moscow ring, then flash error
    if 'api_key' not in session.keys() or session['api_key'] is None:
        session['api_key'] = request.values.get('api_key')
    
    address = request.values.get('address')
    if validate_coordinates(address) is not True:
        return redirect(url_for('mkad_distance.home'))

    # else, render total distance
    distance = round(calculate_distance(address), 2)
    if 'address_log' in session.keys():
        session['address_log'][address] = distance
    else:
        session['address_log'] = {address: " - " + str(distance) + "km."}

    flash("Total distance from {0} to MKAD is {1:0.2f} km. Added to log."
                                        .format(address, distance), "success")
    return redirect(url_for('mkad_distance.home'))


def validate_coordinates(address):
    """
    Verify if the given address is located inside of the MKAD

    Algorithm Description:
    ----------------------
    1. Set URI parameters to send an HTTP GET request to Yandex geocode maps tool, 
    including flag to limit search area
    2. Send HTTP GET request
    3. If request response is not 200 OK, then flash and return Failure
    4. Else, store data as json in a dictionary
    5. If the response object is empty, then coordinates are outside the MKAD, so 
    return Success 
    6. Else, the location is inside the MKAD, return Failure
    """
    URL = "https://geocode-maps.yandex.ru/1.x/"

    geocode = address
    lang    = 'en_US'        # response language
    rspn    = '1'            # flag to limit search area
    mkad_ll = "37.612,55.71" # log,lat of area center
    spn     = "0.566,0.414"  # difference between max_lat-minlat and max_long-min_long
    format  = "json"

    params = {'geocode':geocode,
              'apikey':session['api_key'],
              'lang':lang,
              'rspn':rspn,
              'll':mkad_ll,
              'spn':spn,
              'format':format}

    safe_params = urllib.parse.urlencode(params, safe=', ')
    r = requests.get(URL, params=safe_params)

    data = r.json()

    if r.status_code != 200:
        if data['message'] == "Invalid key":
            flash("Invalid Yandex API key", "error")
        else:
            flash("Yandex HTTP request failure", "error")
        return False

    if data['response']['GeoObjectCollection']['featureMember'] == []:
        return True
    else:
        flash("Address coordinates are located inside of the MKAD. "
                                        "Please enter another address.", "error")
        return False

def calculate_distance(address):
    """
    Calculate the distance from the address to the MKAD

    Algorithm Description:
    ----------------------
    1. Set URI parameters
    2. Send HTTP GET request
    3. If request response is not 200 OK, then flash and return Failure
    4. Else, store data as json in a dictionary
    5. Calculate and return the distance using geopy.distance utility
    """
    URL = "https://geocode-maps.yandex.ru/1.x/"

    geocode = address
    lang    = 'en_US'
    format  = "json"
    params  = {'geocode':geocode,
               'lang':lang,
               'apikey':session['api_key'],
               'format':format}

    r = requests.get(URL, params=params)
    if r.status_code != 200:
        flash("Yandex HTTP request failed", "error")
        return False

    data = r.json()
    pos = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    location_ll = tuple(map(float, pos.split()))
    mkad_ll = (37.612, 55.71) #long,lat

    # reverse mkad_ll and location_ll to fit geopy format
    return distance.distance(location_ll[::-1], mkad_ll[::-1]).km