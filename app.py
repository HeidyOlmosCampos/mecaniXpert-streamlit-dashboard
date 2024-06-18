import streamlit as st
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px  # pip install plotly-express



BASE_URL = 'http://127.0.0.1:8000'

# Clase para gestionar el estado de sesión
class SessionState:
    def __init__(self):
        self.user = None
        self.empresa_id = None
        self.selected_option = "Inicio"  # Opción por defecto

# Función para enviar la solicitud de login al servidor backend
def login_with_credentials(username, password):
    url = f'{BASE_URL}/auth/login'  # URL de tu servidor FastAPI
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'accept': 'application/json'
    }
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(url, headers=headers, data=data)
    return response

# Función para obtener los clientes de la API
def obtener_clientes(id_empresa):
    url = f'{BASE_URL}/clientes/porEmpresaText/{id_empresa}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('clientes', [])
    else:
        st.error(f'Error al obtener clientes. Código de estado: {response.status_code}')
        return []
    
# Función para obtener los empleados de la API
def obtener_empleados(id_empresa):
    url = f'{BASE_URL}/empleados/porEmpresaText/{id_empresa}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('empleados', [])
    else:
        st.error(f'Error al obtener empleados. Código de estado: {response.status_code}')
        return []
    
# Función para obtener los servicios de la API
def obtener_servicios(id_empresa):
    url = f'{BASE_URL}/servicios/porEmpresaText/{id_empresa}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('servicios', [])
    else:
        st.error(f'Error al obtener servicios. Código de estado: {response.status_code}')
        return []
    
# Función para obtener los clientes de la API
def obtener_ordenes(id_empresa):
    url = f'{BASE_URL}/ordenes/porEmpresaText/{id_empresa}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('ordenes', [])
    else:
        st.error(f'Error al obtener ordenes. Código de estado: {response.status_code}')
        return []    
    
def obtener_kpi_ordenes_trabajo(inicio, fin, id_empresa):
    url = f'{BASE_URL}/kpis/ordenes-trabajo?inicio={inicio}&fin={fin}&empresa={id_empresa}'
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None
    
def obtener_kpi_tasa_retencion_clientes(inicio, fin, id_empresa):
    url = f'{BASE_URL}/kpis/tasa-retencion-clientes?inicio={inicio}&fin={fin}&empresa={id_empresa}'
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def obtener_kpi_top_empleados_ordenes_trabajo(inicio, fin, id_empresa):
    url = f'{BASE_URL}/kpis/top-empleados-ordenes-trabajo?inicio={inicio}&fin={fin}&empresa={id_empresa}'
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def obtener_kpi_top_servicios_vendidos_finalizados(inicio, fin, id_empresa):
    url = f'{BASE_URL}/kpis/top-servicios-vendidos-finalizados?inicio={inicio}&fin={fin}&empresa={id_empresa}'
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None    
    
    
    

