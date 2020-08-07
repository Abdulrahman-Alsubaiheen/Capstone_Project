import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import *

# access tokens:
Casting_Assistant = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklIWEVFV1l3dF91bEdKTnhCWE5EcyJ9.eyJpc3MiOiJodHRwczovL2Fib3htc2EzZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVlMmVkYWVmNDVlODEwYmEyYjc2NWQ2IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1OTY4MDk0MDQsImV4cCI6MTU5Njg5NTgwNCwiYXpwIjoiZVhPS3pDWHBDTmtReG5BUTVReDRHdllSVjdNb3JVTGgiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.dxxxK3arkR_jNm_ekRRYVSyHMuI-2NMeLzU6YiTfvR1Xj1J8YzHFG6VuKLdTGfo_Evulaee6ewfCkJkwHm7I_nxjth1YqFTJN2cmJXjuArgRhnlWlxW_eDok5QlH-fqAOdxdIDTVfpUyIZtSBzLJkkzFbNPffFdpxNhND3DKybFn4oe3DwytAyediMvcgcXv1VvbPmtxORvNgeWjmAOzO2API-a49WdIbXH5Q1DY25npqx5_AA_uHEAotZKYCAlIfxngXw9gjdSm-JD8kFH94LNIjHHru5zvFN-KAUIHmuMyttk7pPxQJph4OO7vmXbUPd0dNe8Q18ISKtJFpdFNrw"
Casting_Director = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklIWEVFV1l3dF91bEdKTnhCWE5EcyJ9.eyJpc3MiOiJodHRwczovL2Fib3htc2EzZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYyOWZhN2QzMmNlYTMwMjIxMTQ1YjRiIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1OTY4MDk0NjYsImV4cCI6MTU5Njg5NTg2NiwiYXpwIjoiZVhPS3pDWHBDTmtReG5BUTVReDRHdllSVjdNb3JVTGgiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.nHZ8zCRH-8bSn-jG0DQ00bT_h8CyrV9DJ8cM2sEIwIuyEIRIR0Y7RTgCWqB5lujGG3i6--2vMFC_BO0ylB4oqB9QKuxAF2qol8RF-M1lWn3TbBq9l6nmR7kcAhaKxgninrtHnpChEj0lkO5tbWcZtz4kSfHjOi_E594qmK060pPs8XEaASSRCR35DMW8oGfR_fO0DziCk8jzTlIqSleD99hpz5M_W1HoUodCvyILeOYq38aevc8thnxU-Dm_3oeBR1C_m0wZ9I5RX9bvuP0YAe_LDRYFB496XOjVIZJFt7o5jOKTYqVYjqKpxV-4tcMB9OLYS1lNKx5sTZSX7uCdJQ"
Executive_Producer = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklIWEVFV1l3dF91bEdKTnhCWE5EcyJ9.eyJpc3MiOiJodHRwczovL2Fib3htc2EzZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVlYjA5ZWIzNTdjMTUwYjZjMjJlYzE3IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1OTY4MDk2MDksImV4cCI6MTU5Njg5NjAwOSwiYXpwIjoiZVhPS3pDWHBDTmtReG5BUTVReDRHdllSVjdNb3JVTGgiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.TZcQWyKy_R5eOXiWXgP3ZoxKPBtC8bg2QefoVWF9FmSvraIgg39YpNRrIsL5BEHO4GfXMCFstEsD4L_7XBm34o1ssbhhn0zb7srGffJuCmg34Qi5fXSUO2e76T0a3GxUWKYWIbKmOp4-NR6BRsOeHZBYUZmhb_JFxID7TUatopuFtjSaDBc0SZx_3jGTIKWaeJ-qIStc61ipcIvHW3h8YlJcyWd4MnK6AaPeH9_BUZwB8jVUjxv-0MAGta4IclCAqzmgwUxMRzftx98zxNYJicplrtevb6ktICLWHHfCh6mCKXyM2EyKXZ0wEqM5DgzwqEbXrO0rfiqFvB_EZOi73w"


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
