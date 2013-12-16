import json
import webapp2

import models


class Login(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "text/json"

        username = self.request.get('username', None)

        if username is None or len(username) < 1:
            self.response.write(json.dumps({'success': False}))
            return

        user = models.User.get_by_id(username.lower(), parent=models.app_key())
        if user is None:
            self.response.write(json.dumps({'success': False}))
            return

        self.response.write(json.dumps({'success': True, 'user': user.username}))


class CreateUser(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = "text/json"

        username = self.request.get('username', None)

        if username is None:
            self.response.write(json.dumps({
                'success': False,
                'message': 'Username missing'
            }))
            return

        if len(username) < 3:
            self.response.write(json.dumps({
                'success': False,
                'message': 'Username too short (should be at least 3 characters long)'
            }))
            return

        user = models.User.get_by_id(username.lower(), parent=models.app_key())
        if not user is None:
            self.response.write(json.dumps({
                'success': False,
                'message': 'Username already exists'
            }))
            return

        user = models.User(id=username.lower(), parent=models.app_key())
        user.username = username
        user.put()

        self.response.write(json.dumps({
            'success': True,
            'user': user.username
        }))
