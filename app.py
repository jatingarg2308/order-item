from yaml import safe_load
from easydict import EasyDict
from flask import *
from flask_expects_json import expects_json
from werkzeug.exceptions import HTTPException, abort

from schema import get_schema

SCHEMA = get_schema()
app = Flask(__name__)
OFFER_TYPES = ['DELIVERY', 'FLAT']

def items_cost(order_items):
    cost = 0

    for item in order_items:
        cost += item['quantity'] * item['price']

    return cost

def distance_cost(distance):
    km_distance = distance/1000
    if 0<=km_distance<10:
        return 5000
    if 10<km_distance<20:
        return 10000
    if 20<=km_distance<50:
        return 50000
    return 100000

def apply_flat_offer(offer, cost):
    offer_val = offer.get('offer_val', 0)
    return cost - min(cost, offer_val)


def calculate_cost(req):
    item_cost = items_cost(req['order_items'])

    dist_cost = distance_cost(req['distance'])

    total_cost = item_cost + dist_cost
    
    if "offer" in req:
        offer = req['offer']
        if offer['offer_type'] == 'FLAT':
            total_cost = apply_flat_offer(offer, total_cost)
        elif offer['offer_type'] == 'DELIVERY':
            total_cost -= dist_cost
        else:
            raise HTTPException(response=Response(
                json.dumps({
                    "code": 400,
                    "name": "Bad Request",
                    "description": f"{OFFER_TYPES} offer_type values are only allowed"
                }), status=400))
    
    return total_cost

@app.errorhandler(HTTPException)
def handle_exception(e):
    try:
        description = e.description.message
    except AttributeError:
        description = e.description

    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": description
    })
    
    response.content_type = "application/json"
    return response


@app.route("/", methods=['GET'])
@expects_json(SCHEMA)
def get_total_cost():
    params = request.json
    cost = calculate_cost(params)
    
    return {"order_total": cost}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
