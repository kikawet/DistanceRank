# DistanceRank
 Implementación del algoritmo Distance Rank y Scrapy Crawler
 ## Prerequisitos
   Instalar [Python 3.7.4](https://www.python.org/downloads/release/python-374/)
   
 ## Instalación
      
   Descarga el proyecto y ejecuta dentro de la carpeta del proyecto
  ```
     pip install -r requirements.txt
  ```

## Ejecución
 Dentro de la carpeta ***src*** ejecutar:
   ### 1. Generar matriz sociométrica
   ```
      python -m scrapy.cmdline runspider crawler.py -a output=.. -a max_urls=5
   ```
   Donde **max_urls** es el número de urls que se recogerán.
 
   ### 2. Ejecutar el algoritmo
   ```
      python main.py
   ```


