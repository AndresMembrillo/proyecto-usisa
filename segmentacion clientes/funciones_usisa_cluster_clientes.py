import pandas as pd
import re
from unidecode import unidecode
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import folium
from geopy.geocoders import Nominatim


#FUNCION PARA MANTENER LAS COLUMNAS DESEADAS Y NOS DESHACEMOS DEL RESTO
def eliminar_columnas_df_nuevo(df):  
    quedar = ['order_id', 'order_date', 'status',
              'order_total', 'order_subtotal', 'order_currency', 'billing_first_name',
              'billing_last_name', 'billing_email', 'billing_address_1',
              'billing_postcode', 'billing_city', 'billing_state', 'billing_country'] 
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


#FUNCION PARA ELIMINAR FILAS DE EMAIL CON VALORES NANS
def limpiar_email(df):
    df = df.dropna(subset=['billing_email']).reset_index(drop=True)  
    return df


#FUNCION PARA CREAR ID_CLIENTE PARA TODOS LOS CLIENTES TENIENDO EN CUENTA EL EMAIL DE ENVIO
def asignar_id_cliente(df):
    df['id_cliente'], _ = pd.factorize(df['billing_email'])
    return df


#FUNCION GLOBAL PARA DF_NUEVO
def todas_las_funciones_nuevo(df):
    df=eliminar_columnas_df_nuevo(df)
    df=convertir_variables(df)
    df=limpiar_status(df)
    df=eliminar_pruebas(df)
    df=limpiar_email(df)
    df=asignar_id_cliente(df)
    return df


#FUNCION PARA CRAR DF_CLIENTE, OBTENEMOS LAS VARIABLES "FRECUENCIA", "RECENCIA", "GASTO TOTAL" POR ID_CLIENTE PARA HACER CLUSTER POR COMPORTAMIENTO DE COMPRA
def crear_df_cliente(df):
    df_cliente = df.copy()

    df_cliente['order_date'] = pd.to_datetime(df_cliente['order_date'])

    max_date_per_client = df_cliente.groupby('id_cliente')           ['order_date'].max().reset_index()

    df_cliente = df_cliente.merge(max_date_per_client, on='id_cliente', suffixes=('', '_max'))

    day = pd.to_datetime(df_cliente['order_date_max'].max())
    df_cliente['dias_desde_la_ultima_compra'] = df_cliente.groupby('id_cliente')['order_date'].transform(lambda x: (day - x.max()).days)

    df_cliente['numero_de_pedidos_por_cliente'] = df_cliente.groupby('id_cliente')['order_id'].transform('nunique')

    total_purchases = df_cliente['numero_de_pedidos_por_cliente'].sum()
    df_cliente['frecuencia_compras_por_cliente'] = df_cliente['numero_de_pedidos_por_cliente'] / total_purchases

    df_cliente['order_total'] = df_cliente['order_total'].astype(str) 
    df_cliente['order_total'] = df_cliente['order_total'].str.replace("'", "").astype(float)
    df_cliente['order_total'] = df_cliente['order_total'].round(2)
    df_cliente['facturacion_total_por_cliente(€)'] = df_cliente.groupby('id_cliente')['order_total'].transform('sum')
    df_cliente['facturacion_total_por_cliente(€)'] = df_cliente['facturacion_total_por_cliente(€)'].round(2)
    df_cliente['order_currency'] = df_cliente.groupby('id_cliente')['order_currency'].transform('max')

    df_cliente['billing_first_name'] = df_cliente.groupby('id_cliente')['billing_first_name'].transform('max')
    df_cliente['billing_last_name'] = df_cliente.groupby('id_cliente')['billing_last_name'].transform('max')
    df_cliente['billing_email'] = df_cliente.groupby('id_cliente')['billing_email'].transform('max')
    df_cliente['billing_address_1'] = df_cliente.groupby('id_cliente')['billing_address_1'].transform('max')
    df_cliente['billing_postcode'] = df_cliente.groupby('id_cliente')['billing_postcode'].transform('max')
    df_cliente['billing_city'] = df_cliente.groupby('id_cliente')['billing_city'].transform('max')
    df_cliente['billing_state'] = df_cliente.groupby('id_cliente')['billing_state'].transform('max')
    df_cliente['billing_country'] = df_cliente.groupby('id_cliente')['billing_country'].transform('max')
    
    df_cliente = df_cliente[['id_cliente', 'dias_desde_la_ultima_compra', 'numero_de_pedidos_por_cliente',                                                                                              'frecuencia_compras_por_cliente', 'facturacion_total_por_cliente(€)', 'order_currency',                                                                                    'billing_first_name','billing_last_name', 'billing_email', 'billing_address_1',
                             'billing_postcode', 'billing_city', 'billing_state', 'billing_country']]

    df_cliente = df_cliente.drop_duplicates(subset=['id_cliente'])
    
    df_cliente = df_cliente.reset_index(drop=True)  

    return df_cliente


#FUNCION PARA VISUALIZAR HISTOGRAMA Y BOXPLOT
def plot_histograms_and_boxplots(df, columnas_modelo, colors):
    
    # HISTOGRAMAS
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    for i, col in enumerate(columnas_modelo, start=0):
        sns.histplot(df[col], color=colors[i], kde=True, ax=axes[i])
        axes[i].set_xlabel(col, fontsize=16)
        axes[i].set_ylabel('Número de clientes', fontsize=16)

    fig.suptitle('Histogramas', fontsize=30)
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.4)
    plt.show()

    # BOXPLOT
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    for i, col in enumerate(columnas_modelo, start=0):
        sns.boxplot(x=df[col], color=colors[i], ax=axes[i])  
        axes[i].set_xlabel(col, fontsize=16)

    fig.suptitle('Box Plot', fontsize=30)
    plt.tight_layout()
    plt.subplots_adjust(hspace=0.4)
    
    plt.show()
    
    
