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
2. Make sure you have numpy. If you don't then use: *pip install numpy*
3. Replace the data in *ephemeris.csv* with your data.
4. Run *ECEF_Vector_Estimation.py*

## Default Example (Make Sure It Works After Pulling)
If you run *ECEF_Vector_Estimation.py*, and provide it with time 1700000340, you should get the following console output:
```
Enter the time, in seconds since the Unix epoch, you wish to receive an ECEF velocity vector for.
1700000340
ECEF Velocity Vector at time: 1700000340.0
[-3145.555811346912, 200.39658667631448, -7011.372965759505]
```
