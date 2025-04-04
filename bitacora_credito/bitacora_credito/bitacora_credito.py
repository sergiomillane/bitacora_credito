import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text
import pytz 
from datetime import datetime 

# Definir la zona horaria de Culiacán, Sinaloa (UTC -7)
culiacan_tz = pytz.timezone("America/Mazatlan")  # Zona horaria correcta para Sinaloa

# Obtener la fecha y hora actual en la zona horaria especificada
fecha_actual = datetime.now(culiacan_tz).date()

# Usar la fecha con la zona horaria en Streamlit


# Configurar la conexión a SQL Server usando pymssql
DATABASE_URL = "mssql+pymssql://credito:Cr3d$.23xme@52.167.231.145:51433/CreditoyCobranza"

# Crear el engine de SQLAlchemy
engine = create_engine(DATABASE_URL)

def get_connection():
    """Obtiene la conexión a la base de datos."""
    try:
        conn = engine.connect()
        return conn
    except Exception as e:
        st.error(f"Error en la conexión con la base de datos: {e}")
        return None

# ========== INTERFAZ STREAMLIT ==========
st.title("Departamento de crédito - Bitácora de actividades")

# Sidebar para navegar entre secciones
st.sidebar.title("Menú")
pagina = st.sidebar.radio("Selecciona una opción", ["Bitácora de Actividades", "Indicadores"])

