import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import *

# access tokens:
Casting_Assistant = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklIWEVFV1l3dF91bEdKTnhCWE5EcyJ9.eyJpc3MiOiJodHRwczovL2Fib3htc2EzZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVlMmVkYWVmNDVlODEwYmEyYjc2NWQ2IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1OTY2NzUwNDMsImV4cCI6MTU5Njc2MTQ0MywiYXpwIjoiZVhPS3pDWHBDTmtReG5BUTVReDRHdllSVjdNb3JVTGgiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.bDS1RoOz4MWa8rlyqpJ6eGRXRegD-FzEvwrMMhsK6dxZ9v3qUZRRev99DWe0MZTD78vh05t8DHXjEFA5Vf3XYYzfB6Q4r-g7cJSveayD9J0LXPSahuzOLD78Xw8mC9SKdZKG4kjU3U0nR4E70q5fY0ySuqRq0Hn9teaSCo-JUPmYVtUbPqHcCW99dVJJgVQ-AUzrycdUBPr6VDLmFQ0y2yaYekxuESwirS8JCgWA9y7_BXFDkPR3WWOcFs3CPPsXFCyWtTdSvywNI6mOnYfjS_mdEZpBI6nSeMMh4VVkucuUsfnvbZ5RPLVW7AXnvqgBFuAMz9iZWNlkOAmNiI_gGg"
Casting_Director = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklIWEVFV1l3dF91bEdKTnhCWE5EcyJ9.eyJpc3MiOiJodHRwczovL2Fib3htc2EzZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYyOWZhN2QzMmNlYTMwMjIxMTQ1YjRiIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1OTY2NzUxMTksImV4cCI6MTU5Njc2MTUxOSwiYXpwIjoiZVhPS3pDWHBDTmtReG5BUTVReDRHdllSVjdNb3JVTGgiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.fyuIx1ojivQoMqk8IIOgi9LWHijIfYdyZ2WnoaWghYiDj-8SydMIpF07HqgmKnYwA3HxfnciNEVg2FjwUspcixJKGiQOwL06G54fUY54yoCqzIs35PacHVL3MmPn2WqXzhpjs5FUYxXIueTER71oNOX66dphoHPUKt3_Ld3jUANYZCkdNkyBzdUtmshWVg8Ih-KcmA2ASz-1k4xomhrG8ba0XgiSQQWLKJK4vDbt4V9ewaLCgbLRzRE0eva4LJ9Sp6jX763DLHd2g0Z048_dWrNRQBCiLOVW7Z3wMQlPzWGVYkIt5kTEvNxrIsqtJyMmiW5pbe1w-YslYL28r_Zk9Q"
Executive_Producer = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklIWEVFV1l3dF91bEdKTnhCWE5EcyJ9.eyJpc3MiOiJodHRwczovL2Fib3htc2EzZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVlYjA5ZWIzNTdjMTUwYjZjMjJlYzE3IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1OTY2NzUxNTgsImV4cCI6MTU5Njc2MTU1OCwiYXpwIjoiZVhPS3pDWHBDTmtReG5BUTVReDRHdllSVjdNb3JVTGgiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.ud2zF8yTI5WFNyHr7M9GLCkifFglYLvlHIPYjaEWsUkRknLPh2bH6AuoCLw3VwvdzN-oeNq4jr3qZVw9x-2PsyUMNeMiOz_IcErMNlKJVoW1BO8M-e4uKkRiuIQg64Ak2qKIAdTU1kLdN5AfuYQaZLWavfJWX-6_NNpuGgqqqG39fEl4AxzQ4bjieq6Pk4PDYnthd19Lkkml-pTP-nFU46s9B0vZiHuGN8Svl9RWHguh2nhuZrRIR4iexEpTx_NC1_2FDDdQDXoUFFizVKFjyn_iVoWo9JR9bIB8sIZB0I9ROwL1dkX1EzKqkjrCb7lM4QO4-5v-pa6NITb7pw_7Zg"


