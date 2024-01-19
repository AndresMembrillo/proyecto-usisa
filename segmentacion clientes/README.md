# PROYECTO USISA - SEGMENTACIÓN DE CLIENTES
Proyectos como freelance  para la tienda online de Union Salazonera Isleña, S.A. (USISA),  empresa de conservas de pescado más grande de Andalucia.

![usisa_barco](https://github.com/AndresMembrillo/proyecto-usisa/assets/145653361/d019eb2f-299d-4f14-b5c2-a1bae1c6bb58)

## Datos
La empresa nos ha suministrado todos los datos disponibles de la tienda online de USISA (www.usisa.com). Es importante señalar que, debido a las normativas de protección de datos, no hemos podido cargar los archivos que contienen dicha información.

## Objetivo 
El objetivo del proyecto es la segmentación de clientes, diferenciar y agrupar a los clientes de la tienda online según su comportamiento de compra. Con los datos existententes se pueden obtener las siguientes variables:

- `Frecuencia de compra`: Se refiere a la medición del número total de pedidos realizados por un cliente en la tienda online de USISA. 

- `Recencia de compra`: Implica el análisis de los días transcurridos desde el último pedido efectuado por un cliente en la tienda online de USISA.

- `Gasto Total`: Se refiere al monto total (en euros) gastado por un cliente en todos sus pedidos realizados en la tienda online de USISA.

## EDA

![EDA_clustering](https://github.com/AndresMembrillo/proyecto-usisa/assets/145653361/22cefa6b-f4d0-4541-ada2-d854a24b56e2)

## Modelo K-MEANS
Para la segmentación de clientes por comportamiento de compra, necesitamos un modelo de aprendizaje no supervisado ya que carecemos de la variable objetivo, que en nuestro caso sería el grupo o segmento que se asigna a cada cliente.

Para ello vamos a comparar dos modelos de clustering, K-Means y DBSCAN. Después de visualizar los clusters, estudiar las métricas de cada modelo, aplicamos el más eficiente: `K-MEANS`

![cluster_clientes](https://github.com/AndresMembrillo/proyecto-usisa/assets/145653361/50e9c32a-9591-4dca-bfa2-ec08dbee9a7e)

Se agrupan los clientes por sus respectivos clusters y se obtiene el centro de cada cluster usando la media para ver las características que mejor explican cada grupo. 

- `Clúster 0`: su última compra fue hace mucho, promedian tan solo un pedido y es el grupo que menos dinero gasta. Corresponde al 54% de los clientes. El clúster 0 lo etiquetamos como clientes perdidos

- `Clúster 1`: se observa que la última compra de este grupo ha sido muy reciente, promedian tan solo un pedido y gasta moderadamente. Comprende el 22% aproximadamente del total de clientes. El clúster 1 lo etiquetamos  como clientes nuevos.

- `Clúster 2`: su última compra ha sido hace relativamente poco, es el grupo que más pedidos promedia y que más gasta prácticamente cuadruplicando los demás. Se trata del 24% de los clientes. El clúster 2  lo etiquetamos como clientes fieles.

También graficamos un mapa de España por cada cluster, con la geolocalización donde se aprecian dónde están los mayores volúmenes de pedidos de cada cluster según su código postal. A continuación se visualiza el mapa del cluster 2, etiquetado como el grupo de los clientes fieles

![cluster2](https://github.com/AndresMembrillo/proyecto-usisa/assets/145653361/bf86ea3b-d3a6-468b-bde4-2583e810ac5c)


  nota: estos graficos de la libreria folium son dinamicos y no se pueden visualizar en GitHub.

## Conclusión
Hemos segmentado los clientes y sabemos donde se localiza cada grupo, esta información junto a los datos del cliente (correo electrónico) es de gran valor para una campaña de marketing.
