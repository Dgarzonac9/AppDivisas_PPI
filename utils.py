import requests

# Clave de API proporcionada para el servicio de tasas de cambio
API_KEY = "T036e078875144954d119fab60c46078f"

# Función para obtener las tasas de cambio de la API externa
def obtener_tasas(base):
    """
    Obtiene las tasas de cambio para una moneda base dada.

    Args:
        base (str): La moneda base para la cual se obtendrán las tasas.
    
    Returns:
        dict or None: Un diccionario de tasas de cambio si la solicitudes
        exitosa, None en caso contrario.
    """
    endpoint = f"https://open.er-api.com/v6/latest/{base}?apikey={API_KEY}"
    response = requests.get(endpoint)

    if response.status_code == 200:
        data = response.json()
        return data['rates']
    else:
        return None

# Clave de acceso para el servicio de datos históricos
ACCESS_KEY2 = "85431cd6569b54a072508a2fd778828a"

def obtener_datos_historicos(fecha, moneda_base, monedas_objetivo):
    """
    Obtiene datos históricos de tasas de cambio para una fecha dada.

    Args:
        fecha (str): La fecha en formato YYYY-MM-DD para la cual se desean
        los datos históricos.
        moneda_base (str): La moneda base para la cual se obtendrán los datos
        históricos.
        monedas_objetivo (list): Lista de monedas objetivo para las cuales se
        obtendrán los datos históricos.

    Returns:
        dict or None: Un diccionario de datos históricos si la solicitud es
        exitosa, None en caso contrario.   
    """
    endpoint = (
        f"http://api.currencylayer.com/historical?"
        f"access_key={ACCESS_KEY2}&date={fecha}&source={moneda_base}"
        f"&currencies={','.join(monedas_objetivo)}&format=1"
    )
    response = requests.get(endpoint)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None
