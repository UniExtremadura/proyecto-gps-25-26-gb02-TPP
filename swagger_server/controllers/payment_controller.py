import connexion
import six

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.payment_method import PaymentMethod  # noqa: E501
from swagger_server import util


def add_payment_method(body=None):  # noqa: E501
    """Add a new payment method

    Add a new payment method # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = PaymentMethod.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_payment_method(payment_method_id):  # noqa: E501
    """Delete a payment method by ID.

    Delete a payment method by ID. # noqa: E501

    :param payment_method_id: 
    :type payment_method_id: int

    :rtype: None
    """
    return 'do some magic!'


def show_user_payment_methods():  # noqa: E501
    """Returns a list of payment methods for the selected user.

    Returns a list of payment methods for the selected user. # noqa: E501


    :rtype: List[PaymentMethod]
    """
    return 'do some magic!'
