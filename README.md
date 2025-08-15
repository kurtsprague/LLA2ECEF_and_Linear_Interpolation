# LLA2ECEF_and_Linear_Interpolation
## How It Works
This project expects a user to provide ephemeris of a spacecraft in the form of a CSV following the format:
*Seconds since Unix epoch, Latitude (in Degrees), Longitude (in Degrees), and Altitude (in meters)*

I have provided a small sample, named *ephemeris.csv*.
The sample ephemeris is a mock example of a satellite in Low Earth Orbit. 

Comments are provided throughout ECEF_Vector_Estimation.py that showcase my thought around building each function, but at a glance it works like this:
1. The user is asked for a specific time (seconds since Unix epoch), in which they want an estimated ECEF vector. **Since the script provides an estimation, the user must provide a time which isn't in *ephemeris.csv*.**
2. *ephemeris.csv* is parsed, and a dictionary is built where each key is a different time. From there the dictionary is nested, where each time has a LLA and an ECEF entry.
3. To fill the ECEF entry, *lla_to_ecef()* is called where I use numpy and the WGS84 parameters to calculate the ECEF X, Y, and Z.
4. The two nearest times to the user given time are found, and then linear interpolation is performed to estimate the ECEF vector at the user given time.

## How To Use It Yourself
1. Clone this repository.
2. Replace the data in *ephemeris.csv* with your data.
3. Run *ECEF_Vector_Estimator.py*
