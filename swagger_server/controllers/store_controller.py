import connexion
import six

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server import util


def show_storefront_products(page=None, limit=None):  # noqa: E501
    """Returns a paginated list of products available items in the storefront.

    Returns a paginated list of products available items in the storefront. # noqa: E501

    :param page: Page number (starts at 1)
    :type page: int
    :param limit: Number of items per page
    :type limit: int

    :rtype: InlineResponse200
    """
    return 'do some magic!'
