import requests
# API key proporcionada
API_KEY = "T036e078875144954d119fab60c46078f"

# Función para obtener las tasas de cambio de la API
def obtener_tasas(base):
    endpoint = f"https://open.er-api.com/v6/latest/{base}?apikey={API_KEY}"
    response = requests.get(endpoint)
    if response.status_code == 200:
        data = response.json()
        return data['rates']
    else:
        return None


ACCESS_KEY2 = "85431cd6569b54a072508a2fd778828a"

def obtener_datos_historicos(fecha, moneda_base, monedas_objetivo):
    endpoint = f"http://api.currencylayer.com/historical?access_key={ACCESS_KEY2}&date={fecha}&source={moneda_base}&currencies={','.join(monedas_objetivo)}&format=1"
    response = requests.get(endpoint)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None