class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ #

    def setUp(self):  # run before each test
        """Define test variables and initialize app."""
        self.app = create_app()  # 1. initialize the app
        self.client = self.app.test_client  # 2. initialize test client

        # 3. set up the database (use diff database for test)
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            'postgres', 'd7oom11', 'localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        # 4. add some sample to test it (create it every time i run)
        self.new_actor = {
            "name": "m7md",
            "age": 22,
            "gender": "male"
        }

        self.new_movie = {
            "title": "tbn",
            "release_date": "2015-4-9"
        }

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ #

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ #

    def tearDown(self):  # run after each test
        """Executed after reach test"""
        pass

    # every test method must start with ( test_........(self) )

    #----------------------------------------------------------------------------#
    # Test for Casting Assistant Role
    #----------------------------------------------------------------------------#

    def test_get_actors_for_Casting_Assistant(self):
        res = self.client().get(
            '/actors',
            headers={
                "Authorization": 'bearer ' +
                Casting_Assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_Actors'], len(data['Actors']))

    #  ________________________________________________________________ #

    def test_get_movies_for_Casting_Assistant(self):
        res = self.client().get(
            '/movies',
            headers={
                "Authorization": 'bearer ' +
                Casting_Assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_Movies'], len(data['Movies']))

    # ________________________________________________________________ #

    def test_add_new_actor(self):
        # json=self.new_actor ( that i create up in the setup )
        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers={
                "Authorization": 'bearer ' +
                Casting_Assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # ________________________________________________________________ #

    def test_add_new_movie(self):
        # json=self.new_actor ( that i create up in the setup )
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers={
                "Authorization": 'bearer ' +
                Casting_Assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # ________________________________________________________________ #

    def test_update_actor_age(self):
        res = self.client().patch(
            '/actors/1',
            json={
                'age': 18},
            headers={
                "Authorization": 'bearer ' +
                Casting_Assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # ________________________________________________________________ #

    def test_update_movie_title(self):
        res = self.client().patch(
            '/movies/1',
            json={
                'title': 'title is changed'},
            headers={
                "Authorization": 'bearer ' +
                Casting_Assistant})
        data = json.loads(res.data)

        #actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # ________________________________________________________________ #

    def test_delete_actor(self):  # must change the id every time runing the test
        res = self.client().delete(
            '/actors/1',
            headers={
                "Authorization": 'bearer ' +
                Casting_Assistant})
        data = json.loads(res.data)

        #actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # ________________________________________________________________ #

    def test_delete_movie(self):  # must change the id every time runing the test
        res = self.client().delete(
            '/movies/1',
            headers={
                "Authorization": 'bearer ' +
                Casting_Assistant})
        data = json.loads(res.data)

        #movie = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')

    #----------------------------------------------------------------------------#
    # Test for Casting Director Role
    #----------------------------------------------------------------------------#

    def test_get_actors_for_Casting_Director(self):
        res = self.client().get(
            '/actors',
            headers={
                "Authorization": 'bearer ' +
                Casting_Director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #  ________________________________________________________________ #

    def test_get_movies_for_Casting_Director(self):
        res = self.client().get(
            '/movies',
            headers={
                "Authorization": 'bearer ' +
                Casting_Director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # ________________________________________________________________ #

    def test_add_new_actor_for_Casting_Director(self):
        # json=self.new_actor ( that i create up in the setup )
        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers={
                "Authorization": 'bearer ' +
                Casting_Director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # ________________________________________________________________ #

    def test_add_new_movie_for_Casting_Director(self):
        # json=self.new_actor ( that i create up in the setup )
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers={
                "Authorization": 'bearer ' +
                Casting_Director})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')

    # ________________________________________________________________ #

    def test_update_actor_age_for_Casting_Director(self):
        res = self.client().patch(
            '/actors/1',
            json={
                'age': 18},
            headers={
                "Authorization": 'bearer ' +
                Casting_Director})
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # ________________________________________________________________ #

    def test_update_movie_title_for_Casting_Director(self):
        res = self.client().patch(
            '/movies/1',
            json={
                'title': 'title is changed'},
            headers={
                "Authorization": 'bearer ' +
                Casting_Director})
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # ________________________________________________________________ #

    # must change the id every time runing the test
    def test_delete_movie_for_Casting_Director(self):
        res = self.client().delete(
            '/movies/1',
            headers={
                "Authorization": 'bearer ' +
                Casting_Director})
        data = json.loads(res.data)

        #movie = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')

    #----------------------------------------------------------------------------#
    # Test for Executive Producer Role
    #----------------------------------------------------------------------------#

    def test_get_actors_for_Executive_Producer(self):
        res = self.client().get(
            '/actors',
            headers={
                "Authorization": 'bearer ' +
                Executive_Producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #  ________________________________________________________________ #

    def test_get_movies_for_Executive_Producer(self):
        res = self.client().get(
            '/movies',
            headers={
                "Authorization": 'bearer ' +
                Executive_Producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # ________________________________________________________________ #

    def test_add_new_actor_for_Executive_Producer(self):
        # json=self.new_actor ( that i create up in the setup )
        res = self.client().post(
            '/actors',
            json=self.new_actor,
            headers={
                "Authorization": 'bearer ' +
                Executive_Producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # ________________________________________________________________ #

    def test_add_new_movie_for_Executive_Producer(self):
        # json=self.new_actor ( that i create up in the setup )
        res = self.client().post(
            '/movies',
            json=self.new_movie,
            headers={
                "Authorization": 'bearer ' +
                Executive_Producer})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # ________________________________________________________________ #

    def test_update_actor_age_for_Executive_Producer(self):
        res = self.client().patch(
            '/actors/1',
            json={
                'age': 18},
            headers={
                "Authorization": 'bearer ' +
                Executive_Producer})
        data = json.loads(res.data)

        #actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # ________________________________________________________________ #

    # must change the id every time runing the test
    def test_delete_actor_for_Executive_Producer(self):
        res = self.client().delete(
            '/actors/1',
            headers={
                "Authorization": 'bearer ' +
                Executive_Producer})
        data = json.loads(res.data)

        #actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # ________________________________________________________________ #

    def test_update_movie_title_for_Executive_Producer(self):
        res = self.client().patch(
            '/movies/1',
            json={
                'title': 'title is changed'},
            headers={
                "Authorization": 'bearer ' +
                Executive_Producer})
        data = json.loads(res.data)

        #movie = Movie.query.filter(Movie.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # ________________________________________________________________ #

    # must change the id every time runing the test
    def test_delete_movie_for_Executive_Producer(self):
        res = self.client().delete(
            '/movies/1',
            headers={
                "Authorization": 'bearer ' +
                Executive_Producer})
        data = json.loads(res.data)

        #movie = Movie.query.filter(Movie.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # ________________________________________________________________ #

    # Run the test, by running python <test_file_name>.py in the command line.

    # ________________________________________________________________ #


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
