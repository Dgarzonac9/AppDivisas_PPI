# AppDivisas_PPI

## Descripción
AppDivisas_PPI es una aplicación de cambio de divisas que te permite realizar conversiones y obtener tasas de cambio históricas. La aplicación utiliza Streamlit y se conecta a una API para obtener datos actualizados.

## App desplegada
La app desplegaa la puedes ver desde este link: https://divisas.streamlit.app/

## Funcionalidades
- **Cambio de Divisas en Tiempo Real:**
  - Selecciona la divisa base y la cantidad a convertir.
  - Visualiza las tasas de cambio en tiempo real.
  - Obtiene el resultado de la conversión.

- **Tasas de Cambio Históricas:**
  - Elige una fecha, la divisa base y las monedas objetivo.
  - Muestra un gráfico con las tasas de cambio históricas.
- **Rendimiento de cartera:**
  - La función calcular_rendimiento_cartera calcula  el rendimiento total de una cartera de activos dados sus precios diarios y las inversiones en cada activo.
  -Muestra un grafico de el rendimiento diario de los activos que componen la cartera.

- **Navegación Fácil:**
  - Barra lateral con botones para navegar entre las páginas "Inicio" y "Histórico".

## Instalación y Ejecución
1. Clona este repositorio: `git clone https://github.com/TuUsuario/AppDivisas_PPI.git`
2. Entra al directorio del proyecto: `cd AppDivisas_PPI`
3. Instala las dependencias: `pip install -r requirements.txt`
4. Ejecuta la aplicación: `streamlit run app.py`

## Dependencias
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)

## Contribución
Si quieres contribuir a este proyecto, ¡no dudes en abrir un problema o enviar un pull request!

## Licencia
ste proyecto está bajo la Licencia GNU General Public License