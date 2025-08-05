from flask import Flask, jsonify, request
from datetime import datetime
from skyfield.api import load, wgs84, Star
from skyfield.api import Loader
from skyfield.data import hipparcos
from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
from astropy import units as u
from pygeomag import GeoMag
from gui import GUIselection, open_manual_calibration_window
import threading
import time
import requests
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
skyfield_path = os.path.join(script_dir, 'Skyfield', '.skyfield')

calibration_command = {'command': 'stop'}
command_lock = threading.Lock()


with load.open(hipparcos.URL) as f:
    df = hipparcos.load_dataframe(f)


### INTERFACE FOR DUMB USER


result_data_gui = GUIselection()
'''
print(" \n \n \n For the object names:\n \n Consult stations.txt for the satellites, \n \n For planets and moon, type [planet_name barycenter] in non-capital letters, \n \n For stars input the HIP number (find on wikipedia or somewhere else) \n \n For Galaxies and Nebulas, find the M Number \n \n \n")

print("\n \n Find me at http://192.168.1.169:5000/track \n \n \n")
lat = float(input("Enter your latitude: "))
lon = float(input("Enter your longitude: "))
el = float(input("Enter your elevation: "))
is_user_dumb = True
while(is_user_dumb):
    type_of_object = str(input("Enter the type of object (Star, Planet, Moon, Satelllite, Galaxy, Nebula):"))
    if type_of_object == "Star" or type_of_object == "Planet" or type_of_object == "Moon" or type_of_object == "Satellite" or type_of_object == "Galaxy" or type_of_object == "Nebula":
        is_user_dumb = False
    else:
        print("You Donkey, chose a valid option (Star/Planet/Moon/Satellite/Galaxy/Nebula")

'''

lat = float(result_data_gui['latitude'])
lon = float(result_data_gui['longitude'])
el = float(result_data_gui['elevation'])
type_of_object = result_data_gui["type_of_body"]

### TRACKING PART



app = Flask(__name__)



loader = Loader(skyfield_path)
ts = loader.timescale()
t = ts.now()
yeardec = t.utc_datetime().year + (t.utc_datetime().timetuple().tm_yday - 1) / 365.25
gm = GeoMag()  # loads WMM coefficients (2025–2030)
result = gm.calculate(glat=lat, glon=lon, alt=(el/1000), time=yeardec)
mag = result.d

planets = loader('de431t.bsp')

moons_jupiter = loader('jup365.bsp')
moons_mars = loader('mar099.bsp')
moons_neptune = loader('nep097.bsp')
moons_pluto = loader('plu060.bsp')
moons_saturn = loader('sat441l.bsp')
moons_uranus = loader('ura182.bsp')

print(planets)
print(moons_jupiter)
print(moons_mars)
print(moons_neptune)
print(moons_pluto)
print(moons_saturn)
print(moons_uranus)

earth = planets['earth']


is_moon = False


if(type_of_object == "Planet"):

    #object_name = str(input("\n \n \n Enter the name of the planet in non capital letters:"))
    object_name = result_data_gui["body_name"]
    planet = planets[object_name + " barycenter"]

elif(type_of_object == "Satellite"):
    #object_name = str(input(" \n \n \n Enter the name of the object according to the active.txt file:"))
    object_name = result_data_gui["body_name"]
    satellites = load.tle_file("https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle")
    sat = {sat.name: sat for sat in satellites}
    satellite = sat[object_name]


elif(type_of_object == "Star"):
    #object_name = str(input("\n \n \n Enter the HIP number of the star:"))
    object_name = result_data_gui["body_name"]
    row = df.loc[int(object_name)]
    star = Star.from_dataframe(row)


elif type_of_object == "Galaxy" or type_of_object == "Nebula":
    #object_name = str(input("\n \n \n Enter the name, eg M17:"))
    object_name = result_data_gui["body_name"]
    table = Simbad.query_object(object_name)
    ra_deg = table['ra'][0]
    dec_deg = table['dec'][0]
    star = Star(ra_hours=ra_deg/15.0, dec_degrees=dec_deg)


elif type_of_object == "Moon":
    #planet_name = str(input("Enter the name of the planet:"))
    planet_name = result_data_gui["moon_planet"]
    #moon_name = str(input("Enter the name of the moon:"))
    moon_name = result_data_gui["moon"]
    if planet_name == "jupiter":
        planet = planets["jupiter barycenter"]
        moon = moons_jupiter[moon_name]
    elif planet_name == "mars":
        planet = planets["mars barycenter"]
        moon = moons_mars[moon_name]
    elif planet_name == "neptune":
        planet = planets["neptune barycenter"]
        moon = moons_neptune[moon_name]
    elif planet_name == "pluto":
        planet = planets["pluto barycenter"]
        moon = moons_pluto[moon_name]
    elif planet_name == "saturn":
        planet = planets["saturn barycenter"]
        moon = moons_saturn[moon_name]
    elif planet_name == "uranus":
        planet = planets["uranus barycenter"]
        moon = moons_uranus[moon_name]
    elif planet_name == "earth":
        is_moon = True
        planet = earth
        moon = planets["moon"]

    else:
        print("Something went wrong you fuck")

observer1 = wgs84.latlon(lat, lon, elevation_m=el)



#calibrated = str(input("Choose the calibration point (Polaris/Moon/Sun):"))
calibrated = result_data_gui["calibration"]

