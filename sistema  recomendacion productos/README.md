# PROYECTO USISA - SISTEMA DE RECOMENDACIÓN DE PRODUCTOS
Proyectos como freelance para la tienda online de Unión Salazonera Isleña, S.A. (USISA),  empresa de conservas de pescado más grande de Andalucía.

![usisa_barco](https://github.com/AndresMembrillo/proyecto-usisa/assets/145653361/d019eb2f-299d-4f14-b5c2-a1bae1c6bb58)

## Datos
La empresa nos ha suministrado todos los datos disponibles de la tienda online de USISA (www.usisa.com). Es importante señalar que, debido a las normativas de protección de datos, no hemos podido cargar los archivos que contienen dicha información.

## Objetivo 
El propósito central de este proyecto reside en desarrollar un sistema de recomendación de productos para la tienda online de USISA. Con los datos existententes se pueden obtener las siguientes variables:

- `Identificador de pedido`: gracias al identificador del pedido podemos agrupar todos los productos comprados en cada pedido.

- `Identificador de producto`: hay 110 productos registrados con distinto identificador

La esencia del sistema de recomendación se fundamenta en la capacidad de aprovechar la información derivada de las compras anteriores. Este sistema tiene como objetivo principal prever y sugerir productos a los usuarios, basándose en la similitud de sus patrones de compra con otros usuarios. La premisa fundamental es analizar y comprender las elecciones y preferencias pasadas de los usuarios para anticipar sus necesidades futuras, proporcionándoles recomendaciones personalizadas que mejoren significativamente su experiencia de compra en la plataforma. La similitud en los patrones de compra entre usuarios se convierte así en la piedra angular para ofrecer sugerencias relevantes y adaptadas a cada individuo, impulsando así la eficacia y la utilidad del sistema de recomendación en la tienda online.

## EDA
Se visualiza un box-plot de la distribución de las cantidades vendidas por productos diferentes y también se visualizan 5 gráficos de barras que clasifican los 110 productos registrados en el sistema,  de los más vendidos a los menos vendidos. A cointinuación se visualiza el top 10:

![top10](https://github.com/AndresMembrillo/proyecto-usisa/assets/145653361/5852bf54-c3e9-4925-90c4-a6592fcac7bf)

## Modelo
Pasos:

- `Preprocesamiento de datos`: Se utiliza TransactionEncoder para convertir la lista de productos en una matriz binaria (one-hot encoding).
- `Algoritmo Apriori`: El algoritmo Apriori se utiliza para descubrir conjuntos de productos que aparecen con frecuencia juntos en los pedidos.
- `Reglas de asociación`: A partir de los conjuntos frecuentes encontrados con Apriori, se generan reglas de asociación para capturar patrones de compra.

Estos dos pasos son cruciales para la generación de recomendaciones, ya que el algoritmo Apriori y las reglas de asociación permiten identificar patrones de compra comunes. Estos patrones se utilizan luego para sugerir productos adicionales que tienen una alta probabilidad de ser comprados junto con los productos de un pedido dado, contribuyendo así a un sistema de recomendación efectivo

## Generación de recomendaciones para el conjunto de prueba y para un nuevo pedido

Se usan unos pocos pedidos de los datos como test, para probar el sistema de recomendación:

![Captura de pantalla 2024-01-29 123935](https://github.com/AndresMembrillo/proyecto-usisa/assets/145653361/250df9bc-7c3a-4e75-8f83-0927bc96e334)

También se muestra un ejemplo de cómo obtener recomendaciones para un nuevo pedido específico:

 ![recomendacion nuevo](https://github.com/AndresMembrillo/proyecto-usisa/assets/145653361/01196fe9-5eb0-41f6-b189-da30a1bc0071)

## Conclusión
En el desarrollo de este proyecto, hemos logrado implementar un robusto sistema de recomendación para la tienda online de USISA, utilizando datos de compras pasadas y reglas de asociación. Sin embargo, identificamos una oportunidad clave para mejorar aún más la precisión y personalización de nuestras recomendaciones. La incorporación de ratings específicos para cada producto permitiría usar otros modelos de recomendación y ofrecer sugerencias más ajustadas a las preferencias individuales de los usuarios, enriqueciendo significativamente la experiencia de compra.
