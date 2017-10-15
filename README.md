# Bike trips

Playing with bike trip data.
Scripts to manipulate Citi bike data from New York City.

1) Extract unique stations and their latitude and longitude.
1) For each possible pair call Google for the distance between them
(in meters) and trip time (in seconds) and write to a new output file.
The number of paths computed is: `(N)(N-1)/2` where `N` is the number of
stations. If there are 680 stations the paths are 230,680. This is
ignoring the fact that the path from A to B is not necessarily the
same as B to A, but it should be close.