if(calibrated == "Polaris"):
    t = ts.now()
    row_polaris = df.loc[int(11767)]
    polaris = Star.from_dataframe(row_polaris)

    observer_polaris = earth + observer1

    # Observe ISS from observer's locationplanet
    astrometric_polaris = observer_polaris.at(t).observe(polaris).apparent()

    # Get altitude and azimuth angles
    alt_polaris, az_polaris, distance_polaris = astrometric_polaris.altaz()
elif (calibrated == "Sun"):
    polaris = planets['sun']
    t = ts.now()
    observer_polaris = earth + observer1

    # Observe ISS from observer's locationplanet
    astrometric_polaris = observer_polaris.at(t).observe(polaris).apparent()

    # Get altitude and azimuth angles
    alt_polaris, az_polaris, distance_polaris = astrometric_polaris.altaz()
else:
    t = ts.now()
    observer_polaris = earth + observer1
    polaris = planets['moon']
    # Observe ISS from observer's locationplanet
    astrometric_polaris = observer_polaris.at(t).observe(polaris).apparent()

    # Get altitude and azimuth angles
    alt_polaris, az_polaris, distance_polaris = astrometric_polaris.altaz()







#pointed = str(input("Once you pointed the telescope at  the calibration object press enter to continue"))





if type_of_object == "Planet":
    @app.route('/track')
    def planet_data():




        # Load current time
        t = ts.now()

        # Observer location (e.g., Zurich)4
        observer = earth + wgs84.latlon(lat, lon, elevation_m=el)

        # Observe ISS from observer's location
        astrometric = observer.at(t).observe(planet).apparent()

        # Get altitude and azimuth angles
        alt, az, distance = astrometric.altaz()

        return jsonify({
                'altitude_deg': round(alt.degrees, 3),
                'azimuth_deg': round(az.degrees, 3),
                'distance_km': round(distance.km, 3),
                'timestamp_utc': datetime.utcnow().isoformat() + 'Z',
                'magnetic_dec': mag,
                'polaris_alt': round(alt_polaris.degrees, 3),
                'polaris_az': round(az_polaris.degrees, 3)
            })
elif type_of_object == "Moon":
    @app.route('/track')
    def moon_data():
        t = ts.now()

        observer = earth + observer1

        if is_moon ==False:
            topocentric = observer.at(t).observe(planet + moon).apparent()
        elif is_moon == True:
            topocentric = observer.at(t).observe(moon).apparent()


        alt, az, distance = topocentric.altaz()
        return jsonify({
                'altitude_deg': round(alt.degrees, 3),
                'azimuth_deg': round(az.degrees, 3),
                'distance_km': round(distance.km, 3),
                'timestamp_utc': datetime.utcnow().isoformat() + 'Z',
                'magnetic_dec': mag,
                'polaris_alt': round(alt_polaris.degrees, 3),
                'polaris_az': round(az_polaris.degrees, 3)
            })
elif type_of_object == "Satellite":
    @app.route('/track')
    def track_satellite():
        t = ts.now()
        difference = satellite - observer1
        topocentric = difference.at(t)
        alt, az, distance = topocentric.altaz()

        return jsonify({
            'altitude_deg': round(alt.degrees, 3),
            'azimuth_deg': round(az.degrees, 3),
            'distance_km': round(distance.km, 3),
            'timestamp_utc': datetime.utcnow().isoformat() + 'Z',
            'magnetic_dec': mag,
            'polaris_alt': round(alt_polaris.degrees, 3),
            'polaris_az': round(az_polaris.degrees, 3)
        })
else:
    @app.route('/track')
    def star_data():




        # Load current time
        t = ts.now()

        # Observer location (e.g., Zurich)
        observer = earth + wgs84.latlon(lat, lon, elevation_m=el)

        # Observe ISS from observer's locationplanet
        astrometric = observer.at(t).observe(star).apparent()

        # Get altitude and azimuth angles
        alt, az, distance = astrometric.altaz()

        return jsonify({
                'altitude_deg': round(alt.degrees, 3),
                'azimuth_deg': round(az.degrees, 3),
                'distance_km': round(distance.km, 3),
                'timestamp_utc': datetime.utcnow().isoformat() + 'Z',
                'magnetic_dec': mag,
                'polaris_alt': round(alt_polaris.degrees, 3),
                'polaris_az': round(az_polaris.degrees, 3)
            })

@app.route('/manual', methods=['GET', 'POST'])
def handle_calibration_command():
    global calibration_command
    global command_lock

    if request.method == 'POST':
        # This is where your GUI will send the command
        data = request.json
        if data and 'command' in data:
            with command_lock:
                calibration_command['command'] = data['command']
            print(f"Received calibration command: {data['command']}")
            return jsonify({'status': 'success', 'message': 'Command received'}), 200
        return jsonify({'status': 'error', 'message': 'Invalid command format'}), 400

    elif request.method == 'GET':
        # This is what the ESP32 will poll
        with command_lock:
            current_command = calibration_command['command']
            calibration_command['command'] = "Idle"
            if current_command == "stop":
                calibration_command['command'] = "stop"
        return jsonify({'command': current_command}), 200


def run_flask():
    app.run(host='0.0.0.0', port=5000)
if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000)

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    open_manual_calibration_window()
    flask_thread.join()



