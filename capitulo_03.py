# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 06:57:51 2024

@author: joseph
"""


from capitulo_01 import mass_import, signal, signal_chart,ohlc_plot_candles, ma
import matplotlib.pyplot as plt

# Ejemplo de uso
horizon = 'H1'
asset = 'USDJPY'
mydata = mass_import(asset, horizon)
mydata = signal(mydata)

# Calculo de ma

#lookback = 30
#close_column = 3
#ma_column = 4

#mydata = ma(mydata, lookback, close_column, ma_column)

#ohlc_plot_candles(mydata, window=100)



#mydata = signal(mydata)

# Verificar si las señales se han generado correctamente
#print(mydata[-50:])  # Imprimir las últimas filas para verificar las señales

#signal_chart(mydata, 3, 4, 5, window=500)  # Cambiar `position` a 3 para usar la columna 'close'