# ========== PÁGINA DE BITÁCORA ==========
if pagina == "Bitácora de Actividades":

    st.markdown("### ⚠️ **NO DAR ENTER O SE GUARDARÁ EL REGISTRO** ⚠️")
    st.markdown("Por favor, utilice el botón **'Guardar Registro'** para enviar el formulario.")

    # ========== FORMULARIO ==========
    with st.form("registro_form", clear_on_submit=True):  
        col1, col2, col3 = st.columns(3)

        with col1:
            fecha = st.date_input("Fecha", fecha_actual)
            ticket = st.text_input("Ticket")
            moto = st.selectbox("Moto", ["SI", "NO"])
            sucursal = st.selectbox("Sucursal", list(range(1, 101)))
            
        with col2:
            venta = st.selectbox("Venta", ["AUTORIZADA", "NO AUTORIZADA", "AUTORIZADA PARCIAL"])
            cliente = st.text_input("ID_Cliente")
            lc_actual = st.number_input("LC Actual", min_value=0.0, format="%.2f")
            lc_final = st.number_input("LC Final", min_value=0.0, format="%.2f")

        with col3:
            tipo_cliente = st.selectbox("Tipo de Cliente", ["RECOMPRA ACTIVO", "NUEVO", "RECOMPRA INACTIVO", "CAMPAÑA"])
            notas = st.selectbox("Notas", ["CON ENGANCHE", "SIN ENGANCHE", "OTRO"])
            enganche_requerido = st.number_input("Enganche Requerido", min_value=0.0, format="%.2f")
            enganche_recibido = st.number_input("Enganche Recibido", min_value=0.0, format="%.2f")

        especial = st.selectbox("Especial", ["Ninguno",
            "Aut. Fernando Valdez", "Aut. Francisco Valdez", "Aut. Gabriel Valdez", "Aut. Enrique Valdez",
            "Aut. Pedro Moreno", "Aut. Edmar Cruz",
            "Aut. Benjamin Rivera", "Aut. Jose Medina", "Aut. Ramon Casillas", "Aut. Area de crédito"
        ])

        # Crear una nueva fila para Artículo, Ejecutivo y Celular Cliente
        col4, col5, col6, col7 = st.columns(4)

        with col4:
            articulo = st.text_input("Artículo")

        with col5:
            ejecutivo = st.selectbox("Ejecutivo", ["Francis", "Alejandra", "Alma", "Francisco", "Mario", "Paul", "Victor", "Yadira", "Zulema", "Martin"])

        with col6:
            cel_cte = st.text_input("Celular Cliente")
        
        with col7:
            actualizacion = st.selectbox("Actualización cliente",["SI","NO"])

        # Fila aparte para Observación y Consulta Buró
        observacion = st.text_area("Observación")

        col8, col9 = st.columns(2)
        with col8:
            consulta_buro = st.selectbox("Consulta Buró", ["SI", "NO"])
        
        with col9:
            facturo = st.selectbox("Facturó", ["SIN DEFINIR","SI", "NO"])

    
    # ✅ IMPORTANTE: Botón de envío dentro del `st.form()`
        submit_button = st.form_submit_button("Guardar Registro")

    # ========== GUARDAR REGISTRO ==========
    if submit_button:
        conn = get_connection()
        if conn:
            try:
                query = text("""
                    INSERT INTO Bitacora_Credito (
                        FECHA, TICKET, SUC, CLIENTE, VENTA, MOTO, 
                        TIPO_DE_CLIENTE, NOTAS, LC_ACTUAL, LC_FINAL, 
                        ENGANCHE_REQUERIDO, ENGANCHE_RECIBIDO, OBSERVACION, ESPECIAL,
                        ARTICULO, EJECUTIVO, CEL_CTE, CONSULTA_BURO, Actualizacion, FACTURO
                    ) 
                    VALUES (:fecha, :ticket, :sucursal, :cliente, :venta, :moto, 
                            :tipo_cliente, :notas, :lc_actual, :lc_final, 
                            :enganche_requerido, :enganche_recibido, :observacion, :especial,
                            :articulo, :ejecutivo, :cel_cte, :consulta_buro, :actualizacion, :facturo)
                """)

                conn.execute(query, {
                    "fecha": fecha.strftime('%Y-%m-%d'),
                    "ticket": ticket,
                    "sucursal": sucursal,
                    "cliente": cliente,
                    "venta": venta,
                    "moto": moto,
                    "tipo_cliente": tipo_cliente,
                    "notas": notas,
                    "lc_actual": lc_actual,
                    "lc_final": lc_final,
                    "enganche_requerido": enganche_requerido,
                    "enganche_recibido": enganche_recibido,
                    "observacion": observacion,
                    "especial": especial,
                    "articulo": articulo,
                    "ejecutivo": ejecutivo,
                    "cel_cte": cel_cte,
                    "consulta_buro": consulta_buro,
                    "actualizacion":actualizacion,
                    "facturo": facturo 
                })
                conn.commit()
                st.success("Registro guardado exitosamente en la base de datos.")
            except Exception as e:
                st.error(f"Error al guardar el registro: {e}")
            finally:
                conn.close()

    # ========== VISUALIZADOR EN TIEMPO REAL ==========
    st.header("📊 Registros en tiempo real")

    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        filtro_cliente = st.text_input("Filtrar por ID Cliente", "")

    with col2:
        filtro_rango = st.selectbox("Rango de fechas", ["Día específico", "Histórico", "Año completo", "Mes específico"], index=0)

    with col3:
        filtro_ejecutivo = st.selectbox("Filtrar por Ejecutivo", ["Todos"] + ["Alejandra", "Alma", "Francisco", "Mario", "Paul", "Victor", "Yadira", "Zulema", "Martin"])

    # Selección de fechas según el rango
    fecha_inicio, fecha_fin = None, None

    if filtro_rango == "Día específico":
        fecha = st.date_input("Selecciona el día", value=fecha_actual)
        fecha_inicio = fecha_fin = fecha

    elif filtro_rango == "Mes específico":
        anio = st.selectbox("Selecciona el año", list(range(2022, fecha_actual.year + 1)), index=(fecha_actual.year - 2022))
        mes = st.selectbox("Selecciona el mes", list(range(1, 13)), index=(fecha_actual.month - 1))
        fecha_inicio = datetime(anio, mes, 1).date()
        if mes == 12:
            fecha_fin = datetime(anio + 1, 1, 1).date() - pd.Timedelta(days=1)
        else:
            fecha_fin = datetime(anio, mes + 1, 1).date() - pd.Timedelta(days=1)

    elif filtro_rango == "Año completo":
        anio = st.selectbox("Selecciona el año", list(range(2022, fecha_actual.year + 1)), index=(fecha_actual.year - 2022))
        fecha_inicio = datetime(anio, 1, 1).date()
        fecha_fin = datetime(anio, 12, 31).date()

    elif filtro_rango == "Histórico":
        fecha_inicio = datetime(2022, 1, 1).date()
        fecha_fin = fecha_actual

    # Función para obtener registros desde SQL Server
    def fetch_records():
        conn = get_connection()
        if conn:
            try:
                query = text("""
                    SELECT Registro AS '#Registro', * 
                    FROM Bitacora_Credito 
                    WHERE FECHA BETWEEN :inicio AND :fin
                    {filtro_ejecutivo_sql}
                    ORDER BY Registro ASC
                """.format(
                    filtro_ejecutivo_sql="AND EJECUTIVO = :ejecutivo" if filtro_ejecutivo != "Todos" else ""
                ))

                params = {
                    "inicio": fecha_inicio.strftime('%Y-%m-%d'),
                    "fin": fecha_fin.strftime('%Y-%m-%d')
                }
                if filtro_ejecutivo != "Todos":
                    params["ejecutivo"] = filtro_ejecutivo

                df = pd.read_sql(query, conn, params=params)
                conn.close()
                return df
            except Exception as e:
                st.error(f"Error al obtener los registros: {e}")
                return pd.DataFrame()
        return pd.DataFrame()

    # Mostrar registros en tiempo real
    df_records = fetch_records()

    if not df_records.empty:
        st.dataframe(df_records)
    else:
        st.warning("No hay registros para mostrar con los filtros seleccionados.")

    # ========== EDITAR Y ELIMINAR REGISTRO LADO A LADO ==========
    col_editar, col_eliminar = st.columns(2)

    with col_editar:
        st.subheader("✏️ Editar un registro")
        if not df_records.empty:
            registros_disponibles = df_records["#Registro"].tolist()
            registro_editar = st.selectbox("Registro a editar:", registros_disponibles, key="editar")

            columnas_editables = ["TICKET", "CLIENTE", "FECHA", "SUC", "VENTA", "MOTO", "LC_ACTUAL", "LC_FINAL",
                                "ENGANCHE_REQUERIDO", "ENGANCHE_RECIBIDO", "OBSERVACION", "ESPECIAL", "ARTICULO",
                                "EJECUTIVO", "CEL_CTE", "CONSULTA_BURO", "Actualizacion", "FACTURO"]

            campo_seleccionado = st.selectbox("Campo a editar:", columnas_editables)
            nuevo_valor = st.text_input(f"Nuevo valor para {campo_seleccionado}:")

            if st.button("Actualizar Registro"):
                conn = get_connection()
                if conn:
                    try:
                        update_query = text(f"""
                            UPDATE Bitacora_Credito
                            SET {campo_seleccionado} = :nuevo_valor
                            WHERE Registro = :registro
                        """)
                        conn.execute(update_query, {"nuevo_valor": nuevo_valor, "registro": registro_editar})
                        conn.commit()
                        st.success(f"Registro #{registro_editar} actualizado exitosamente.")
                    except Exception as e:
                        st.error(f"Error al actualizar el registro: {e}")
                    finally:
                        conn.close()
                    st.rerun()

    with col_eliminar:
        st.subheader("❌ Eliminar un registro")
        if not df_records.empty:
            registros_disponibles = df_records["#Registro"].tolist()
            registro_eliminar = st.selectbox("Registro a eliminar:", registros_disponibles, key="eliminar")

            if st.button("Eliminar Registro"):
                conn = get_connection()
                if conn:
                    try:
                        delete_query = text("DELETE FROM Bitacora_Credito WHERE Registro = :registro")
                        conn.execute(delete_query, {"registro": registro_eliminar})
                        conn.commit()
                        st.success(f"Registro #{registro_eliminar} eliminado exitosamente.")
                    except Exception as e:
                        st.error(f"Error al eliminar el registro: {e}")
                    finally:
                        conn.close()
                st.rerun()


