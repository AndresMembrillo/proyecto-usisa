# PROYECTO USISA - PREDICCIÓN DE VENTAS
Proyectos como freelance  para la tienda online de Union Salazonera Isleña, S.A. (USISA),  empresa de conservas de pescado más grande de Andalucia.

![usisa_barco](https://github.com/AndresMembrillo/proyecto-usisa/assets/145653361/d019eb2f-299d-4f14-b5c2-a1bae1c6bb58)

## Datos
La empresa nos ha suministrado todos los datos disponibles de la tienda online de USISA (www.usisa.com). Es importante señalar que, debido a las normativas de protección de datos, no hemos podido cargar los archivos que contienen dicha información.

## Objetivo 
El objetivo del proyecto consiste en realizar una predicción de las ventas de la tienda online de USISA, abordando tanto el número de pedidos como la facturación total. Con los datos existententes se pueden obtener las siguientes variables:

- `Total pedidos`: Esta métrica refleja el número global de pedidos efectuados diariamente en la tienda online de USISA. 

- `Total Facturación`: Esta variable se expresa en euros (€) y representa la suma total de ingresos generados a través de los pedidos realizados diariamente en la tienda online de USISA.

- `Fecha`: Indicador temporal que registra la fecha asociada a cada medición.

En cuanto a la duración del pronóstico futuro estará condicionada por el modelo seleccionado; en otras palabras, determinaremos el horizonte temporal que ofrezca los mejores resultados. Es importante tener en cuenta que a medida que aumentamos la cantidad de intervalos de tiempo pronosticados es probable que también incremente el margen de error. Por lo tanto, se buscará un equilibrio para lograr predicciones precisas sin comprometer la fiabilidad del modelo.

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

## Conclusión
Hemos segmentado los clientes y sabemos donde se localiza cada grupo, esta información junto a los datos del cliente (correo electrónico) es de gran valor para una campaña de marketing.