#FUNCION PARA VISUALIZAR HEATMAP    
def plot_heatmap(df, columnas_modelo):
    plt.figure(figsize=(4, 4))

    matrix = df[columnas_modelo].corr()
    mask = np.zeros_like(matrix)
    mask[np.triu_indices_from(mask)] = True

    sns.heatmap(matrix,
                center=0,
                fmt=".3f",
                mask=mask,
                square=True,
                linewidth=0.3,
                annot=True,
                cmap='coolwarm',
                cbar_kws={"shrink": 0.8} 
                )

    plt.title('Matriz de Correlación Heatmap', fontsize=16, y=1.1)
    plt.show()

    
# FUNCION PARA VISUALIZAR MAPA GEOLOCALIZACION DE PEDIDOS POR CODIGO POSTAL
def crear_mapa(dicciona, color):
    mapa = folium.Map(location=[40.416775, -3.703790], zoom_start=6)
  
    geolocalizador = Nominatim(user_agent='geolocalizador',timeout=5)

    def obtener_coordenadas(cp):
        ubicacion = geolocalizador.geocode(f'{cp}, España')
        if ubicacion:
            return [ubicacion.latitude, ubicacion.longitude]
        else:
            return None

    for cp, pedidos in dicciona.items():
        coordenadas = obtener_coordenadas(cp)
        if coordenadas:
            # Crear círculo proporcional al número de pedidos
            folium.CircleMarker(
                location=coordenadas,
                radius=pedidos,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.6,
                popup=f'Código Postal: {cp}<br>Pedidos: {pedidos}',
            ).add_to(mapa)

    return mapa


#FUNCION PARA VISUALIZAR K-MEANS CLUSTERS SCATTER PLOT 3D 
def scatter_plot_clusters_3d(df, columnas_modelo, cluster_column, cluster_colors):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    for cluster_label in df[cluster_column].unique():
        cluster_data = df[df[cluster_column] == cluster_label]
        ax.scatter(cluster_data[columnas_modelo[0]], 
                   cluster_data[columnas_modelo[1]], 
                   cluster_data[columnas_modelo[2]],
                   label=f'Clúster {cluster_label}', color=cluster_colors[cluster_label])

    ax.legend()

    ax.set_xlabel(columnas_modelo[0])
    ax.set_ylabel(columnas_modelo[1])
    ax.set_zlabel(columnas_modelo[2], labelpad=-4)
    ax.set_title('K-MEANS Clustering - 3D Scatter Plot')

    plt.show()


#FUNCION PARA VISUALIZAR RADAR GRAPH K-MEANS CLUSTERS 
def radar_clusters(df, cluster_column, cluster_colors):
    legend_labels = [f"Clúster {i}" for i in sorted(df[cluster_column].unique())]
    features = ['dias_desde_la_ultima_compra', 'numero_de_pedidos_por_cliente', 'facturacion_total_por_cliente(€)']
    center = np.mean
    centers = df.groupby(cluster_column)[features].agg(center)
    n_clusters = len(centers)
    num_features = len(features)
    angles = np.linspace(0, 2 * np.pi, num_features, endpoint=False).tolist()
    values = centers.values.tolist()
    values += values[:1]
    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    for i in range(n_clusters):
        ax.plot(angles, values[i], linewidth=2, linestyle="solid", label=legend_labels[i], color=cluster_colors[i])

    ax.fill(angles, values[0], color=cluster_colors[0], alpha=0.25)
    for i in range(1, n_clusters):
        ax.fill(angles, values[i], alpha=0.25, color=cluster_colors[i])

    ax.set_yticklabels([])
    ax.set_xticks(angles)
    ax.set_xticklabels(features)

    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    ax.set_title('Radar Graph')
    plt.show()
    
    
#FUNCION PARA VISUALIZAR PIE CHART PROPORCION TOTAL POR CLUSTER    
def pie_chart_clusters(cluster_counts, cluster_colors):
    colors = [cluster_colors[i] for i in cluster_counts.index]

    plt.figure(figsize=(8, 8))
    plt.pie(cluster_counts.values, labels=cluster_counts.index, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.title('Distribución de Clusters')
    plt.show()
    
    
#FUNCION PARA VISUALIZAR BAR PLOT FACTURACION TOTAL POR CLUSTER    
def bar_plot_facturacion_totales_clusters(df, cluster_column, cluster_colors):
    grouped_df = df.groupby(cluster_column)['facturacion_total_por_cliente(€)'].sum().reset_index()

    fig, ax = plt.subplots(figsize=(8, 6))

    sns.barplot(x=cluster_column, y='facturacion_total_por_cliente(€)', data=grouped_df, ci='sd', capsize=0.1,
                palette=[cluster_colors[i] for i in grouped_df[cluster_column]], ax=ax)

    sns.stripplot(x=cluster_column, y='facturacion_total_por_cliente(€)', data=grouped_df, color='black', size=5,
                  jitter=True, ax=ax)

    ax.set_xlabel('KMeans Clúster')
    ax.set_ylabel('Precio Total Cliente Suma')
    ax.set_title('Bar Plot Dinero Total Facturado por Clúster')

    plt.show()