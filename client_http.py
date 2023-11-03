import requests
import argparse

BASE_URL = "https://petstore.swagger.io/v2"
BASE_HEADER = {"accept": "application/json"}

class Order:
    def __init__(self, id, pet_id, quantity, ship_date, status, complete):
        self.id = id
        self.pet_id = pet_id
        self.quantity = quantity
        self.ship_date = ship_date
        self.status = status
        self.complete = complete

    def convertToApi(self):
        return {
            "id": self.id,
            "petId": self.pet_id,
            "quantity": self.quantity,
            "shipDate": self.ship_date,
            "status": self.status,
            "complete": self.complete
        }

def create_order(order):
    url = f"{BASE_URL}/store/order"
    data = order.convertToApi()
    print(data)
    r = requests.post(url, json=data, headers=BASE_HEADER)
    return r

def get_order_by_id(order_id):
    url = f"{BASE_URL}/store/order/{order_id}"
    r = requests.get(url, headers=BASE_HEADER)
    return r

def delete_order_by_id(order_id):
    url = f"{BASE_URL}/store/order/{order_id}"
    r = requests.delete(url, headers=BASE_HEADER)
    return r

def display(request):
    print("-----General Informations-----")
    print(f"URL : {request.url}")
    print(f"Status code : {request.status_code}")

    print("-----Request Informations-----")
    print(f"Headers : {request.headers}")
    print(f"Body Request : {request.request.body}")

    print("-----Response Informations-----")
    print(f"Data : {request.text}")


def parse_arguments():
    parser = argparse.ArgumentParser("Client for Petstore")
    subparsers = parser.add_subparsers(title="commands", dest="command", help="Available commands.")

    create_order_parser = subparsers.add_parser("create", help="Create an order")
    create_order_parser.add_argument("-i", "--id", help="Order ID", type=int)
    create_order_parser.add_argument("-p", "--pet_id", help="Pet ID", type=int)
    create_order_parser.add_argument("-q", "--quantity", help="Quantity", type=int)
    create_order_parser.add_argument("-s", "--ship_date", help="Ship Date", type=str)
    create_order_parser.add_argument("-S", "--status", help="Status", type=str)
    create_order_parser.add_argument("-c", "--complete", help="Complete", type=bool)

    get_order_parser = subparsers.add_parser("get", help="Get an order")
    get_order_parser.add_argument("-i", "--id", help="Order ID", type=int)

    delete_order_parser = subparsers.add_parser("delete", help="Delete an order")
    delete_order_parser.add_argument("-i", "--id", help="Order ID", type=int)

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    match(args.command):
        case "create":
            order = Order(args.id, args.pet_id, args.quantity, args.ship_date, args.status, args.complete)
            request = create_order(order)
            display(request)
        case "get":
            request = get_order_by_id(args.id)
            display(request)
        case "delete":
            request = delete_order_by_id(args.id)
            display(request)
        case _:
            print("Invalid command")



