import connexion
import six

from swagger_server.models.cart_body import CartBody  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.product import Product  # noqa: E501
from swagger_server import util


def add_to_cart(body=None):  # noqa: E501
    """Add a product to the cart.

    Add a product to the cart. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = CartBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def get_cart_products():  # noqa: E501
    """Get the products from a user&#x27;s cart.

    Get the products from a user&#x27;s cart. # noqa: E501


    :rtype: List[Product]
    """
    return 'do some magic!'


def remove_from_cart(product_id, type=None):  # noqa: E501
    """Remove a product from the cart.

    Remove a product from the cart. # noqa: E501

    :param product_id: 
    :type product_id: int
    :param type: Product type: &#x27;song&#x27;/&#x27;0&#x27;, &#x27;album&#x27;/&#x27;1&#x27;, &#x27;merch&#x27;/&#x27;2&#x27;. If not specified, searches all tables.
    :type type: str

    :rtype: None
    """
    return 'do some magic!'
