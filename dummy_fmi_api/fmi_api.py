from flask import redirect, url_for, Flask, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

teacher_groups_json = [
    {
        "specializare":"Informatica",
        "ani":[
            {
                "an":1,
                "serii":[
                    {
                        "seria":3,
                        "grupe":["131","132","133"]
                    }
                ]
            },
            {
                "an":2,
                "serii":[
                    {
                        "seria":3,
                        "grupe":["231","232","233"]
                    }
                ]
            }
        ]
    }
]

groups_json = [
    {
        "specializare":"Informatica",
        "ani":[
            {
                "an":1,
                "serii":[
                    {
                        "seria":3,
                        "grupe":["131","132","133"]
                    },
                    {
                        "seria":4,
                        "grupe":["141","142","143"]
                    }
                ]
            },
            {
                "an":2,
                "serii":[
                    {
                        "seria":3,
                        "grupe":["231","232","233"]
                    },
                    {
                        "seria":4,
                        "grupe":["241","242","243"]
                    }
                ]
            }
        ]
    },
    {
        "specializare":"Matematica",
        "ani":[
            {
                "an":1,
                "serii":[
                    {
                        "seria":1,
                        "grupe":["111","112","113"]
                    },
                    {
                        "seria":2,
                        "grupe":["121","122","123"]
                    }
                ]
            },
            {
                "an":2,
                "serii":[
                    {
                        "seria":1,
                        "grupe":["211","212","213"]
                    },
                    {
                        "seria":2,
                        "grupe":["221","222","223"]
                    }
                ]
            }
        ]
    }
]

@app.route('/auth_user_normal')
def auth_user_normal():
    url = request.args.get("redirect_uri")
    return redirect(url + "?fname=George&lname=Glavan&email=george.glavan@gmail.com&is_admin=0&is_student=1&is_teacher=0&group=233")

@app.route('/auth_admin')
def auth_admin():
    url = request.args.get("redirect_uri")
    return redirect(url + "?fname=Neacsu&lname=Radu&email=admin.admin@gmail.com&is_admin=1&is_student=0&is_teacher=0")

@app.route('/auth_profesor')
def auth_profesor():
    url = request.args.get("redirect_uri")
    return redirect(url + "?fname=Costi&lname=Cir&email=costi.cir@gmail.com&is_admin=0&is_student=0&is_teacher=1")

@app.route('/resources/')
def res():
    return json.dumps(groups_json)

@app.route('/resources_teacher')
def res_tea():
    return json.dumps(teacher_groups_json)

if __name__ == "__main__":
    app.run(port=10000,host='0.0.0.0')