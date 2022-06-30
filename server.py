from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

countries = [
    {"id": 1, "name": "Thailand", "capital": "Bangkok", "area": 513120},
    {"id": 2, "name": "Australia", "capital": "Canberra", "area": 7617930},
    {"id": 3, "name": "Egypt", "capital": "Cairo", "area": 1010408},
]

def _find_next_id():
    return max(country["id"] for country in countries) + 1

@app.route("/countries",methods=['GET'])
def get_countries():
    return jsonify(countries)

@app.route("/countries",methods=['POST'])
def add_country():
    if request.is_json:
        country = request.get_json()
        country["id"] = _find_next_id()
        countries.append(country)
        return country, 201
    return {"error": "Request must be JSON"}, 415

@app.route("/countries/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def choosemethod(id):
    print(request.method)
    if request.method == "GET":
        return find_country(id)
    elif request.method == "PUT":
        return update(id)
    elif request.method == "DELETE":
        return delete(id)
        
def find_country(id):
    for data in  countries:
        if data['id'] == id:
            return jsonify(data)
    return jsonify('Error, id not founded'), 404

def delete(id):
    for data in  countries:
        if data['id'] == id:
            countries.remove(data)
            return jsonify({}), 204
    return jsonify('Error, id not founded'), 404
     
def update(id):
    for data in  countries:
        if data['id'] == id:
            data["name"] = request.json["name"]
            data["capital"] = request.json["capital"]
            data["area"] = request.json["area"]
            return jsonify(data), 200
    return jsonify('Error, id not founded'), 404
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=8090)