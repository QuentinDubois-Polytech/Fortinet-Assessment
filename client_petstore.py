"""
HTTP Client for Petstore
"""

from dataclasses import dataclass

import requests
import argparse
import logging

BASE_URL = "https://petstore.swagger.io/v2"
BASE_HEADER = {"accept": "application/json"}


@dataclass
class Order:
    """
    Order dataclass
    """
    id: int
    pet_id: int
    quantity: int
    ship_date: str
    status: str
    complete: bool

    def convertToApi(self):
        """
        Convert Order to API format
        """
        return {
            "id": self.id,
            "petId": self.pet_id,
            "quantity": self.quantity,
            "shipDate": self.ship_date,
            "status": self.status,
            "complete": self.complete
        }

    @classmethod
    def convertFromApi(cls, data: dict[str, any]) -> 'Order':
        """
        Convert API Order object into to Order object
        :param data: API Order object
        :return: Order object converted
        """
        return cls(
            data.get("id"),
            data.get("petId"),
            data.get("quantity"),
            data.get("shipDate"),
            data.get("status"),
            data.get("complete")
        )


def create_order(order: Order) -> requests.Response:
    """
    Call to petstore's API to create an order
    :param order: Order to create
    :return: response of the request
    """
    url = f"{BASE_URL}/store/order"
    data = order.convertToApi()
    r = requests.post(url, json=data, headers=BASE_HEADER)
    return r


def get_order_by_id(order_id: id) -> requests.Response:
    """
    Call to petstore's API to get an order by its ID
    :param order_id: order ID to retrieve
    :return: response of the request
    """
    url = f"{BASE_URL}/store/order/{order_id}"
    r = requests.get(url, headers=BASE_HEADER)
    return r


def delete_order_by_id(order_id: id) -> requests.Response:
    """
    Call to petstore's API to delete an order by its ID
    :param order_id: order ID to delete
    :return: response of the request
    """
    url = f"{BASE_URL}/store/order/{order_id}"
    r = requests.delete(url, headers=BASE_HEADER)
    return r


def display(request: requests.Response) -> None:
    """
    Display information about the request
    :param request: request to display
    """
    logging.info("-----General Informations-----")
    logging.info(f"URL : {request.url}")
    logging.info(f"Status code : {request.status_code}")

    logging.debug("-----Request Informations-----")
    logging.debug(f"Headers : {request.headers}")
    logging.debug(f"Body Request : {request.request.body}")

    logging.debug("-----Response Informations-----")
    logging.debug(f"Data : {request.text}")


def parse_arguments() -> argparse.Namespace:
    """
    Parse CLI arguments
    :return: arguments parsed
    """
    parser = argparse.ArgumentParser("Client for Petstore")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")

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

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Verbose mode activated")
    else:
        logging.basicConfig(level=logging.INFO)

    match args.command:
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
