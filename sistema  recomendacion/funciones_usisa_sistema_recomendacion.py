#LIMPIEZA Y MANIPULACION DE DATOS
import pandas as pd
import re
from unidecode import unidecode
import numpy as np
import datetime

#VISUALIZACION
import seaborn as sns
import matplotlib.pyplot as plt


#FUNCION PARA MANTENER LAS COLUMNAS DESEADAS Y NOS DESHACEMOS DEL RESTO
def eliminar_columnas_df_nuevo(df):  
    quedar = ['order_id', 'order_date', 'status',
              'order_total', 'order_subtotal', 'order_currency', 'billing_first_name',
              'billing_last_name'] 
    quedar.extend([f'line_item_{i}' for i in range(1, 34)])
    return df[quedar]


#FUNCION PARA CONVERTIR VARIABLES A FORMATO NUMERICO Y DATETIME
def convertir_variables(df):
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
def eliminar_pruebas(df):
 
    nan_filas = df[df[['order_id', 'order_date', 'order_total', 'order_subtotal']].isnull().any(axis=1)]

    negativo_filas = df[(df['order_total'] < 0) | (df['order_subtotal'] < 0)]

    prueba_filas = df[df['order_subtotal'] < 3]

    filas_a_eliminar = set(nan_filas.index) | set(negativo_filas.index) | set(prueba_filas.index)

    df_limpio = df.drop(filas_a_eliminar)

    return df_limpio


#DESGLOSAR LOS DIFERENTES PRODUCTOS DE CADA PEDIDO EN UNA FILA INDEPENDIENTE MANTENIENDO EL RESTO DE DATOS 
def desglosar_items(df):
    columnas_items=[f'line_item_{i}' for i in range(1,34)]
    resto_columnas=['billing_first_name', 'billing_last_name', 'order_date',
       'order_id']

    df_melted = pd.melt(df, id_vars=resto_columnas, value_vars=columnas_items, var_name='line_item')

    df_melted = df_melted.dropna()
    df_melted.reset_index(drop=True,inplace=True)
    return df_melted


#USANDO REGEX EXTRAEMOS EL NOMBRE DE CADA PRODUCTO
def procesar_dataframe_con_producto(df):
    def obtener_producto(z):
        match_producto = re.search(r'name:(.*?)(?=\|)', z)
        if match_producto:
            valor_producto = str(match_producto.group(1))
            return valor_producto
        else:
            return None

    df['producto'] = df['value'].apply(obtener_producto)
    return df


#EXTRAEMOS EL ID DE CADA PRODUCTO
def procesar_dataframe_con_product_id(df):
    def obtener_product_id(z):
        match_product_id = re.search(r'product_id:(\d+\.?\d*)', z)
        if match_product_id:
            valor_product_id = int(match_product_id.group(1))
            return valor_product_id
        else:
            return None

    df["product_id"] = df["value"].apply(obtener_product_id)
    return df


#EXTRAEMOS LA CANTIDAD COMPRADA DE CADA PRODUCTO
def procesar_dataframe_con_cantidad(df):
    def obtener_cantidad(z):
        match_cantidad = re.search(r'quantity:(\d+\.?\d*)', z)
        if match_cantidad:
            valor_cantidad = int(match_cantidad.group(1))
            return valor_cantidad
        else:
            return None

    df["quantity"] = df["value"].apply(obtener_cantidad)
    return df


#EXTRAEMOS EL PRECIO TOTAL DE CADA PRODUCTO
def procesar_dataframe_con_total_precio(df):
    def obtener_total_precio(z):
        match_total = re.search(r'total:(\d+\.?\d*)', z)
        if match_total:
            valor_total = float(match_total.group(1))
            return valor_total
        else:
            return None

    df['total_precio'] = df['value'].apply(obtener_total_precio)
    return df


#UNIMOS NOMBRE Y APELLIDOS DE CADA CLIENTE EN UNA MISMA COLUMNA. ELIMINAMOS Y CAMBIAMOS EL NOMBRE DE LAS COLUMNAS.
def procesar_dataframe(df):
    df['cliente_nombre'] = df['billing_first_name'] + ' ' + df['billing_last_name']
    df.drop(["billing_first_name", "billing_last_name", "value", "line_item"], axis=1, inplace=True)

    columnas_dic = {
        'order_date': 'fecha',
        'order_id': 'order_id',
        'cliente_nombre': 'cliente_nombre',
        'product_id': 'producto_id',
        'producto': 'producto_nombre',
        'quantity': 'product_cantidad',
        'total_precio': 'total_precio'
    }

    df.rename(columns=columnas_dic, inplace=True)

    return df


#FUNCION PARA ORDENAR COLUMNAS DESEADAS 
def ordenar_columnas_df_nuevo(df):  
    ordenar = ['fecha','order_id','cliente_nombre', 'producto_nombre', 'producto_id', 'product_cantidad', 'total_precio'] 
    return df[ordenar]


#FUNCION GLOBAL PARA DF_NUEVO
def todas_funciones_nuevo(df):
    df=eliminar_columnas_df_nuevo(df)
    df=convertir_variables(df)
    df=limpiar_status(df)
    df=eliminar_pruebas(df)
    df=desglosar_items(df)
    df=procesar_dataframe_con_producto(df)
    df=procesar_dataframe_con_product_id(df)
    df=procesar_dataframe_con_cantidad(df)
    df=procesar_dataframe_con_total_precio(df)
    df=procesar_dataframe(df)
    df=ordenar_columnas_df_nuevo(df)
    return df


#FUNCIONES PARA EDA
#FUNCION PARA AGRUPAR PRODUCTOS POR ID Y SACAR EL NUMERO DE VENTAS POR PRODUCTO
def agrupar_y_seleccionar_nombre(df, id_columna, nombre_columna, cantidad_columna):
    modas = df.groupby(id_columna)[nombre_columna].apply(lambda x: x.mode().iloc[0]).reset_index()
    sumas = df.groupby(id_columna)[cantidad_columna].sum().reset_index()
    resultado = pd.merge(sumas, modas, on=id_columna, how='inner')
    resultado = resultado.sort_values(by=cantidad_columna, ascending=False)
    resultado = resultado.reset_index(drop=True)
    return resultado


#FUNCION PARA VISUALIZAR CANTIDADES DE PRODUCTOS VENDIDOS
def plot_top_segments(df):
    df = df.sort_values(by='product_cantidad', ascending=False)

    for i in range(5):
        start_idx = 0
        end_idx = 0
        
        if i == 0:
            segmento = df.iloc[:10]
            end_idx = 10
        else:
            start_idx = 10 + (i - 1) * 25
            end_idx = start_idx + 25
            segmento = df.iloc[start_idx:end_idx]

        segmento = segmento[::-1]

        plt.figure(figsize=(10, 6))
        plt.barh(segmento['producto_nombre'], segmento['product_cantidad'], color='skyblue')
        plt.title(f'Top {start_idx + 1}-{end_idx} Productos')
        plt.xlabel('Cantidad Vendida')
        plt.ylabel('Productos')
        plt.tight_layout()
        plt.show()
        
        
# FUNCION PARA BOX PLOT NUMERO DE VENTAS POR ID_PRODCUTO
def plot_boxplot(df):
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='product_cantidad', data=df, color='skyblue')
    plt.title('Distribución de Cantidades Vendidas por Producto', size=22)
    plt.xlabel('Número de Ventas por Producto')
    plt.show()

