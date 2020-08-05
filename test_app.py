import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import *
from auth import AuthError, requires_auth

# access tokens:
Casting_Assistant = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklIWEVFV1l3dF91bEdKTnhCWE5EcyJ9.eyJpc3MiOiJodHRwczovL2Fib3htc2EzZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVlMmVkYWVmNDVlODEwYmEyYjc2NWQ2IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1OTY2NjczMTAsImV4cCI6MTU5NjY3NDUxMCwiYXpwIjoiZVhPS3pDWHBDTmtReG5BUTVReDRHdllSVjdNb3JVTGgiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.T6f71oQaAg8uDbLLAXKyaeC2CxV_Fd4ae0WAGcBWky7rzn3P96jGsuXkzf1bzZd4rV14FkxuoYP3FfLR66YQ0U1FjdIm_FlyfYZlxzoi-lPZEqqcFcOo2S493FbeD0OlzGqaAS7L2k48wTyomjPss6HGpqZpG3a-6GzlGiwQSbRK029xlnqB89wLDATlwLKJEABcga1MvHrB9AnxlYffUIvy9vCmeo-aNOOhbBKgxoyqMOpL5Uua6mThSSGxLsinnbOSXvzF7SNSqIwF2C0L91KZCBalwbz06nPsBp7DiPjLviET7F0K5NJjE2k1HdHz3OMwdrUyhHPXgRlXtILjbA"
Casting_Director = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklIWEVFV1l3dF91bEdKTnhCWE5EcyJ9.eyJpc3MiOiJodHRwczovL2Fib3htc2EzZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWYyOWZhN2QzMmNlYTMwMjIxMTQ1YjRiIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1OTY2NjczODksImV4cCI6MTU5NjY3NDU4OSwiYXpwIjoiZVhPS3pDWHBDTmtReG5BUTVReDRHdllSVjdNb3JVTGgiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.QAsQgX73pVkBTRJpnIPATEnqTItlPWVkADbLIDFfzohBde0BVPbhRUoTVY9B90zPBa1FFdEs6mbRiN_Z0mf-FeP16VwzUapak3KjTdfFbpQP9BGpQKnDXzNJxvansuBqkTNSU_QmhIVnCMvwqPK7Jo0XVSsRbA7wNzP0pauAZsXAUfmZfGcN5YNip_kuvzUTJciIb5Tmjhj6NOwOigvNwae5HhMcGueVHZjU2Jvdt7-35dNoDg77Rd2we7ECea5Sll2aOI3q2GEF9EP4YiiqAYDXtiDJ_snDwR43lvZfXGbgHaZ7jd5VOYbgXwbVpQlZIGGWPFzBZ0IJAT9fEABPVw"
Executive_Producer = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IklIWEVFV1l3dF91bEdKTnhCWE5EcyJ9.eyJpc3MiOiJodHRwczovL2Fib3htc2EzZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVlYjA5ZWIzNTdjMTUwYjZjMjJlYzE3IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE1OTY2Njc0NTIsImV4cCI6MTU5NjY3NDY1MiwiYXpwIjoiZVhPS3pDWHBDTmtReG5BUTVReDRHdllSVjdNb3JVTGgiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.He4KW3YPOtrzBgPGLoy2fc0fZSCjhDT3iM1DCxlkTLszBXPC58W10fMQ1Eol_5pG-HvLoq51j4vw0iTD03cB_RL3iYmb_RGDdjwKWxXszcQO3GZmWNfaTQDaNheq7ez6R0YYLGRyNM5ulRHsmdnfncuD3ZqR3SRYbgSCybUPprQO4wfiI4DCI0ZCsL32tQAupIbO5P952IpEW5VZJvvflZI24NrA-05VWCB10ocuALxaP5C4scwtNpANgXRtu_UuqpvA9OzPX8PBo-tw7XHqf3zlzyyDWxctUBB13CZkPXu1DH_2Iemzk2ug7DO_VRWjR4goLLN3NvzydvETAvGJ8w"


class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    # ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ #

    def setUp(self): # run before each test
        """Define test variables and initialize app."""
        self.app = create_app() # 1. initialize the app
        self.client = self.app.test_client #2. initialize test client

        self.database_name = "capstone_test" # 3. set up the database (use diff database for test)
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

    def tearDown(self): # run after each test
        """Executed after reach test"""
        pass


    # every test method must start with ( test_........(self) ) 

    #----------------------------------------------------------------------------#
    # Test for Casting Assistant Role
    #----------------------------------------------------------------------------#

    def test_get_actors_for_Casting_Assistant(self):
        res = self.client().get('/actors' , headers={"Authorization": 'bearer '+Casting_Assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_Actors'], len(data['Actors']))

    #  ________________________________________________________________ #

    def test_get_movies_for_Casting_Assistant(self):
        res = self.client().get('/movies' , headers={"Authorization": 'bearer '+Casting_Assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_Movies'], len(data['Movies']))


    # ________________________________________________________________ #

    def test_add_new_actor(self):
        # json=self.new_actor ( that i create up in the setup )
        res = self.client().post('/actors', json=self.new_actor , headers={"Authorization": 'bearer '+Casting_Assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # ________________________________________________________________ #

    def test_add_new_movie(self):
        # json=self.new_actor ( that i create up in the setup )
        res = self.client().post('/movies', json=self.new_movie , headers={"Authorization": 'bearer '+Casting_Assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # ________________________________________________________________ #

    def test_update_actor_age(self):      
        res = self.client().patch('/actors/1', json={'age': 18} , headers={"Authorization": 'bearer '+Casting_Assistant})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # ________________________________________________________________ #

    def test_update_movie_title(self):      
        res = self.client().patch('/movies/1', json={'title': 'title is changed'} , headers={"Authorization": 'bearer '+Casting_Assistant})
        data = json.loads(res.data)

        #actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # ________________________________________________________________ #

    def test_delete_actor(self): # must change the id every time runing the test
        res = self.client().delete('/actors/1' , headers={"Authorization": 'bearer '+Casting_Assistant})
        data = json.loads(res.data)

        #actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # ________________________________________________________________ #

    def test_delete_movie(self): # must change the id every time runing the test
        res = self.client().delete('/movies/1' , headers={"Authorization": 'bearer '+Casting_Assistant})
        data = json.loads(res.data)

        #movie = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')








    # ________________________________________________________________ #

    # Run the test, by running python <test_file_name>.py in the command line.

    # ________________________________________________________________ #



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
