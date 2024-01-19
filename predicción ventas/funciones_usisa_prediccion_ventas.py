import pandas as pd
import numpy as np
import re
from unidecode import unidecode
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.seasonal import seasonal_decompose


#FUNCIONES PARA DF_NUEVO: 

#FUNCION PARA MANTENER LAS COLUMNAS DESEADAS Y NOS DESHACEMOS DEL RESTO
def eliminar_columnas_df_nuevo(df):  
    quedar = ['order_id', 'order_date', 'status',
              'order_total', 'order_subtotal', 'billing_first_name', 'billing_last_name'] 
    return df[quedar]


#FUNCION PARA CONVERTIR VARIABLES A FORMATO NUMERICO Y DATETIME
def convertir_variables_df_nuevo(df):
    df = df.copy()
    df['order_total'] = pd.to_numeric(df['order_total'], errors='coerce')
    df['order_subtotal'] = pd.to_numeric(df['order_subtotal'], errors='coerce')
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')
    return df


#FUNCION PARA LIMPIAR LAS STRINGS DE TILDES Y DE MAYUSCULAS
def clean(x):
    x = x.lower()
    x = re.sub(r'\W', ' ', x)
    x=unidecode(x)
    return x


#FUNCION PARA MANTENER SOLO LOS PEDIDOS COMPLETADAS 
def limpiar_status(df):
    df = df.copy()  # Asegúrate de trabajar con una copia del DataFrame
    df.loc[:, "status"] = df["status"].apply(clean)
    df = df.loc[df["status"]=="completed"]
    df.reset_index(drop=True, inplace=True)
    return df


#FUNCION PARA ELIMINAR PEDIDOS DE PRUEBA Y OTROS
def eliminar_pruebas_df_nuevo(df):
 
    nan_filas = df[df[['order_id', 'order_date', 'order_total', 'order_subtotal']].isnull().any(axis=1)]

    negativo_filas = df[(df['order_total'] < 0) | (df['order_subtotal'] < 0)]

    prueba_filas = df[df['order_subtotal'] < 3]

    filas_a_eliminar = set(nan_filas.index) | set(negativo_filas.index) | set(prueba_filas.index)

    df_limpio = df.drop(filas_a_eliminar)

    return df_limpio


#FUNCION PARA UNIR NOMBRE Y APELLIDOS CLIENTE EN UNA MISMA COLUMNA. ELIMINA COLUMNAS ORGINALES.
def unir_nombre(df):
    df['cliente_nombre'] = df['billing_first_name'] + ' ' + df['billing_last_name']
    df.drop(["billing_first_name", "billing_last_name"], axis=1, inplace=True)
    return df


#FUNCION PARA filtrar COLUMNAS DF_NUEVO 
def filtrar_df_nuevo(df):
    nuevo_orden_columnas = ['order_date', 'order_id', 'cliente_nombre', 'order_total']
    df_filtrado = df[nuevo_orden_columnas]
    return df_filtrado


#FUNCION GLOBAL PARA DF_NUEVO
def todas_las_funciones_nuevo(df):
    df=eliminar_columnas_df_nuevo(df)
    df=convertir_variables_df_nuevo(df)
    df=limpiar_status(df)
    df=eliminar_pruebas_df_nuevo(df)
    df=unir_nombre(df)
    df=filtrar_df_nuevo(df)
    return df






#FUNCIONES PARA DF_ANTIGUO:

#FUNCION PARA MANTENER LAS COLUMNAS DESEADAS Y NOS DESHACEMOS DEL RESTO
def eliminar_columnas_df_antiguo(df):  
    quedar = ['id_order', 'Cliente', 'fecha', 'total_price_tax_incl'] 
    return df[quedar]


#FUNCION PARA CONVERTIR VARIABLES A FORMATO NUMERICO Y DATETIME
def convertir_variables_df_antiguo(df):
    df = df.copy()
    df['total_price_tax_incl'] = pd.to_numeric(df['total_price_tax_incl'], errors='coerce')
    df["total_price_tax_incl"]=df["total_price_tax_incl"]/1000000
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    return df