# Función para manejar el contenido principal según la opción seleccionada
def main_content(session_state):
    
    if session_state.selected_option == "Inicio":
        fecha_inicio_str = '01/01/2024'
        fecha_fin_str = '31/12/2024'

        kpi_data_1 = obtener_kpi_ordenes_trabajo(fecha_inicio_str, fecha_fin_str, session_state.empresa_id)
        kpi_data_2 = obtener_kpi_tasa_retencion_clientes(fecha_inicio_str, fecha_fin_str, session_state.empresa_id)
        kpi_data_3 = obtener_kpi_top_empleados_ordenes_trabajo(fecha_inicio_str, fecha_fin_str, session_state.empresa_id)
        kpi_data_4 = obtener_kpi_top_servicios_vendidos_finalizados(fecha_inicio_str, fecha_fin_str, session_state.empresa_id)
        
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            fecha_inicio = st.date_input('Fecha de inicio', value=datetime(2024, 1, 1))
        with col2:
            fecha_fin = st.date_input('Fecha de fin', value=datetime(2024, 12, 31))            
        with col3:
            st.write('   ')
            st.write('   ')
            if st.button('Actualizar'):
                fecha_inicio_str = fecha_inicio.strftime('%d/%m/%Y')
                fecha_fin_str = fecha_fin.strftime('%d/%m/%Y')
                kpi_data_1 = obtener_kpi_ordenes_trabajo(fecha_inicio_str, fecha_fin_str, session_state.empresa_id)
                kpi_data_2 = obtener_kpi_tasa_retencion_clientes(fecha_inicio_str, fecha_fin_str, session_state.empresa_id)
                kpi_data_3 = obtener_kpi_top_empleados_ordenes_trabajo(fecha_inicio_str, fecha_fin_str, session_state.empresa_id)
                kpi_data_4 = obtener_kpi_top_servicios_vendidos_finalizados(fecha_inicio_str, fecha_fin_str, session_state.empresa_id)
        with col4:
            st.subheader("Ordenes finalizadas:")
            st.subheader(f"{kpi_data_1['total_ordenes_trabajo']}")
            

        # Crear un DataFrame de pandas con los datos
        if(kpi_data_2):
            df_compras = pd.DataFrame(kpi_data_2.values(), index=kpi_data_2.keys())
            fig_kpi1 = px.pie(
                df_compras,
                values='porcentaje',
                names='rango',
                title='<b>Frecuencia de Compras de Servicios por Clientes</b>',
                labels={'rango': 'Rango de Compras', 'porcentaje': 'Porcentaje'},
                hole=0.4,  # Tamaño del agujero en el centro (opcional)
                color_discrete_sequence=px.colors.qualitative.Set3  # Colores del gráfico (opcional)
            )
            fig_kpi1.update_traces(textinfo='percent+label', pull=[0.1, 0.1, 0.1, 0.1], marker=dict(line=dict(color='#000000', width=2)))
                    
        if(kpi_data_3):
            df_empleados = pd.DataFrame(kpi_data_3["top_6_empleados"])
            df_empleados = df_empleados.sort_values(by="ordenes", ascending=True)
            fig_kpi2 = px.bar(
                df_empleados,
                x="ordenes",
                y="nombre",
                orientation="h",
                title="<b>Top 6 Empleados por Ordenes</b>",
                labels={"ordenes": "Órdenes", "nombre": "Nombre del Empleado"},
                color="ordenes",  # Opcional: Colorear por número de órdenes
                color_continuous_scale=px.colors.sequential.Blues,  # Opcional: Escala de colores
            )
            fig_kpi2.update_layout(
                plot_bgcolor="rgba(0, 0, 0, 0)",  # Fondo transparente
                xaxis=dict(showgrid=False),  # Sin líneas de la cuadrícula en el eje x
                yaxis=dict(showgrid=False),  # Sin líneas de la cuadrícula en el eje y
                title_font_size=17,  # Tamaño de fuente del título
            )
        
        if(kpi_data_2 and kpi_data_3):
            left_column, right_column = st.columns(2)
            left_column.plotly_chart(fig_kpi1, use_container_width=True)
            right_column.plotly_chart(fig_kpi2, use_container_width=True)
        
        if(kpi_data_4):
            df_servicios = pd.DataFrame(kpi_data_4["top_6_servicios"])
            df_servicios = df_servicios.sort_values(by="ventas", ascending=True)
            fig_kpi3 = px.bar(
                df_servicios,
                x="servicio",
                y="ventas",
                title="<b>Top 6 Servicios por Ventas</b>",
                labels={"ventas": "Ventas", "servicio": "Servicio"},
                color="ventas",  # Opcional: Colorear por número de ventas
                color_continuous_scale=px.colors.sequential.Blues,  # Opcional: Escala de colores
            )
            fig_kpi3.update_layout(
                plot_bgcolor="rgba(0, 0, 0, 0)",  # Fondo transparente
                xaxis=dict(showgrid=False),  # Sin líneas de la cuadrícula en el eje x
                yaxis=dict(showgrid=False),  # Sin líneas de la cuadrícula en el eje y
                title_font_size=17,  # Tamaño de fuente del título
            )
            st.plotly_chart(fig_kpi3)
                
        
        
    elif session_state.selected_option == "Clientes":
        listaObjetos = obtener_clientes(session_state.empresa_id)
        st.write("Listado de clientes: " + str(len(listaObjetos)) + " Registros")
        search_term = st.text_input("Buscar cliente por nombre:")
        if search_term:
            listaObjetos = [unObjeto for unObjeto in listaObjetos if search_term.lower() in unObjeto['nombre'].lower()]
        # Paginación y mostrar tabla
        page_size = st.slider("Número de filas por página", min_value=1, max_value=100, value=10)
        paginated = listaObjetos[:page_size]
        st.table(paginated)

    elif session_state.selected_option == "Personal":
        listaObjetos = obtener_empleados(session_state.empresa_id)
        st.write("Listado de personal: " + str(len(listaObjetos)) + " Registros")
        search_term = st.text_input("Buscar personal por nombre:")
        if search_term:
            listaObjetos = [unObjeto for unObjeto in listaObjetos if search_term.lower() in unObjeto['nombre'].lower()]
        # Paginación y mostrar tabla
        page_size = st.slider("Número de filas por página", min_value=1, max_value=100, value=10)
        paginated = listaObjetos[:page_size]
        st.table(paginated)

        
    elif session_state.selected_option == "Servicios":
        listaObjetos = obtener_servicios(session_state.empresa_id)
        st.write("Listado de personal: " + str(len(listaObjetos)) + " Registros")
        search_term = st.text_input("Buscar servicio por nombre:")
        if search_term:
            listaObjetos = [unObjeto for unObjeto in listaObjetos if search_term.lower() in unObjeto['nombre'].lower()]
        # Paginación y mostrar tabla
        page_size = st.slider("Número de filas por página", min_value=1, max_value=100, value=10)
        paginated = listaObjetos[:page_size]
        st.table(paginated)
        
    elif session_state.selected_option == "Ordenes de Trabajo":
        listaObjetos = obtener_ordenes(session_state.empresa_id)
        st.write("Listado de ordenes de trabajo: " + str(len(listaObjetos)) + " Registros")
        search_term = st.text_input("Buscar orden por empleado:")
        if search_term:
            listaObjetos = [unObjeto for unObjeto in listaObjetos if search_term.lower() in unObjeto['empleado'].lower()]
        search_term_dos = st.text_input("Buscar orden por servicio:")
        if search_term_dos:
            listaObjetos = [unObjeto for unObjeto in listaObjetos if search_term_dos.lower() in unObjeto['servicio'].lower()]
        # Paginación y mostrar tabla
        page_size = st.slider("Número de filas por página", min_value=1, max_value=100, value=10)
        paginated = listaObjetos[:page_size]
        st.table(paginated)
        
        
    elif session_state.selected_option == "Cerrar sesión":
        st.warning("Has cerrado sesión exitosamente")
        session_state.user = None
        session_state.empresa_id = None
        session_state.selected_option = "Inicio"  # Restablecer la opción seleccionada

        # Redirigir a la página de inicio de sesión
        st.experimental_set_query_params()
        st.experimental_rerun()