elif pagina == "Indicadores":
    st.header("📊 Indicadores de Conversión")

    from dateutil.relativedelta import relativedelta

    # Calcular el primer y último día del mes actual
    hoy = datetime.now()
    primer_dia_mes = hoy.replace(day=1).date()
    ultimo_dia_mes = (primer_dia_mes + relativedelta(months=1)) - pd.Timedelta(days=1)

    conn = get_connection()
    if conn:
        try:
            # Bitácora
            query_bitacora = text("""
                SELECT CLIENTE, FECHA, SUC, VENTA, LC_ACTUAL, LC_FINAL, NOTAS, OBSERVACION, EJECUTIVO
                FROM Bitacora_Credito
                WHERE CLIENTE IS NOT NULL
            """)
            bitacora = pd.read_sql(query_bitacora, conn)

            # RPVENTA
            query_rpventa = text("""
                SELECT CLIENTE, FECHA AS FECHA_VENTA, FOLIO_POS, TOTALFACTURA
                FROM RPVENTA
                WHERE CLIENTE IS NOT NULL
            """)
            ventas = pd.read_sql(query_rpventa, conn)

            # Recompra del mes (por FECHA)
            query_recompra = text("""
                SELECT DISTINCT FOLIO_POS
                FROM SeguimientoActivacion
                WHERE Segmento = 'Recompra'
                  AND FECHA BETWEEN :inicio AND :fin
            """)
            df_recompra = pd.read_sql(query_recompra, conn, params={"inicio": primer_dia_mes, "fin": ultimo_dia_mes})

            # Clientes únicos en Bitácora en el mes
            query_bitacora_mes = text("""
                SELECT COUNT(DISTINCT CLIENTE) as conteo
                FROM Bitacora_Credito
                WHERE FECHA BETWEEN :inicio AND :fin
            """)
            clientes_registrados_mes = pd.read_sql(query_bitacora_mes, conn, params={"inicio": primer_dia_mes, "fin": ultimo_dia_mes})["conteo"][0]

            conn.close()
        except Exception as e:
            st.error(f"Error al obtener los datos: {e}")
            bitacora = pd.DataFrame()
            ventas = pd.DataFrame()
            df_recompra = pd.DataFrame()
            clientes_registrados_mes = 0

    if not bitacora.empty and not ventas.empty:
        bitacora["FECHA"] = pd.to_datetime(bitacora["FECHA"])
        ventas["FECHA_VENTA"] = pd.to_datetime(ventas["FECHA_VENTA"])
        bitacora["CLIENTE"] = bitacora["CLIENTE"].astype(str).str.strip()
        ventas["CLIENTE"] = ventas["CLIENTE"].astype(str).str.strip()

        merged = pd.merge(bitacora, ventas, on="CLIENTE", how="left")
        merged["DIAS_PARA_COMPRA"] = (merged["FECHA_VENTA"] - merged["FECHA"]).dt.days
        compras_validas = merged[merged["DIAS_PARA_COMPRA"] >= 0].copy()

        resumen = (
            compras_validas
            .groupby(["CLIENTE", "FOLIO_POS", "FECHA_VENTA"], as_index=False)
            .agg({
                "TOTALFACTURA": "sum",
                "DIAS_PARA_COMPRA": "min",
                "FOLIO_POS": "count"
            })
            .rename(columns={
                "TOTALFACTURA": "TOTAL_COMPRA",
                "FOLIO_POS": "#Productos",
                "FECHA_VENTA": "Fecha de Compra"
            })
        )

        total_clientes = bitacora["CLIENTE"].nunique()
        clientes_con_compra = compras_validas["CLIENTE"].nunique()
        clientes_sin_compra = total_clientes - clientes_con_compra
        total_recompra = df_recompra["FOLIO_POS"].nunique()
        porcentaje_bitacora_recompra = round((clientes_registrados_mes / total_recompra) * 100, 2) if total_recompra > 0 else 0

        # Layout
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown(f"""
                <div style="border: 2px solid #ff4b4b; border-radius: 10px; padding: 15px; background-color: #fff3f3;">
                    <h4 style="margin: 0; color: #ff4b4b;">📌 % Clientes recompra procesados</h4>
                    <p style="font-size: 28px; font-weight: bold; margin: 0; color: #000;">{porcentaje_bitacora_recompra}%</p>
                </div>
            """, unsafe_allow_html=True)

            st.metric("📋 Total Facturas Recompra", total_recompra)
            st.metric("📎 Clientes registrados", total_clientes)
            st.metric("✅ Clientes con compra", clientes_con_compra)
            st.metric("❌ Clientes sin compra", clientes_sin_compra)

        with col2:
            st.subheader("Distribución por ejecutivo (clientes sin compra)")

            clientes_con_compra_set = set(compras_validas["CLIENTE"].unique())
            sin_compra_df = bitacora[~bitacora["CLIENTE"].isin(clientes_con_compra_set)].copy()

            resumen_ejecutivo = (
                sin_compra_df.groupby("EJECUTIVO")["CLIENTE"]
                .nunique()
                .reset_index()
                .rename(columns={"CLIENTE": "Clientes sin compra"})
            )

            total_sin_compra = resumen_ejecutivo["Clientes sin compra"].sum()
            resumen_ejecutivo["% del total"] = (
                resumen_ejecutivo["Clientes sin compra"] / total_sin_compra * 100
            ).round(2)

            resumen_ejecutivo = resumen_ejecutivo.sort_values(by="% del total", ascending=False)

            # Formatear el estilo con colores condicionales
            styled_df = resumen_ejecutivo.style.format({
                "% del total": "{:.2f}"
            }).background_gradient(
                subset=["% del total"], cmap="RdYlGn_r"
            )

            st.dataframe(styled_df, use_container_width=True)


        # Tabla de clientes sin compra con filtros
        st.subheader("📋 Clientes sin compra")

        # Filtros en una misma fila
        col1, col2, col3 = st.columns(3)

        with col1:
            filtro_rango = st.selectbox("Rango de fechas", ["Día específico", "Mes específico", "Año completo", "Histórico"])

        with col2:
            filtro_ejecutivo = st.selectbox("Ejecutivo", ["Todos"] + sorted(sin_compra_df["EJECUTIVO"].dropna().unique()))

        # Determinar valores predeterminados
        anio_default = fecha_actual.year
        mes_default = fecha_actual.month
        fecha_inicio, fecha_fin = None, None

        with col3:
            if filtro_rango == "Día específico":
                fecha = st.date_input("Día", value=fecha_actual, key="fecha_dia")
                fecha_inicio = fecha_fin = fecha
            elif filtro_rango == "Mes específico":
                anio = st.selectbox("Año", list(range(2022, anio_default + 1)), index=(anio_default - 2022), key="anio_mes")
                mes = st.selectbox("Mes", list(range(1, 13)), index=(mes_default - 1), key="mes_mes")
                fecha_inicio = datetime(anio, mes, 1).date()
                fecha_fin = (datetime(anio + 1, 1, 1).date() - pd.Timedelta(days=1)) if mes == 12 else (datetime(anio, mes + 1, 1).date() - pd.Timedelta(days=1))
            elif filtro_rango == "Año completo":
                anio = st.selectbox("Año", list(range(2022, anio_default + 1)), index=(anio_default - 2022), key="anio_anual")
                fecha_inicio = datetime(anio, 1, 1).date()
                fecha_fin = datetime(anio, 12, 31).date()
            elif filtro_rango == "Histórico":
                fecha_inicio = datetime(2022, 1, 1).date()
                fecha_fin = fecha_actual

        # Aplicar filtros al DataFrame
        filtro_df = sin_compra_df.copy()
        filtro_df = filtro_df[(filtro_df["FECHA"] >= pd.to_datetime(fecha_inicio)) & (filtro_df["FECHA"] <= pd.to_datetime(fecha_fin))]

        if filtro_ejecutivo != "Todos":
            filtro_df = filtro_df[filtro_df["EJECUTIVO"] == filtro_ejecutivo]

        # Mostrar tabla con formato de fecha
        columnas_mostrar = ["FECHA", "CLIENTE", "EJECUTIVO", "SUC", "VENTA", "LC_ACTUAL", "LC_FINAL", "NOTAS", "OBSERVACION"]
        df_display = filtro_df[columnas_mostrar].copy()
        df_display["FECHA"] = df_display["FECHA"].dt.strftime("%Y-%m-%d")

        st.dataframe(df_display.reset_index(drop=True))




    else:
        st.warning("No se pudo cargar la información de Bitácora o RPVENTA.")

