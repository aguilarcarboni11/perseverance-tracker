import pandas as pd
import numpy as np
import requests as rq
from fastapi import FastAPI

def getManifestData(url): # gets manifest data
    manifestData = rq.get(url).json()
    manifestData = manifestData['photo_manifest'] # pandas
    return manifestData

def getSol(manifestData):
    sol = manifestData['max_sol']
    return sol

def getImages(url):
    images = []
    imagesJson = rq.get(url).json()
    imagesJson = imagesJson['photos'] # returns a list of all img dictionaries
    for j in range(len(imagesJson)):
        imageURL = imagesJson[j]['img_src'] # retrieves all photos
        if imagesJson[j]['camera']['name'] != 'SKYCAM':
            images.append(imageURL)
    return images

def getWaypoints(url):
    coords = []
    coord = {}
    coordsJson = rq.get(url).json()
    coordsJson = coordsJson['features'] # gets all position data
    for i in range(len(coordsJson)):
        coord = {'lon': float(coordsJson[i]['properties']['lon']), 'lat': float(coordsJson[i]['properties']['lat']),'sol':int(coordsJson[i]['properties']['sol'])}
        coords.append(coord) #add coord to list
    return coords

def getDistance(coordsJson):
    distances = []
    distanceData = coordsJson
    for i in range(len(distanceData)):
        distances.append([distanceData[i]['properties']['dist_m'],distanceData[i]['properties']['sol']])
    distances = np.array(distances)
    distances = pd.DataFrame(distances) #data frame
    return distances
    
#Images dataframe
def getimagesJson():
    #imagesDF.to_csv('/Users/aguilarcarboni/Desktop/Coding/CTDS/NASA/React/public/Assets/CSV/imageData.csv',index = False)
    #imagesDF.to_csv('C:/Users/Agui/Desktop/Coding/NASA/React/public/Assets/CSV/imageData.csv',index = False)
    #imagesDF.to_csv('/home/andres/React/public/Assets/CSV/imageData.csv', index = False)
    return 

#Coordinates dataframe
def getCoordinateData():
    #CSV
    #coordsJson.to_csv('/Users/aguilarcarboni/Desktop/Coding/CTDS/NASA/React/public/Assets/CSV/waypoints.csv',index = False) #coords csv
    #coordsJson.to_csv('C:/Users/Agui/Desktop/Coding/NASA/React/public/Assets/CSV/waypoints.csv',index = False)
    #coordsJson.to_csv('/home/andres/React/public/Assets/CSV/coordsJson.csv', index = False)
    return


#Main
manifestUrl = 'https://api.nasa.gov/mars-photos/api/v1/manifests/perseverance/?api_key=kQwoyoXi4rQeY0lXWt1RZln6mLeatlYKLmYfGENB'
manifest = getManifestData(manifestUrl)

sol = getSol(manifest)


imagesUrl = 'https://api.nasa.gov/mars-photos/api/v1/rovers/perseverance/photos?sol='+ str(sol) + '&api_key=kQwoyoXi4rQeY0lXWt1RZln6mLeatlYKLmYfGENB'
waypointsUrl = 'https://mars.nasa.gov/mmgis-maps/M20/Layers/json/M20_waypoints.json'

images = getImages(imagesUrl)
coordinates = getWaypoints(waypointsUrl)

data = {
    'images': images,
    'coords': coordinates
}

#print(data)

app = FastAPI()
@app.get("/")
async def root():
    return data