import urllib
import webapp2
import json
import login

from google.appengine.api import urlfetch


class MainPage(webapp2.RequestHandler):

  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('Hello, World!')


class CheckLocation(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/json'
    try:
      latitude = float(self.request.get('lat') or '0')
      longtitude = float(self.request.get('lon') or '0')
      query = '[out:json];way["building"](around:100,%f,%f);(._;>;);out body;' % (latitude, longtitude)
      url = "http://overpass-api.de/api/interpreter?data=" + urllib.quote_plus(query)
      result = urlfetch.fetch(url=url, method=urlfetch.GET)
      if result.status_code == 200:
        data = json.loads(result.content)
        elements = data["elements"]
        buildings = self.parse_buildings(elements)
        the_building = None
        for id, building in buildings.iteritems():
          if self.location_inside_building(building[0], (latitude, longtitude)):
            the_building = (id, building)
        if not the_building is None:
          tag = the_building[1][1]
          tag["building_id"] = the_building[0]
          tag["building_nodes"] = the_building[1][0]
          self.response.write(json.dumps(tag))
          return
    except:
      pass
    self.response.write("{}")

  def parse_buildings(self, elements):
    nodes = {}
    buildings = {}
    for element in elements:
      if element["type"] == "node":
        nodes[element["id"]] = (element["lat"], element["lon"])
    for element in elements:
      if element["type"] == "way":
        buildings[element["id"]] = ([nodes[i] for i in element["nodes"]], element["tags"])
    return buildings

  def location_inside_building(self, building, location):
    x = location[0]
    y = location[1]
    n = len(building)
    inside = False
    p1x, p1y = building[0]
    for i in range(n + 1):
      p2x, p2y = building[i % n]
      if y > min(p1y, p2y):
        if y <= max(p1y, p2y):
          if x <= max(p1x, p2x):
            if p1y != p2y:
              xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
            if p1x == p2x or x <= xints:
              inside = not inside
      p1x, p1y = p2x, p2y
    return inside


application = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/check_location', CheckLocation),
  ('/login', login.Login),
  ('/createuser', login.CreateUser),
], debug=True)
