import connexion
import six

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.models.purchase import Purchase  # noqa: E501
from swagger_server import util


def set_purchase(body=None):  # noqa: E501
    """Set a product as purchased by the user.

    Set a product as purchased by the user. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: InlineResponse2001
    """
    if connexion.request.is_json:
        body = Purchase.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
