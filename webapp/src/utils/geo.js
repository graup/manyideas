import { apiGet } from './api';

const searchDistance = 700;
const searchCenter = [36.3708, 127.3626];

const overpassApiUrl = 'https://overpass-api.de/api/interpreter';

const overpassScript = (lat, lon, distance) => `
[timeout:5][out:json];
(
  node["building"]["name"~".*"](around:${distance}, ${lat}, ${lon});
  way["building"]["name"~".*"](around:${distance}, ${lat}, ${lon});
  node["water"]["name"~".*"](around:${distance}, ${lat}, ${lon});
  way["water"]["name"~".*"](around:${distance}, ${lat}, ${lon})
);
out tags center;
relation["building"](around:${distance}, ${lat}, ${lon});
out center;
`;

function deg2rad(deg) {
  return deg * (Math.PI / 180);
}

function getCoordOffset(what, lat, lon, offset) {
  const earthRadius = 6378137;
  const coord = [lat, lon];
  const radOff = what === 0 ? offset / earthRadius : offset / (earthRadius * Math.cos((Math.PI * coord[0]) / 180));
  return coord[what] + (radOff * (180 / Math.PI));
}

function getBBox(lat, lon, area) {
  const offset = area / 2;
  return [
    getCoordOffset(1, lat, lon, -offset),
    getCoordOffset(0, lat, lon, -offset),
    getCoordOffset(1, lat, lon, offset),
    getCoordOffset(0, lat, lon, offset),
  ]; // 0 = minlon, 1 = minlat, 2 = maxlon, 3 = maxlat
}

function getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) {
  const R = 6371;
  const dLat = deg2rad(lat2 - lat1);
  const dLon = deg2rad(lon2 - lon1);
  const a =
    (Math.sin(dLat / 2) * Math.sin(dLat / 2)) +
    (Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2))
  ;
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const d = R * c; // Distance in km
  return d;
}

const sortByDistance = (places, lat, lon) =>
  places.map((place) => {
    const dist = getDistanceFromLatLonInKm(place.center.lat, place.center.lon, lat, lon);
    place.distance = dist;
    return [dist, place];
  }).sort().map(j => j[1]);

const getPlacesAroundPoint = (lat, lon) =>
  new Promise((resolve, reject) => {
    const params = { data: overpassScript(searchCenter[0], searchCenter[1], searchDistance) };
    apiGet(overpassApiUrl, { params }).then((resp) => {
      const places = sortByDistance(resp.data.elements, lat, lon);
      resolve(places);
    }).catch(reject);
  });

export {
  getPlacesAroundPoint,
  getBBox,
};