#FUNCION PARA AGRUPAR POR ID_ORDER
def agrupar_por_id_order(df):
    df_agrupado = df.groupby('id_order').agg({
        'Cliente': 'first',
        'fecha': 'first',
        'total_price_tax_incl': 'sum'
    }).reset_index()
    
    df_agrupado = df_agrupado.sort_values(by='fecha', ascending=False)

    return df_agrupado


#FUNCION PARA ELIMINAR PEDIDOS DE PRUEBA Y OTROS
def eliminar_pruebas_df_antiguo(df):
    
    df['fecha'] = pd.to_datetime(df['fecha'])

    df_filtrado = df[df['fecha'] >= '2017-12-01']

    nan_filas = df_filtrado[df_filtrado[['id_order', 'fecha', 'total_price_tax_incl']].isnull().any(axis=1)]
    prueba_filas = df_filtrado[df_filtrado['total_price_tax_incl'] < 3]

    filas_a_eliminar = set(nan_filas.index) | set(prueba_filas.index)

    df_filtrado = df_filtrado.drop(filas_a_eliminar)

    return df_filtrado


#FUNCION PARA FILTRAR Y RENOMBRAR COLUMNAS DF_ANTIGUO 
def filtrar_df_antiguo(df):
    nuevo_orden_columnas = ['fecha', 'id_order', 'Cliente', 'total_price_tax_incl']
    df_filtrado = df[nuevo_orden_columnas]
    
    df_filtrado = df_filtrado.rename(columns={
        'fecha': 'order_date',
        'id_order': 'order_id',
        'Cliente': 'cliente_nombre',
        'total_price_tax_incl': 'order_total'
    })
    
    return df_filtrado


#FUNCION GLOBAL PARA DF_ANTIGUO
def todas_las_funciones_antiguo(df):
    df=eliminar_columnas_df_antiguo(df)
    df=convertir_variables_df_antiguo(df)
    df=agrupar_por_id_order(df)
    df=eliminar_pruebas_df_antiguo(df)
    df=filtrar_df_antiguo(df)
    return df






#FUNCIONES PARA  DF_NUEVO Y DF_ANTIGUO UNIDOS

