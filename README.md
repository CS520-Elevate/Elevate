# Elevate

Given a starting and ending location, the Elevate program will allow the user to choose a difficulty level for the path between two points. The assumption is they will be running, walking or biking, so are choosing the level of resistance. The algorithm will then create the path based on their choice. What determines difficulty is a combination of the length (distance) of the path, as well as the amount of elevation gain (hills).


## Getting Started

Clone the following repository:

```
git clone https://github.com/CS520-Elevate/Elevate
```

### Prerequisites
Python Programming Language


### Installation
OSMNX
```
pip install osmnx
```
Note: If you are pip installing OSMnx, install geopandas and rtree first. It's easiest to use conda-forge to get these dependencies installed.

with conda:
```
conda install -c conda-forge osmnx

```
Folium
```
pip install folium
```

###Run the Program
Once the repository is cloned, simply run the following from the repository
```
python main.py
```
You will be asked to enter the origin and destination coordinates and select the difficulty you would desire with respect to elevation.
Then the route will be displayed as an .html file.
## Authors

See the list of [contributors](https://github.com/CS520-Elevate/Elevate/settings/collaboration) who participated in this project.
