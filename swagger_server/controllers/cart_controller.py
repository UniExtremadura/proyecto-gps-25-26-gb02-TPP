import connexion
import six

from swagger_server.models.cart_body import CartBody  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.product import Product  # noqa: E501
from swagger_server import util


def add_to_cart(body=None):
    """
    Añade un producto al carrito del usuario autenticado.
    
    Permite agregar canciones, álbumes o merchandising al carrito de compras.
    Valida que el producto no esté ya en el carrito para evitar duplicados.
    Para merchandising, permite especificar la cantidad de unidades.
    
    Validaciones:
        - El cuerpo de la petición debe ser JSON válido
        - El usuario debe estar autenticado (token válido)
        - Debe proporcionar exactamente uno de: songId, albumId o merchId
        - El producto no debe existir previamente en el carrito
    
    Operaciones en BD:
        - Inserta en CancionesCarrito si es una canción
        - Inserta en AlbumesCarrito si es un álbum
        - Inserta en MerchCarrito (con unidades) si es merchandising
    
    Args:
        body (CartBody, optional): Objeto con el producto a añadir al carrito.
                                   Debe contener uno de: song_id, album_id, merch_id.
                                   Para merch puede incluir 'unidades' (default: 1).
    
    Returns:
        Tuple[Dict|Error, int]: Tupla con respuesta y código HTTP:
            - ({"message": "..."}, 200): Producto añadido exitosamente
            - (Error, 400): Petición inválida (no JSON, producto ya existe, etc.)
            - (Error, 401): Token no encontrado
            - (Error, 403): Usuario no autorizado
            - (Error, 500): Error interno del servidor
    
    Examples:
        Request JSON para añadir canción:
            {"songId": 42}
        
        Request JSON para añadir merch con cantidad:
            {"merchId": 10, "unidades": 3}
    
    Note:
        La transacción se realiza con rollback automático en caso de error.
    """
    print("[DEBUG] add_to_cart: Inicio de la función")
    db_conexion = None
    try:
        print(f"[DEBUG] add_to_cart: Verificando si la petición es JSON")
        if not connexion.request.is_json:
            print("[DEBUG] add_to_cart: ERROR - La petición no es JSON")
            return Error(code="400", message="El cuerpo de la petición no es JSON").to_dict(), 400
        
        print(f"[DEBUG] add_to_cart: Parseando body desde JSON")
        body = CartBody.from_dict(connexion.request.get_json())
        print(f"[DEBUG] add_to_cart: Body parseado - song_id={body.song_id}, album_id={body.album_id}, merch_id={body.merch_id}")

        # Obtener user_id del contexto (ya validado por check_oversound_auth)
        print("[DEBUG] add_to_cart: Obteniendo user_id del contexto")
        print(f"[DEBUG] add_to_cart: connexion.context completo = {connexion.context}")
        user_info = connexion.context.get('token_info')
        print(f"[DEBUG] add_to_cart: user_info del contexto = {user_info}")
        if user_info is None:
            print("[DEBUG] add_to_cart: ERROR CRÍTICO - user_info es None")
            return Error(code="401", message="No se pudo obtener información del usuario autenticado").to_dict(), 401
        user_id = user_info.get('userId') or user_info.get('id')
        print(f"[DEBUG] add_to_cart: user_id obtenido = {user_id}")

        print("[DEBUG] add_to_cart: Conectando a la base de datos")
        db_conexion = dbConectar()
        cursor = db_conexion.cursor()
        print("[DEBUG] add_to_cart: Conexión establecida")

        if body.song_id:
            print(f"[DEBUG] add_to_cart: Procesando canción con ID {body.song_id}")
            cursor.execute("SELECT 1 FROM CancionesCarrito WHERE idCancion = %s AND idUsuario = %s",
                           (body.song_id, user_id))
            if cursor.fetchone():
                print(f"[DEBUG] add_to_cart: ERROR - La canción {body.song_id} ya está en el carrito")
                return Error(code="400", message="La canción ya está en el carrito").to_dict(), 400
            print(f"[DEBUG] add_to_cart: Insertando canción en el carrito")
            cursor.execute("INSERT INTO CancionesCarrito (idCancion, idUsuario) VALUES (%s, %s)",
                           (body.song_id, user_id))
            print(f"[DEBUG] add_to_cart: Canción insertada correctamente")

        elif body.album_id:
            print(f"[DEBUG] add_to_cart: Procesando álbum con ID {body.album_id}")
            cursor.execute("SELECT 1 FROM AlbumesCarrito WHERE idAlbum = %s AND idUsuario = %s",
                           (body.album_id, user_id))
            if cursor.fetchone():
                print(f"[DEBUG] add_to_cart: ERROR - El álbum {body.album_id} ya está en el carrito")
                return Error(code="400", message="El álbum ya está en el carrito").to_dict(), 400
            print(f"[DEBUG] add_to_cart: Insertando álbum en el carrito")
            cursor.execute("INSERT INTO AlbumesCarrito (idAlbum, idUsuario) VALUES (%s, %s)",
                           (body.album_id, user_id))
            print(f"[DEBUG] add_to_cart: Álbum insertado correctamente")

        elif body.merch_id:
            print(f"[DEBUG] add_to_cart: Procesando merch con ID {body.merch_id}, unidades={body.unidades}")
            cursor.execute("SELECT 1 FROM MerchCarrito WHERE idMerch = %s AND idUsuario = %s",
                           (body.merch_id, user_id))
            if cursor.fetchone():
                print(f"[DEBUG] add_to_cart: ERROR - El merch {body.merch_id} ya está en el carrito")
                return Error(code="400", message="El artículo ya está en el carrito").to_dict(), 400
            print(f"[DEBUG] add_to_cart: Insertando merch en el carrito")
            cursor.execute("INSERT INTO MerchCarrito (idMerch, idUsuario, unidades) VALUES (%s, %s, %s)",
                           (body.merch_id, user_id, body.unidades))
            print(f"[DEBUG] add_to_cart: Merch insertado correctamente")

        else:
            print("[DEBUG] add_to_cart: ERROR - No se proporcionó songId, albumId ni merchId")
            return Error(code="400", message="Debes proporcionar songId, albumId o merchId").to_dict(), 400
        
        print("[DEBUG] add_to_cart: Haciendo commit de la transacción")
        db_conexion.commit()
        cursor.close()
        print("[DEBUG] add_to_cart: Producto añadido exitosamente")
        return {"message": "Producto añadido al carrito correctamente"}, 200

    except Exception as e:
        if db_conexion:
            db_conexion.rollback()
        print(f"[DEBUG] add_to_cart: EXCEPCIÓN - {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return Error(code="500", message=str(e)).to_dict(), 500

    finally:
        if db_conexion:
            dbDesconectar(db_conexion)


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
