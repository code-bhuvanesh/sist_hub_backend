import requests


def getToken():
    url = "http://localhost:8000/api-token-auth/"
    userData = {
        'username' : 'admin',
        'password' : '1234'
    }

    response = requests.post(url=url, json=userData)

    return response.json()["token"]

# print(getToken())

def createUser():

    # userData = {
    #     "username":"admin",
    #     "password":"1234",
    #     "user_type":"admin",
    #     "first_name":"admin",
    #     "last_name":"admin",
    #     "email":"admin@sist.com",
    #     "regno":41110296,
    #     "phone_number":"7010362931",
    #     "course":"CSE",
    #     "section":"a4",
    #     "branch":"BE",
    #     # "field1":"BE2",
    #     # "field2":12,
    # }

    userData = {
        "username":"bhuvanesh",
        "password":"1234",
        "user_type":"student",
        "first_name":"bhuvanesh",
        "last_name":"d",
        "regno":41110296,
        "phone_number":"7010362931",
        "course":"CSE",
        "section":"a4",
        "branch":"BE",
        # "field1":"BE2",
        # "field2":12,
    }
    userData["email"] = userData["first_name"]+str(userData["regno"])+"@sisthub.com" 


    url = 'http://127.0.0.1:8000/api/users/'
    headers = {"Authorization": f"TOKEN {getToken()}"}

    response = requests.post(url,headers=headers, json = userData)
    # response = requests.post(url,json = userData)

    print(response.text)
createUser()