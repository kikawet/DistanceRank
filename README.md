# DistanceRank
Implementación del algoritmo Distance Rank y Scrapy Crawler

## Instalación
Ejecutar dentro de la carpeta del proyecto
```
pip install -r requirements.txt
```

## Ejecución
### 1. Generar matriz sociométrica
Dentro de la carpeta `src` ejecutar:
```
 python -m scrapy.cmdline runspider crawler.py -a output=.. -a max_urls=5
```
 Donde **max_urls** es el número de urls que se recogerán.
 
### 2. Ejecutar el algoritmo
Dentro de la carpeta ***src*** ejecutar:
```
python main.py
```


