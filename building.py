import json
import webapp2

import models


class AddBuildingTag(webapp2.RequestHandler):
    def post(self):
        self.response.headers['Content-Type'] = "text/json"

        username = self.request.get('username', None)
        building = self.request.get('building', None)
        name = self.request.get('name', None)

        if username is None or len(username) < 1:
            self.response.write(json.dumps({
                'success': False,
                'message': 'User missing'
            }))
            return

        user = models.User.get_by_id(username.lower(), parent=models.app_key())
        if user is None:
            self.response.write(json.dumps({
                'success': False,
                'message': 'User does not exist'
            }))
            return

        building_id = 0
        try:
            building_id = int(building)
        except:
            building_id = 0

        if building_id == 0:
            self.response.write(json.dumps({
                'success': False,
                'message': 'Building id missing'
            }))
            return

        if name is None or len(name) < 1:
            self.response.write(json.dumps({
                'success': False,
                'message': 'Name is missing'
            }))
            return

        b = models.BuildingTag(parent=models.app_key())
        b.username = username.lower()
        b.building = building_id
        b.name = name
        b.put()

        self.response.write(json.dumps({'success': True}))
