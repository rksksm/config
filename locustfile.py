from locust import HttpLocust, TaskSet
import json

def configPost(l):
    l.client.post("/config", json.dumps('{"tenant": "tata","integration_type": "byee","configuration": {"username": "ujyfjhgkgk","password": "dc","wsdl_urls": {"session_url": "scs","booking_url": "sd123"}}}'))
#
# def health(l):
#     l.client.get("/")
#
# def configGet(l):
#     l.client.get("/config?tenant=hello&integration_type=hello")

class UserBehavior(TaskSet):
    # tasks = {configGet: 2, configPost: 1}

    def on_start(self):
        configPost(self)

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000