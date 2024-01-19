# PROYECTO USISA - PREDICCIÓN DE VENTAS
Proyectos como freelance  para la tienda online de Unión Salazonera Isleña, S.A. (USISA),  empresa de conservas de pescado más grande de Andalucía.

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

El archivo con nombre `1_EDA-timeseries_diario.ipynb` recoge los datos con frecuencia diaria y visualiza los siguientes gráficos:

- `Gráifcos de time series`.
- `Descomposición: Tendencia, estacionalidad y ruido`.
- `Graficos de autocorrelación y autocorrelación parcial.`

## Modelo time series

Para llevar a cabo la predicción futura, construimos un modelo de aprendizaje supervisado abordando los siguientes puntos clave:

- `Frecuencia de Datos`: Después de probar con frecuencia diaria y semanal, optamos por una frecuencia mensual, ya que nuestro modelo ofrece mejores resultados con esta configuración.
- `Proporción de Datos en Train y Test`: Seleccionamos los últimos 3 meses como conjunto de prueba y el resto para entrenamiento. Esta proporción demostró ser la más efectiva, proporcionando las métricas más sólidas para la generalización del modelo.
- `Horizonte de Predicción`: Elegimos una frecuencia mensual y un horizonte de predicción de 3 meses, alineado con la muestra utilizada en el conjunto de prueba. Es esencial tener en cuenta que, a medida que aumentamos el horizonte de predicción, el error tiende a acumularse, siendo el último mes menos fiable.

## Modelo AutoARIMA
Después de probar varios modelos de time series (RandomForestRegressor, XGBoostRegressor, ARIMA…). El archivo con nombre: `2_modelo_AutoARIMA.ipynb` contiende un modelo AutoARIMA que selecciona automáticamente los mejores parámetros para el modelo ARIMA, es el que mejores resultados me ha dado. 

Pero debido a la poca cantidad de datos que teniamos, los resultados de las metricas no nos convencian y decidimos hacer uso de la siguiente libreria:

## pycaret.time_series.TSForecastingExperiment
Usaremos los datos de la facturación mensual en euros para explicar las tareas que realiza la libreria de pycaret:

- Visualiza los datos originales:
  ![original](https://github.com/AndresMembrillo/proyecto-usisa/assets/145653361/249f60e6-18a0-435e-945c-4cc46eaf0a40)
  
- Separa los datos en train y test:
  ![train_test](https://github.com/AndresMembrillo/proyecto-usisa/assets/145653361/c83ac201-67be-43cf-aceb-65fde0afb199)
  
- Evalúa todos los modelos de series temporales y los clasifica según su rendimiento. Seleccionamos los 4 mejores modelos:
  ![clasificacion](https://github.com/AndresMembrillo/proyecto-usisa/assets/145653361/2ceece91-4e9e-435b-9d63-171788ba6325)
  
- Realiza un ajuste adicional de los parámetros para los modelos seleccionados:
  ![Tuneado](https://github.com/AndresMembrillo/proyecto-usisa/assets/145653361/7603d07c-7ad6-4dd1-b43b-619d8368b969)
  
- Combina los mejores modelos para obtener un modelo mixto.
  ![blended](https://github.com/AndresMembrillo/proyecto-usisa/assets/145653361/fba90b80-648a-43d3-aa87-a3befe896d44)
  
- Realiza predicciones del modelo mixto en el conjunto de pruebas y proyecciones futuras.
  ![forecast](https://github.com/AndresMembrillo/proyecto-usisa/assets/145653361/c7854303-e32f-4aa9-a140-70479d5f2309)
nota: estos graficos son dinamicos y no se pueden visualizar en GitHub, los graficos de los archivos `1_EDA-timeseries_diario.ipynb` y `2_modelo_AutoARIMA.ipynb` si se pueden visualizar en GitHub.

## Conclusión
El objetivo principal se ha alcanzado de manera parcial. A pesar de la limitada cantidad de datos disponibles, hemos logrado desarrollar un sólido modelo de predicción para la facturación mensual a corto plazo. Sin embargo, en contraste, el modelo de predicción de pedidos mensuales no ha arrojado resultados favorables.

En resumen, hemos logrado desarrollar un modelo de forecasting capaz de realizar predicciones fiables para la facturación de uno o dos meses. No obstante, es importante señalar que a medida que intentamos predecir un mayor número de meses, se observa un aumento progresivo en el error.

