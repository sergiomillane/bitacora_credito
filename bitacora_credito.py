import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text
import pytz 
from datetime import datetime 
import pymssql

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
pagina = st.sidebar.radio("Selecciona una opción", ["Bitácora de Actividades", "Indicadores","Mensajes Sms"])

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
            sucursal = st.selectbox("Sucursal", list(range(1, 102)))
            
        with col2:
            venta = st.selectbox("Venta", ["AUTORIZADA", "NO AUTORIZADA", "AUTORIZADA PARCIAL","VISITA DOMICILIARIA","ACTUALIZACION"])
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

        col8, col9,col10 = st.columns(3)
        with col8:
            consulta_buro = st.selectbox("Consulta Buró", ["SI", "NO"])
        
        with col9:
            facturo = st.selectbox("Facturó", ["SIN DEFINIR","SI", "NO"])

        with col10:
            innecesario = st.selectbox("Solicitud innecesaria",["SI","NO"])

    
    # ✅ IMPORTANTE: Botón de envío dentro del `st.form()`
        submit_button = st.form_submit_button("Guardar Registro")

    # ========== GUARDAR REGISTRO ==========
    if submit_button:
        ejecutivos_validos = ["Francis", "Alejandra", "Alma", "Francisco", "Mario", "Paul", "Victor", "Yadira", "Zulema", "Martin"]

        if ejecutivo not in ejecutivos_validos:
            st.error("⚠️ El ejecutivo seleccionado no es válido. Por favor selecciona uno de la lista.")
        else:
            conn = get_connection()
            if conn:
                try:
                    query = text("""
                        INSERT INTO Bitacora_Credito (
                            FECHA, TICKET, SUC, CLIENTE, VENTA, MOTO, 
                            TIPO_DE_CLIENTE, NOTAS, LC_ACTUAL, LC_FINAL, 
                            ENGANCHE_REQUERIDO, ENGANCHE_RECIBIDO, OBSERVACION, ESPECIAL,
                            ARTICULO, EJECUTIVO, CEL_CTE, CONSULTA_BURO, Actualizacion, FACTURO,innecesario
                        ) 
                        VALUES (:fecha, :ticket, :sucursal, :cliente, :venta, :moto, 
                                :tipo_cliente, :notas, :lc_actual, :lc_final, 
                                :enganche_requerido, :enganche_recibido, :observacion, :especial,
                                :articulo, :ejecutivo, :cel_cte, :consulta_buro, :actualizacion, :facturo, :innecesario)
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
                        "actualizacion": actualizacion,
                        "facturo": facturo,
                        "innecesario": innecesario
                    })
                    conn.commit()
                    st.success("✅ Registro guardado exitosamente en la base de datos.")
                except Exception as e:
                    st.error(f"❌ Error al guardar el registro: {e}")
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
        filtro_ejecutivo = st.selectbox("Filtrar por Ejecutivo", ["Todos"] + ["Alejandra", "Alma", "Francisco", "Mario", "Paul", "Victor", "Yadira", "Zulema", "Martin","Francis"])

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

    # Controles para seleccionar mes y año
    col_mes, col_anio = st.columns(2)
    
    with col_mes:
        # Lista de meses
        meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        mes_seleccionado = st.selectbox("Seleccionar mes:", meses, index=datetime.now().month - 1)
        mes_numero = meses.index(mes_seleccionado) + 1
    
    with col_anio:
        anio_actual = datetime.now().year
        anio_seleccionado = st.selectbox("Seleccionar año:", list(range(2025, anio_actual + 1)), index=anio_actual - 2025)

    # Calcular el primer y último día del mes seleccionado
    primer_dia_mes = datetime(anio_seleccionado, mes_numero, 1).date()
    ultimo_dia_mes = (primer_dia_mes + relativedelta(months=1)) - pd.Timedelta(days=1)

    # Ajustar el inicio si es marzo 2025
    if primer_dia_mes.year == 2025 and primer_dia_mes.month == 3:
        primer_dia_mes = datetime(2025, 3, 19).date()
    
    # Mostrar el período seleccionado
    st.info(f"📅 Mostrando indicadores para: **{mes_seleccionado} {anio_seleccionado}** ({primer_dia_mes} al {ultimo_dia_mes})")
    
    # Debug temporal - mostrar las fechas exactas que se usan en la consulta
    st.write(f"🔍 **Debug**: Consultando desde {primer_dia_mes} hasta {ultimo_dia_mes}")


    conn = get_connection()
    if conn:
        try:
            # Obtener todos los datos de Bitácora para el mes seleccionado
            query_bitacora_mes = text("""
                SELECT CLIENTE, FECHA, SUC, VENTA, LC_ACTUAL, LC_FINAL, NOTAS, OBSERVACION, 
                       EJECUTIVO, Actualizacion, innecesario, TIPO_DE_CLIENTE, ENGANCHE_REQUERIDO, 
                       ENGANCHE_RECIBIDO, CONSULTA_BURO, FACTURO
                FROM Bitacora_Credito
                WHERE FECHA BETWEEN :inicio AND :fin
                  AND CLIENTE IS NOT NULL
            """)
            bitacora = pd.read_sql(query_bitacora_mes, conn, params={"inicio": primer_dia_mes, "fin": ultimo_dia_mes})
            
            # Debug temporal - mostrar cuántos registros se obtuvieron
            st.write(f"🔍 **Debug**: Se encontraron {len(bitacora)} registros en la consulta")

            # RPVENTA para verificar compras posteriores a la fecha de registro
            query_rpventa = text("""
                SELECT CLIENTE, FECHA AS FECHA_VENTA, FOLIO_POS, TOTALFACTURA
                FROM RPVENTA
                WHERE CLIENTE IS NOT NULL
                  AND FECHA >= :inicio_mes
            """)
            ventas = pd.read_sql(query_rpventa, conn, params={"inicio_mes": primer_dia_mes})

            # Recompra del mes seleccionado (por FECHA) - Solo si existe la tabla
            try:
                query_recompra = text("""
                    SELECT DISTINCT FOLIO_POS
                    FROM SeguimientoActivacion
                    WHERE Segmento = 'Recompra'
                      AND FECHA BETWEEN :inicio AND :fin
                """)
                df_recompra = pd.read_sql(query_recompra, conn, params={"inicio": primer_dia_mes, "fin": ultimo_dia_mes})
            except:
                # Si no existe la tabla, usar datos de bitácora para simular
                df_recompra = pd.DataFrame({'FOLIO_POS': []})

            # Prueba_Cliente para clasificación - Solo si existe
            try:
                query_valor_cte = text("""
                    SELECT ID_CLIENTE, VALOR_CTE
                    FROM Prueba_Cliente
                """)
                valor_cte_df = pd.read_sql(query_valor_cte, conn)
            except:
                # Si no existe la tabla, crear DataFrame vacío
                valor_cte_df = pd.DataFrame({'ID_CLIENTE': [], 'VALOR_CTE': []})

            conn.close()
        except Exception as e:
            st.error(f"Error al obtener los datos: {e}")
            bitacora = pd.DataFrame()
            ventas = pd.DataFrame()
            df_recompra = pd.DataFrame()
            valor_cte_df = pd.DataFrame()

    # Inicializar DataFrames vacíos por defecto para evitar errores cuando no hay datos
    sin_compra_df = pd.DataFrame(columns=["CLIENTE", "FECHA", "EJECUTIVO", "VALOR_CTE", "SUC", "VENTA", "LC_ACTUAL", "LC_FINAL", "NOTAS", "OBSERVACION"])
    compras_validas = pd.DataFrame(columns=["CLIENTE", "FOLIO_POS", "FECHA_VENTA", "TOTALFACTURA", "DIAS_PARA_COMPRA"])
    clientes_autorizados_mes = pd.DataFrame(columns=["CLIENTE", "FECHA", "EJECUTIVO", "VENTA", "SUC", "LC_ACTUAL", "LC_FINAL"])
    clientes_con_compra_mes = pd.DataFrame(columns=["CLIENTE"])
    clientes_sin_compra_mes = pd.DataFrame(columns=["CLIENTE"])
    
    if not bitacora.empty:
        # Si no hay datos de ventas, crear DataFrame vacío para evitar errores
        if ventas.empty:
            ventas = pd.DataFrame(columns=["CLIENTE", "FECHA_VENTA", "FOLIO_POS", "TOTALFACTURA"])
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

        # Los datos de bitácora ya vienen filtrados por el mes seleccionado
        total_clientes = bitacora["CLIENTE"].nunique()
        clientes_con_compra = compras_validas["CLIENTE"].nunique()
        clientes_sin_compra = total_clientes - clientes_con_compra
        total_recompra = df_recompra["FOLIO_POS"].nunique() if not df_recompra.empty else 0
        
        # Clientes innecesarios del mes seleccionado
        clientes_innecesarios = bitacora[bitacora["innecesario"] == "SI"]["CLIENTE"].nunique()
        
        # Filtrar solo AUTORIZADOS del mes seleccionado
        clientes_autorizados_mes = bitacora[
            bitacora["VENTA"].str.strip().str.upper() == "AUTORIZADA"
        ]
        
        porcentaje_bitacora_recompra = round((clientes_autorizados_mes["CLIENTE"].nunique() / total_recompra) * 100, 2) if total_recompra > 0 else 0

        # Clientes con compra (entre los autorizados)
        clientes_con_compra_mes = compras_validas[
            compras_validas["CLIENTE"].isin(clientes_autorizados_mes["CLIENTE"])
        ]

        # Clientes sin compra (autorizados sin match en ventas)
        clientes_sin_compra_mes = clientes_autorizados_mes[
            ~clientes_autorizados_mes["CLIENTE"].isin(clientes_con_compra_mes["CLIENTE"])
        ]


        # Layout
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown(f"""
                <div style="border: 2px solid #ff4b4b; border-radius: 10px; padding: 15px; background-color: #fff3f3;">
                    <h4 style="margin: 0; color: #ff4b4b;">📌 % Clientes recompra registrados</h4>
                    <p style="font-size: 28px; font-weight: bold; margin: 0; color: #000;">{porcentaje_bitacora_recompra}%</p>
                </div>
            """, unsafe_allow_html=True)

            st.metric("📋 Total Facturas Recompra", total_recompra)
            st.metric("📎 Clientes autorizados registrados", clientes_autorizados_mes["CLIENTE"].nunique())
            st.metric("✅ Clientes con compra", clientes_con_compra_mes["CLIENTE"].nunique())
            st.metric("❌ Clientes sin compra", clientes_sin_compra_mes["CLIENTE"].nunique())
            st.metric("🟡 Solicitudes innecesarias", clientes_innecesarios)

            porcentaje_sin_compra = round((
                clientes_sin_compra_mes["CLIENTE"].nunique() / clientes_autorizados_mes["CLIENTE"].nunique()
            ) * 100, 2) if clientes_autorizados_mes["CLIENTE"].nunique() > 0 else 0

            st.markdown(f"""
                <div style="border: 2px solid #2b7bba; border-radius: 10px; padding: 15px; background-color: #e6f2ff; margin-top: 15px;">
                    <h4 style="margin: 0; color: #2b7bba;">🚫 % Clientes sin compra</h4>
                    <p style="font-size: 28px; font-weight: bold; margin: 0; color: #000;">{porcentaje_sin_compra}%</p>
                </div>
            """, unsafe_allow_html=True)



        with col2:
            st.subheader("Distribución por ejecutivo (clientes sin compra)")

            # 1. Los datos de bitácora ya vienen filtrados al mes seleccionado
            bitacora_mes = bitacora.copy()

            # 2. Identificar clientes con compra válida
            clientes_con_compra_set = set(compras_validas["CLIENTE"].unique())

            # 3. Clientes sin compra (en base a bitácora del mes)
            sin_compra_df = bitacora_mes[~bitacora_mes["CLIENTE"].isin(clientes_con_compra_set)]

            # 4. Total de registros capturados por ejecutivo (del universo total en el mes)
            total_registrados_por_ejecutivo = bitacora_mes.groupby("EJECUTIVO")["CLIENTE"].nunique().reset_index().rename(columns={"CLIENTE": "Registros"})

            # 5. Registros con VENTA = 'NO AUTORIZADA'
            no_autorizada_df = bitacora_mes[bitacora_mes["VENTA"] == "NO AUTORIZADA"]
            no_autorizada_por_ejecutivo = no_autorizada_df.groupby("EJECUTIVO")["CLIENTE"].nunique().reset_index().rename(columns={"CLIENTE": "No aut."})

            # 6. Registros sin compra
            sin_compra_por_ejecutivo = sin_compra_df.groupby("EJECUTIVO")["CLIENTE"].nunique().reset_index().rename(columns={"CLIENTE": "Sin compra"})

            # 7. Unir todo en un resumen
            resumen_ejecutivo = total_registrados_por_ejecutivo.merge(
                no_autorizada_por_ejecutivo, on="EJECUTIVO", how="left"
            ).merge(
                sin_compra_por_ejecutivo, on="EJECUTIVO", how="left"
            )

            resumen_ejecutivo.fillna(0, inplace=True)

            # 8. Calcular el porcentaje de clientes sin compra
            resumen_ejecutivo["% Sin compra"] = (
                resumen_ejecutivo["Sin compra"] / resumen_ejecutivo["Registros"] * 100
            ).round(2)

            # 9. Reordenar columnas
            resumen_ejecutivo = resumen_ejecutivo[["EJECUTIVO", "Registros", "No aut.", "Sin compra", "% Sin compra"]]

            # 10. Función para aplicar colores basados en porcentaje
            def color_percentage(val):
                if pd.isna(val):
                    return ''
                if val >= 75:
                    return 'background-color: #ffcccc; color: black'  # Rojo claro con texto negro
                elif val >= 50:
                    return 'background-color: #ffe6cc; color: black'  # Naranja claro con texto negro
                elif val >= 25:
                    return 'background-color: #ffffcc; color: black'  # Amarillo claro con texto negro
                else:
                    return 'background-color: #ccffcc; color: black'  # Verde claro con texto negro

            # 10. Mostrar tabla estilizada
            styled_df = resumen_ejecutivo.sort_values(by="% Sin compra", ascending=False).style.format({
                "% Sin compra": "{:.2f}",
                "Registros": "{:.0f}",
                "No aut.": "{:.0f}",
                "Sin compra": "{:.0f}"
            }).map(color_percentage, subset=["% Sin compra"])

            st.dataframe(styled_df, use_container_width=True)

            # 11. KPI de actualizaciones de cliente en el mes seleccionado (color amarillo claro)
            actualizaciones_cliente = bitacora_mes[bitacora_mes["Actualizacion"] == "SI"].shape[0]
            visitas_domiciliarias = bitacora_mes[bitacora_mes["VENTA"] == "VISITA DOMICILIARIA"].shape[0]
            clientes_rechazados = bitacora_mes[bitacora_mes["VENTA"] == "NO AUTORIZADA"].shape[0]

            kpi_col1, kpi_col2,kpi_col3 = st.columns(3)

            with kpi_col1:
                st.markdown(f"""
                    <div style="margin-top: 20px; border: 2px solid #f7c948; border-radius: 10px; padding: 15px; background-color: #fff8e1;">
                        <h4 style="margin: 0; color: #f7c948;">📎 Registros con actualización</h4>
                        <p style="font-size: 24px; font-weight: bold; margin: 0; color: #000;">{actualizaciones_cliente}</p>
                    </div>
                """, unsafe_allow_html=True)

            with kpi_col2:
                st.markdown(f"""
                    <div style="margin-top: 20px; border: 2px solid #6fa24f; border-radius: 10px; padding: 15px; background-color: #edf7ed;">
                        <h4 style="margin: 0; color: #6fa24f;">🏠 Registros con visita domiciliaria</h4>
                        <p style="font-size: 24px; font-weight: bold; margin: 0; color: #000;">{visitas_domiciliarias}</p>
                    </div>
                """, unsafe_allow_html=True)

            with kpi_col3:
                st.markdown(f"""
                    <div style="margin-top: 20px; border: 2px solid #f28b82; border-radius: 10px; padding: 15px; background-color: #fdecea;">
                        <h4 style="margin: 0; color: #f28b82;">❌ Registros no autorizados</h4>
                        <p style="font-size: 24px; font-weight: bold; margin: 0; color: #000;">{clientes_rechazados}</p>
                    </div>
                """, unsafe_allow_html=True)




        # Agregar VALOR_CTE a sin_compra_df
        valor_cte_df["ID_CLIENTE"] = valor_cte_df["ID_CLIENTE"].astype(str).str.strip()
        sin_compra_df["CLIENTE"] = sin_compra_df["CLIENTE"].astype(str).str.strip()
        sin_compra_df = sin_compra_df.merge(valor_cte_df, left_on="CLIENTE", right_on="ID_CLIENTE", how="left")
        sin_compra_df.drop(columns=["ID_CLIENTE"], inplace=True)

        # ✅ Reemplazar nulos por "Nuevo"
        sin_compra_df["VALOR_CTE"] = sin_compra_df["VALOR_CTE"].fillna("Nuevo")

        # Calcular distribución porcentual de los tipos de VALOR_CTE
        distribucion_valor_cte = (
            sin_compra_df.groupby("VALOR_CTE")["CLIENTE"]
            .nunique()
            .reset_index()
            .rename(columns={"CLIENTE": "Clientes sin compra","VALOR_CTE":"Clasificación de cliente"})
        )

        # Usar total_clientes (clientes registrados) como base para el porcentaje
        distribucion_valor_cte["% No compra"] = round((distribucion_valor_cte["Clientes sin compra"] / total_clientes) * 100, 2)

        # Función para aplicar colores a porcentajes
        def color_no_compra(val):
            if pd.isna(val):
                return ''
            if val >= 15:
                return 'background-color: #ffcccc; color: black'  # Rojo claro con texto negro
            elif val >= 10:
                return 'background-color: #ffe6cc; color: black'  # Naranja claro con texto negro
            elif val >= 5:
                return 'background-color: #ffffcc; color: black'  # Amarillo claro con texto negro
            else:
                return 'background-color: #ccffcc; color: black'  # Verde claro con texto negro

        # Ordenar de mayor a menor y mostrar con estilo
        st.subheader("📊 Distribución de clasificación de cliente entre clientes sin compra")
        styled_valor_cte = distribucion_valor_cte.sort_values(by="% No compra", ascending=False).style.format({
            "% No compra": "{:.2f} %",
            "Clientes sin compra": "{:.0f}"
        }).map(color_no_compra, subset=["% No compra"])

        st.dataframe(styled_valor_cte, use_container_width=True)

        # Tabla de solicitudes innecesarias por sucursal
        st.subheader("🟡 Solicitudes innecesarias por Sucursal")
        
        # Filtrar registros innecesarios del mes seleccionado
        solicitudes_innecesarias = bitacora[
            bitacora["innecesario"] == "SI"
        ].copy()
        
        if not solicitudes_innecesarias.empty:
            # Crear tabla agrupada por sucursal
            tabla_innecesarias = (
                solicitudes_innecesarias
                .groupby("SUC")
                .agg({
                    "CLIENTE": "nunique"
                })
                .reset_index()
                .rename(columns={
                    "SUC": "Sucursal",
                    "CLIENTE": "Solicitudes innecesarias"
                })
            )
            
            # Calcular porcentaje respecto al total de solicitudes innecesarias
            total_innecesarias = tabla_innecesarias["Solicitudes innecesarias"].sum()
            tabla_innecesarias["% del total"] = (
                tabla_innecesarias["Solicitudes innecesarias"] / total_innecesarias * 100
            ).round(2)
            
            # Ordenar por cantidad de solicitudes innecesarias (mayor a menor)
            tabla_innecesarias = tabla_innecesarias.sort_values(
                by="Solicitudes innecesarias", ascending=False
            )
            
            # Función para aplicar colores a solicitudes innecesarias
            def color_innecesarias(val):
                if pd.isna(val):
                    return ''
                if val >= 5:
                    return 'background-color: #ffcccc; color: black'  # Rojo claro con texto negro
                elif val >= 3:
                    return 'background-color: #ffe6cc; color: black'  # Naranja claro con texto negro
                elif val >= 1:
                    return 'background-color: #ffffcc; color: black'  # Amarillo claro con texto negro
                else:
                    return 'background-color: #ccffcc; color: black'  # Verde claro con texto negro

            def color_porcentaje_innecesarias(val):
                if pd.isna(val):
                    return ''
                if val >= 30:
                    return 'background-color: #ffcccc; color: black'  # Rojo claro con texto negro
                elif val >= 20:
                    return 'background-color: #ffe6cc; color: black'  # Naranja claro con texto negro
                elif val >= 10:
                    return 'background-color: #ffffcc; color: black'  # Amarillo claro con texto negro
                else:
                    return 'background-color: #ccffcc; color: black'  # Verde claro con texto negro

            # Aplicar estilo
            styled_innecesarias = tabla_innecesarias.style.format({
                "% del total": "{:.2f}%",
                "Solicitudes innecesarias": "{:.0f}"
            }).map(color_innecesarias, subset=["Solicitudes innecesarias"]).map(color_porcentaje_innecesarias, subset=["% del total"])
            
            st.dataframe(styled_innecesarias, use_container_width=True)
            
            # Mostrar detalle de los registros innecesarios
            st.subheader("📋 Detalle de solicitudes innecesarias")
            
            # Seleccionar columnas relevantes para mostrar
            columnas_detalle = ["FECHA", "CLIENTE", "SUC", "EJECUTIVO", "VENTA", "LC_ACTUAL", "LC_FINAL", "OBSERVACION"]
            detalle_innecesarias = solicitudes_innecesarias[columnas_detalle].copy()
            detalle_innecesarias["FECHA"] = detalle_innecesarias["FECHA"].dt.strftime("%Y-%m-%d")
            
            # Renombrar columnas para mejor presentación
            detalle_innecesarias = detalle_innecesarias.rename(columns={
                "SUC": "Sucursal"
            })
            
            st.dataframe(detalle_innecesarias.reset_index(drop=True), use_container_width=True)
        else:
            st.info(f"✅ No hay solicitudes innecesarias registradas en {mes_seleccionado} {anio_seleccionado}.")

    # Tabla de clientes sin compra con filtros
    st.subheader("📋 Clientes sin compra")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        filtro_rango = st.selectbox("Rango de fechas", ["Día específico", "Mes específico", "Año completo", "Histórico"])

    with col2:
        filtro_ejecutivo = st.selectbox("Ejecutivo", ["Todos"] + sorted(sin_compra_df["EJECUTIVO"].dropna().unique()))

    with col3:
        anio_default = fecha_actual.year
        mes_default = fecha_actual.month
        fecha_inicio, fecha_fin = None, None

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

    with col4:
        cc_opciones = ["Todos"] + sorted(sin_compra_df["VALOR_CTE"].dropna().unique())
        filtro_cc = st.selectbox("Clasificacion de Cliente", cc_opciones)

    # Aplicar filtros
    filtro_df = sin_compra_df.copy()
    filtro_df = filtro_df[(filtro_df["FECHA"] >= pd.to_datetime(fecha_inicio)) & (filtro_df["FECHA"] <= pd.to_datetime(fecha_fin))]

    if filtro_ejecutivo != "Todos":
        filtro_df = filtro_df[filtro_df["EJECUTIVO"] == filtro_ejecutivo]

    if filtro_cc != "Todos":
        filtro_df = filtro_df[filtro_df["VALOR_CTE"] == filtro_cc]

    # Renombrar columna
    filtro_df = filtro_df.rename(columns={"VALOR_CTE": "CC"})

    columnas_mostrar = ["FECHA", "CLIENTE", "EJECUTIVO", "SUC", "VENTA", "LC_ACTUAL", "LC_FINAL", "CC", "NOTAS", "OBSERVACION"]
    df_display = filtro_df[columnas_mostrar].copy()
    
    # Solo formatear fecha si hay datos y la columna tiene valores datetime
    if not df_display.empty and pd.api.types.is_datetime64_any_dtype(df_display["FECHA"]):
        df_display["FECHA"] = df_display["FECHA"].dt.strftime("%Y-%m-%d")

    st.dataframe(df_display.reset_index(drop=True))
    
    # Mostrar mensaje si no hay datos
    if bitacora.empty:
        st.warning(f"No hay datos disponibles para {mes_seleccionado} {anio_seleccionado}. Selecciona un período con datos registrados.")


elif pagina == "Mensajes Sms":
    import pandas as pd
    import streamlit as st
    from datetime import datetime, timedelta
    import requests
    import io
    import base64

    # Importar tipos de SQLAlchemy
    from sqlalchemy.types import Integer, UnicodeText, DateTime
    from sqlalchemy.dialects.mssql import NVARCHAR

    st.header("📲 Envío de mensajes a clientes con compra aprobada y sin facturar")

    # ========== INICIALIZAR session_state ==========
    if "clientes_filtrados" not in st.session_state:
        st.session_state["clientes_filtrados"] = None

    # ========== FORMULARIO DE FILTRO ==========
    
    st.subheader("⚠️ Siempre usar el boton de filtrar para actualizar la informacion ⚠️")
    st.subheader("📋 Filtros de clientes ")
    venta_tipo = st.selectbox("Tipo de Venta", ["AUTORIZADA", "NO AUTORIZADA", "AUTORIZADA PARCIAL", "VISITA DOMICILIARIA"])
    facturado   = st.selectbox("¿Ya facturado?",      ["NO", "SI"])

    if st.button("🔍 Buscar clientes"):
        engine = get_connection()  # debe ser un SQLAlchemy Engine
        
        ## si quieres depurar agrega un top(1) y deja fijo tu numero  de telefono  en el max(bc.CEL_CTE) con comilla simple  o deja en blanco
        query = """
           SELECT 
                 BC.CLIENTE AS CLIENTE, 
                MAX(
				CASE 
					WHEN r.NOMBRECLIENTE IS NOT NULL THEN r.NOMBRECLIENTE 
					WHEN APROB.solicitante IS NOT NULL THEN APROB.solicitante
					ELSE
					'' END) 
					AS NOMBRE_CLIENTE, 
                MAX(BC.FECHA)            AS Fecha_bitacora, 
                MAX(BC.CEL_CTE)          AS TELEFONO,
                MAX(t.Tel1)              AS Tel1, 
                MAX(t.Tel2)              AS Tel2, 
                MAX(t.Tel3)              AS Tel3,
                MAX(BC.VENTA)            AS VENTA, 
                MAX(BC.ENGANCHE_REQUERIDO) AS ENGANCHE_REQUERIDO, 
                MAX(BC.ENGANCHE_RECIBIDO)  AS ENGANCHE_RECIBIDO, 
                MAX(BC.LC_ACTUAL)        AS LC_ACTUAL, 
                MAX(BC.LC_FINAL)         AS LC_FINAL
            FROM Bitacora_Credito BC
            LEFT JOIN Telefonos_crm T ON BC.CLIENTE = T.SapIdCliente  
            LEFT JOIN RPVENTA r   ON BC.CLIENTE = r.CLIENTE
            LEFT JOIN historico_ctes_aprob_sql APROB ON APROB.Cliente = BC.CLIENTE
            WHERE 
                MONTH(BC.FECHA) = MONTH(GETDATE())  
                AND YEAR(BC.FECHA)  = YEAR(GETDATE())   
                AND BC.VENTA        = %s
                AND LEN(BC.CEL_CTE) = 10
                AND BC.FACTURO      = %s
            GROUP BY BC.CLIENTE
        """
        df = pd.read_sql(query, engine, params=(venta_tipo, facturado))
        if not df.empty:
            st.success(f"Se encontraron {len(df)} clientes.")
            st.session_state["clientes_filtrados"] = df
        else:
            st.warning("No se encontraron clientes.")
            st.session_state["clientes_filtrados"] = None

    # ========== VISTA Y ENVÍO DE MENSAJES ==========
    df = st.session_state.get("clientes_filtrados")
    if df is not None:
        st.dataframe(df)
        st.subheader("✉️ Mensaje a enviar")

        with st.form("form_sms"):
            mensaje_base = st.text_area(
                "Cuerpo del mensaje",
                "Hola {nombre}, tu compra en Valdez Baluarte fue aprobada!! Por favor acércate a tu sucursal para finalizar el proceso."
            )
            enviar = st.form_submit_button("📤 Enviar mensajes")

        if enviar:
            API_TOKEN = "vGZiMWzV-Sca20zlZ5Mg1c0QVa0bioaC6dsS"
            url       = "https://api.zenvia.com/v2/channels/sms/messages"
            headers   = {"X-API-TOKEN": API_TOKEN, "Content-Type": "application/json"}

            enviados   = 0
            errores    = 0
            log_envios = []

            for _, row in df.iterrows():
                # Inicializar variables por cada fila
                telefono_formato = None

                cliente_id      = row["CLIENTE"]
                nombre_completo = row["NOMBRE_CLIENTE"] or "Cliente"
                primer_nombre   = nombre_completo.strip().split()[0]
                mensaje         = mensaje_base.format(nombre=primer_nombre)

                # Validación de longitud
                if len(mensaje) > 160:
                    status = "❌ Mensaje demasiado largo"
                    errores += 1
                    st.warning(f"⚠️ El mensaje para {primer_nombre} tiene {len(mensaje)} caracteres y NO se envió.")
                else:
                    telefono = row["TELEFONO"] or row["Tel1"] or row["Tel2"] or row["Tel3"]
                    if not telefono:
                        status = "⚠️ Sin teléfono"
                        errores += 1
                       # st.warning(f"⚠️ Cliente {cliente_id} no tiene teléfono disponible.")
                    else:
                        # Formatear teléfono
                        telefono_formato = f"521{telefono}" if not telefono.startswith("52") else telefono
                        body = {
                            "from": "SENDER_ID",
                            "to": telefono_formato,
                            "contents":[{"type":"text","text":mensaje}]
                        }
                        resp = requests.post(url, headers=headers, json=body)
                        if resp.status_code == 200:
                            enviados += 1
                            status = "✅ Enviado"
                           # st.success(f"✅ SMS enviado a {telefono_formato}")
                        else:
                            errores += 1
                            status = f"❌ Error {resp.status_code}"
                            st.warning(f"❌ Error al enviar a {telefono_formato}: {resp.text}")

                # Registrar envío
                log_envios.append({
                    "Cliente": cliente_id,
                    "Nombre": primer_nombre,
                    "Telefono": telefono_formato,
                    "Estado": status,
                    "Mensaje": mensaje,
                    "Fecha": datetime.now()
                })

            # Convertir a DataFrame y guardar histórico
            df_log = pd.DataFrame(log_envios)
            engine = get_connection()
            df_log.to_sql(
                name      = "historico_bitacora_envio_sms",
                con       = engine,
                if_exists = "append",
                index     = False,
                dtype     = {
                    "Cliente": Integer(),
                    "Nombre": NVARCHAR(length=100),
                    "Telefono": NVARCHAR(length=20),
                    "Estado": NVARCHAR(length=50),
                    "Mensaje": UnicodeText(),
                    "Fecha": DateTime()
                }
            )

            # Mostrar log, descarga y resumen
            st.subheader("📋 Detalle de envío de mensajes")
            st.dataframe(df_log)

            ts_file  = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reporte_envio_sms_{ts_file}.xlsx"
            buf      = io.BytesIO()
            df_log.to_excel(buf, index=False)
            b64      = base64.b64encode(buf.getvalue()).decode()
            href = (
                f'<a href="data:application/octet-stream;base64,{b64}" '
                f'download="{filename}">📥 Descargar reporte en Excel</a>'
            )
            st.markdown(href, unsafe_allow_html=True)

            st.info(f"✔️ Mensajes enviados: {enviados}")
            st.info(f"❌ Errores: {errores}")