# Interfaz de usuario con Streamlit
def main():

    
    # Inicializar el estado de sesión
    if 'session_state' not in st.session_state:
        st.session_state.session_state = SessionState()

    session_state = st.session_state.session_state

    # Mostrar formulario de inicio de sesión si no hay usuario autenticado
    if not session_state.user:
        st.title('MecaniXpert')
        
        # Campos de entrada para nombre de usuario y contraseña
        username = st.text_input('Correo')
        password = st.text_input('Contraseña', type='password')

        # Botón para enviar las credenciales
        if st.button('Iniciar sesión'):
            if username and password:
                # Enviar credenciales al servidor
                response = login_with_credentials(username, password)

                if response.status_code == 200:
                    st.success('Inicio de sesión exitoso!')
                    data = response.json()
                    correo = data.get('correo')
                    empresa_id = data.get('empresaId')

                    # Guardar en sesión
                    session_state.user = correo
                    session_state.empresa_id = empresa_id

                    # Redirigir a la página del sidebar después del inicio de sesión
                    st.experimental_set_query_params()
                    st.experimental_rerun()
                else:
                    st.error('Error: Correo o contraseña incorrectos')
            else:
                st.warning('Por favor ingresa nombre de usuario y contraseña')
    else:
        st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

        # Mostrar sidebar y contenido principal si hay usuario autenticado
        st.sidebar.title('MecaniXpert')
        st.sidebar.subheader(session_state.user)
        options = ["Inicio", "Clientes", "Personal", "Servicios", "Ordenes de Trabajo", "Cerrar sesión"]
        choice = st.sidebar.radio('Seleccione una opción', options)

        # Actualizar la opción seleccionada en SessionState
        session_state.selected_option = choice
        
        # Mostrar el contenido principal
        main_content(session_state)
        
    # ---- HIDE STREAMLIT STYLE ----
    hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True)        

if __name__ == '__main__':
    main()
