import csv
import numpy

"""
lla_to_ecef() notes:

There are some changes we need to make to the variable before computation
-Alt to meters from kilometers
-Latitutde and Longitude in radians

Game plan:
-Correct incoming data
-Lay out the params from the PDF
-Compute X Y Z
-Return in a dictionary for quick reference later on
"""
def lla_to_ecef(lat,long,alt):
    # We need the alt in meters
    alt = alt*1000

    # We need the lat and long in radians
    lat = numpy.deg2rad(lat)
    long = numpy.deg2rad(long)

    # WGS84 Parameters from Section 1 of LLAtoECEF.pdf
    a = 6378137.0
    f = 1/298.257223563
    b = a*(1.0-f)
    e = numpy.sqrt((numpy.square(a) - numpy.square(b))/(numpy.square(a)))
    e2 = numpy.sqrt((numpy.square(a) - numpy.square(b))/(numpy.square(b))) # Appears to not be needed

    # X Y Z computation from Section 2.1 of LLAtoECEF.pdf

    N = a/(numpy.sqrt(1-((numpy.square(e)) * numpy.square(numpy.sin(lat)))))

    x = (N + alt) * numpy.cos(lat) * numpy.cos(long)
    y = (N + alt) * numpy.cos(lat) * numpy.sin(long)
    z = ((((numpy.square(b))/(numpy.square(a)))*N) + alt) * numpy.sin(lat)

    #ECEF dict to be returned
    ecef = {}
    ecef['X'] = x
    ecef['Y'] = y
    ecef['Z'] = z

    return ecef

"""
build_ecef_coords() notes:
Before we get into computation, we need to read in the CSV file with the data.

I noticed that each entry has lots of whitespace which will mess with computation.

I prefer to use Python's built in csv library when dealing with data of this size (less than 5 columns)

Game plan: 
-Open the CSV and fill an empty dictionary with each line entry.
-The key will be the Unix epoch seconds
"""
def build_ecef_coords():
    coordinates = {}

    with open("ephemeris.csv", 'r') as f:
        readin_lines = csv.reader(f, delimiter=',')

        for line in readin_lines:
            
            lla_coords = {'lat':float(line[1].strip()), 'long':float(line[2].strip()), 'alt':float(line[3].strip())}

            coordinates[float(line[0].strip())] = {'lla' :{}, 'ecef': {}}

            coordinates[float(line[0].strip())]['lla'] = lla_coords
            
            coordinates[float(line[0].strip())]['ecef'] = lla_to_ecef(float(line[1].strip()),float(line[2].strip()),float(line[3].strip()))

    return coordinates


"""
nearest_time_search() notes:
In order to find the interpolation of the given times, we need the ECEF data at the two nearest times
We can access a list of every time by getting the coordinate dictionary keys

We can find the nearest time by sorting a list of differences between the user input time and every time in the keys list
From here, to keep things neat, I want to return the most recent time second, so that way t2-t1 will provide a positive number later on
"""
def nearest_time_search(coordinates, input_time):

    times = list(coordinates.keys())

    nearest_time1 = min(times, key=lambda x: numpy.abs(x - input_time))
    times.remove(nearest_time1)
    nearest_time2 = min(times, key=lambda x: numpy.abs(x - input_time))

    if nearest_time2 > nearest_time1:
        return(nearest_time1, nearest_time2)
    else:
        return(nearest_time2,nearest_time1)

"""
calculate_ecef_velocity() notes:
Here is where it all comes together!
Using our dictionary of coordinates, and times given from nearest_time_search, we can build our output vector
Calculations are:
(X_2-X_1)/(t2-t1)
(Y_2-Y_1)/(t2-t1)
(Z_2-Z_1)/(t2-t1)
"""
def calculate_ecef_velocity(coordinates, t1, t2):

    output_vector = []

    d_x = (coordinates[t2]['ecef']['X'] - coordinates[t1]['ecef']['X'])/(t2-t1)
    output_vector.append(d_x)

    d_y = (coordinates[t2]['ecef']['Y'] - coordinates[t1]['ecef']['Y'])/(t2-t1)
    output_vector.append(d_y)

    d_z = (coordinates[t2]['ecef']['Z'] - coordinates[t1]['ecef']['Z'])/(t2-t1)
    output_vector.append(d_z)

    return output_vector


"""
main notes:
We will take the input and make sure its a float before continuing
From there build the coordinate dictionary
Gather the nearest times
Calculate the output vector
Print the output vector to the console
"""
if __name__ == "__main__":

    input = input("Enter the time, in seconds since the Unix epoch, you wish to receive an ECEF velocity vector for.\n")

    try:
        input = float(input)
    except ValueError as e:
        print(f"Input cannot be cast to float type! {e}")


    coordinates = build_ecef_coords()
    nearest_time1, nearest_time2 = nearest_time_search(coordinates, input)

    output = calculate_ecef_velocity(coordinates, nearest_time1, nearest_time2)
    print(f"ECEF Velocity Vector at time: {input}")
    print(output)