#CONCATENAMOS EL DATAFRAME ANTIGUO CON EL NUEVO
def concatenar(x_nuevo,x_antiguo):
    df=pd.concat([x_nuevo,x_antiguo], axis=0)
    df.sort_values(by='order_date', ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


#FUNCION PARA CREAR TIMESERIES_DIARIO AGRUPAR PEDIDOS Y FACTURACION DIARIAMENTE Y RELLENAR SALTOS
def agrupar_diario(df):
    df["order_date"] = pd.to_datetime(df["order_date"])
    df_agrupado_diario = df.groupby(df['order_date'].dt.to_period("D")).agg({
        'order_id': 'nunique',
        'order_total': 'sum'
    }).reset_index()

    df_agrupado_diario.columns = ['fecha', 'total_pedidos', 'total_facturacion(€)']

    df_agrupado_diario = df_agrupado_diario.set_index('fecha').resample('D').asfreq().reset_index()
    df_agrupado_diario['fecha'] = df_agrupado_diario['fecha'].dt.to_timestamp()
    df_agrupado_diario = df_agrupado_diario.set_index('fecha')

    df_agrupado_diario['total_pedidos'] = df_agrupado_diario['total_pedidos'].fillna(0).astype(int)
    df_agrupado_diario['total_facturacion(€)'] = df_agrupado_diario['total_facturacion(€)'].fillna(0).round(2)
    
    return df_agrupado_diario
        

#FUNCION PARA VISUALIZAR TIMESERIES DIARIO
#GRAFICO DE FACTURACION TOTAL DIARIA
def timeseries_facturacion_diario(timeseries_diario):
    plt.figure(figsize=(10, 5))
    plt.plot(timeseries_diario.index, timeseries_diario['total_facturacion(€)'], color='orange', label='Total Facturación Diario')
    plt.title('Total Dinero Facturado(€) por Día')
    plt.xlabel('Fecha')
    plt.ylabel('Euros(€)')
    plt.tight_layout()
    plt.legend()
    plt.show()

#GRAFICO DE TOTAL PEDIDOS POR DIA
def timeseries_pedidos_diario(timeseries_diario):
    plt.figure(figsize=(10, 5))
    plt.plot(timeseries_diario.index, timeseries_diario['total_pedidos'], color='blue', label='Total Pedidos por Día')
    plt.title('Total Pedidos por Día')
    plt.xlabel('Fecha')
    plt.ylabel('Número de Pedidos')
    plt.tight_layout()
    plt.legend()
    plt.show()
    

#FUNCION PARA VISUALIZAR TIMESERIES SEMANAL    
#GRAFICO DE FACTURACION TOTAL SEMANAL
def timeseries_facturacion_semanal(timeseries_semanal):
    plt.figure(figsize=(10, 5))
    plt.plot(timeseries_semanal.index, timeseries_semanal['total_facturacion(€)'], color='orange', label='Total Facturación Semanal')
    plt.title('Total Dinero Facturado(€) por Semana')
    plt.xlabel('Fecha')
    plt.ylabel('Euros(€)')
    plt.xticks(timeseries_semanal.index[timeseries_semanal.index.isocalendar().week == 1], [pd.to_datetime(date).strftime('%Y-W%U') for date in timeseries_semanal.index[timeseries_semanal.index.isocalendar().week == 1]], rotation=45, ha='right')
    plt.tight_layout()
    plt.legend()
    plt.show()

#GRAFICO DE TOTAL PEDIDOS POR SEMANA
def timeseries_pedidos_semanal(timeseries_semanal):
    plt.figure(figsize=(10, 5))
    plt.plot(timeseries_semanal.index, timeseries_semanal['total_pedidos'], color='blue', label='Total Pedidos Semanales')
    plt.title('Total Pedidos por Semana')
    plt.xlabel('Fecha')
    plt.ylabel('Número de Pedidos')
    plt.xticks(timeseries_semanal.index[timeseries_semanal.index.isocalendar().week == 1], [pd.to_datetime(date).strftime('%Y-W%U') for date in       timeseries_semanal.index[timeseries_semanal.index.isocalendar().week == 1]], rotation=45, ha='right')
    plt.tight_layout()
    plt.legend()
    plt.show()
    
#FUNCION PARA VISUALIZAR ZOOM TIMESERIES SEMANAL    
#GRAFICO ZOOM DE FACTURACION TOTAL SEMANAL
def zoom_facturacion_semanal(timeseries_semanal):
    plt.figure(figsize=(10, 5))
    plt.plot(timeseries_semanal.index, timeseries_semanal['total_facturacion(€)'], color='orange', label='Total Facturación Semanal')
    plt.title('Total Dinero Facturado(€) por Semana')
    plt.xlabel('Fecha')
    plt.ylabel('Euros(€)')
    #plt.xticks(timeseries_semanal.index[timeseries_semanal.index.isocalendar().week == 1], [pd.to_datetime(date).strftime('%Y-W%U') for date in timeseries_semanal.index[timeseries_semanal.index.isocalendar().week == 1]], rotation=45, ha='right')
    plt.tight_layout()
    plt.legend()
    plt.show()

#GRAFICO ZOOM DE TOTAL PEDIDOS POR SEMANA
def zoom_pedidos_semanal(timeseries_semanal):
    plt.figure(figsize=(10, 5))
    plt.plot(timeseries_semanal.index, timeseries_semanal['total_pedidos'], color='blue', label='Total Pedidos Semanales')
    plt.title('Total Pedidos por Semana')
    plt.xlabel('Fecha')
    plt.ylabel('Número de Pedidos')
    #plt.xticks(timeseries_semanal.index[timeseries_semanal.index.isocalendar().week == 1], [pd.to_datetime(date).strftime('%Y-W%U') for date in       timeseries_semanal.index[timeseries_semanal.index.isocalendar().week == 1]], rotation=45, ha='right')
    plt.tight_layout()
    plt.legend()
    plt.show()
   

#FUNCION PARA VISUALIZAR TIMESERIES MENSUAL
#GRAFICO DE FACTURACION TOTAL MENUSAL 
def timeseries_facturacion_mensual(timeseries_mensual):
    
    plt.figure(figsize=(10, 5))
    plt.plot(timeseries_mensual.index, timeseries_mensual['total_facturacion(€)'], color='orange', marker='o', markersize=4, label='Total Facturación Mensual')
    plt.title('Total Dinero Facturado(€) por Mes')
    plt.xlabel('Fecha')
    plt.ylabel('Euros (€)')
    plt.xticks(timeseries_mensual.index[timeseries_mensual.index.month == 1], [pd.to_datetime(date).strftime('%Y-%m') for date in timeseries_mensual.index[timeseries_mensual.index.month == 1]], rotation=45, ha='right')
    plt.tight_layout()
    plt.legend()
    plt.show()

# GRAFICO DE TOTAL PEDIDOS POR MES
def timeseries_pedidos_mensual(timeseries_mensual):
    plt.figure(figsize=(10, 5))
    plt.bar(timeseries_mensual.index, timeseries_mensual['total_pedidos'], color='blue', label='Total Pedidos Mensuales', width=20)
    plt.title('Total Pedidos por Mes')
    plt.xlabel('Fecha')
    plt.ylabel('Número de Pedidos')
    plt.xticks(timeseries_mensual.index[timeseries_mensual.index.month == 1], [pd.to_datetime(date).strftime('%Y-%m') for date in timeseries_mensual.index[timeseries_mensual.index.month == 1]], rotation=45, ha='right')
    plt.tight_layout()
    plt.legend()
    plt.show()


#FUNCION PARA VISUALIZAR TENDENCIA, ESTACIONALIDAD Y RUIDO
def seasonal_decomposition(df, columna, period=12, color=None):
    descomposicion = seasonal_decompose(df[columna], model='additive', period=period)
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    
    descomposicion.trend.plot(ax=ax1, color=color)
    ax1.set_ylabel('Tendencia')
    ax1.set_title(f'Descomposición de la Serie Temporal de {columna}')

    descomposicion.seasonal.plot(ax=ax2, color=color)
    ax2.set_ylabel('Estacionalidad')

    ax3.scatter(df.index, descomposicion.resid, color=color, marker='.')
    ax3.axhline(y=0, color='r', linestyle='--', linewidth=1)
    ax3.set_ylabel('Residuo')

    ax3.set_xlabel('Mes')
    plt.tight_layout()
    plt.show()
    
    
#GRAFICO TRAIN/TEST FACTURACION MENSUAL
def train_test_facturacion_mensual(facturacion_mensual, test_fm, y_test_fm):
    plt.figure(figsize=(16,8))
    plt.plot(facturacion_mensual.index[-365:], facturacion_mensual['total_facturacion(€)'].tail(365), color='orange', marker='o', label = 'Train Facturacion')
    plt.plot(test_fm.index, y_test_fm, color = 'green', marker= 'o', label = 'Test Facturacion')
    plt.title('Train / Test Split Total Facturación Mensual(€)')
    plt.xlabel('Fecha')
    plt.ylabel('Euros(€)')
    plt.xticks(facturacion_mensual.index[facturacion_mensual.index.month == 1], [pd.to_datetime(date).strftime('%Y-%m') for date in facturacion_mensual.index[facturacion_mensual.index.month == 1]], rotation=45, ha='right')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    
#GRAFICO TRAIN/TEST PEDIDOS MENSUAL
def train_test_pedidos_mensual(pedidos_mensual, test_pm, y_test_pm):
    plt.figure(figsize=(16,8))
    plt.bar(pedidos_mensual.index[-365:], pedidos_mensual['total_pedidos'].tail(365), color='blue', label = 'Train Pedidos', width=20)
    plt.bar(test_pm.index, y_test_pm, color = 'green', label = 'Test Pedidos', width=20)
    #plt.plot(test_fm.index, predictions_fm_autoarima, color = 'red', linewidth=4, label = 'Predicted Facturación')
    plt.title('Train / Test Split Total Pedidos Mensual')
    plt.xlabel('Fecha')
    plt.ylabel('Número de Pedidos')
    plt.xticks(pedidos_mensual.index[pedidos_mensual.index.month == 1], [pd.to_datetime(date).strftime('%Y-%m') for date in pedidos_mensual.index[pedidos_mensual.index.month == 1]], rotation=45, ha='right')
    plt.legend()
    plt.grid(True)
    plt.show()  
    
    
#FUNCIONES GRAFICOS AUTOARIMA:   
#GRAFICO PREDICCION FACTURACION MENSUAL MODELO AUTOARIMA
def prediccion_facturacion_mensual(facturacion_mensual, test_fm, y_test_fm, predictions_fm_autoarima,lower_conf_fm, upper_conf_fm):
    plt.figure(figsize=(16,8))
    plt.plot(facturacion_mensual.index[-365:], facturacion_mensual['total_facturacion(€)'].tail(365), color='orange', marker='o', label = 'Train Facturacion')
    plt.plot(test_fm.index, y_test_fm, color = 'green', marker= 'o', label = 'Real Facturacion')
    plt.plot(test_fm.index, predictions_fm_autoarima, color = 'red', linewidth=4, label = 'Predicción Facturación')
    plt.fill_between(test_fm.index, lower_conf_fm, upper_conf_fm, color='pink', alpha=0.5, label='Intervalo de Confianza')
    plt.title('Predicción AutoARIMA - Total Facturación Mensual(€)')
    plt.xlabel('Fecha')
    plt.ylabel('Euros(€)')
    plt.xticks(facturacion_mensual.index[facturacion_mensual.index.month == 1], [pd.to_datetime(date).strftime('%Y-%m') for date in facturacion_mensual.index[facturacion_mensual.index.month == 1]], rotation=45, ha='right')
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.show()
    
#GRAFICO PREDICCION PEDIDOS MENSUAL MODELO AUTOARIMA
def prediccion_pedidos_mensual(pedidos_mensual, test_pm, y_test_pm, predictions_pm_autoarima, lower_conf_pm, upper_conf_pm):
    plt.figure(figsize=(16,8))
    plt.bar(pedidos_mensual.index[-365:], pedidos_mensual['total_pedidos'].tail(365), color='blue', label = 'Train Pedidos', width=20)
    plt.bar(test_pm.index, y_test_pm, color = 'green', label = 'Real Pedidos', width=20)
    plt.bar(test_pm.index, predictions_pm_autoarima, color = 'red', label = 'Predicción Pedidos', width=20)
    plt.fill_between(test_pm.index, lower_conf_pm, upper_conf_pm, color='pink', alpha=0.5, label='Intervalo de Confianza')
    plt.title('Predicción AutoARIMA - Total Pedidos Mensual')
    plt.xlabel('Fecha')
    plt.ylabel('Número de Pedidos')
    plt.xticks(pedidos_mensual.index[pedidos_mensual.index.month == 1], [pd.to_datetime(date).strftime('%Y-%m') for date in pedidos_mensual.index[pedidos_mensual.index.month == 1]], rotation=45, ha='right')
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.show()