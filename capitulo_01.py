import datetime
import pytz
import pandas as pd
import MetaTrader5 as mt5
import numpy as np
import matplotlib.pyplot as plt
import sys

# Inicializar MetaTrader 5
if not mt5.initialize():
    print("Error al inicializar MetaTrader 5, error code =", mt5.last_error())
    sys.exit()

# Verificar que el símbolo está disponible
symbol = 'EURUSD'
if not mt5.symbol_select(symbol, True):
    print(f"Símbolo {symbol} no encontrado o no disponible.")
    mt5.shutdown()
    sys.exit()

# Definición de los timeframes
frame_H1 = mt5.TIMEFRAME_H1

def get_quotes(time_frame, year=2024, month=1, day=1, asset='EURUSD'):
    timezone = pytz.timezone('Etc/UTC')
    time_from = datetime.datetime(2023, 1, 10, tzinfo=timezone)
    time_to = datetime.datetime(2024, 2, 10, tzinfo=timezone) # Fecha actual en UTC
    print('adui',datetime.datetime.now(timezone))
    print('ui',time_to)
    print(f"Obteniendo datos desde {time_from} hasta {time_to} para el activo {asset} en el marco de tiempo {time_frame}")

    rates = mt5.copy_rates_range(asset, time_frame, time_from, time_to)
    if rates is None or len(rates) == 0:
        print(f"No se pudo obtener datos para el activo: {asset}. Error: {mt5.last_error()}")
        return None

    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    return rates_frame

def mass_import(asset, time_frame):
    data = None
    if time_frame == 'H1':
        data = get_quotes(frame_H1, 2013, 1, 1, asset=asset)
    if data is not None:
        data = data.iloc[:, 1:5]  # Seleccionar columnas relevantes (open, high, low, close)
        data = data.round(decimals=5)
    return data

def add_column(data, times):
    for i in range(times):
        new = np.zeros((len(data), 1), dtype=float)
        data = np.append(data, new, axis=1)
    return data

def signal(data):
    data = add_column(data, 2)
    for i in range(len(data)):
        try:
            # Bullish Alpha
            if data[i, 2] < data[i - 5, 2] and data[i, 2] < data[i - 13, 2] and data[i, 2] > data[i - 21, 2] and data[i, 3] > data[i - 1, 3] and data[i, 4] == 0:
                data[i + 1, 4] = 1
            # Bearish Alpha
            elif data[i, 1] > data[i - 5, 1] and data[i, 1] > data[i - 13, 1] and data[i, 1] < data[i - 21, 1] and data[i, 3] < data[i - 1, 3] and data[i, 5] == 0:
                data[i + 1, 5] = -1
        except IndexError:
            pass
    return data

def ohlc_plot_bars(data, window, ax):
    sample = data[-window:, :]
    for i in range(len(sample)):
        ax.vlines(x=i, ymin=sample[i, 2], ymax=sample[i, 1], color='black', linewidth=1)
        if sample[i, 3] > sample[i, 0]:
            ax.vlines(x=i, ymin=sample[i, 0], ymax=sample[i, 3], color='black', linewidth=1)
        elif sample[i, 3] < sample[i, 0]:
            ax.vlines(x=i, ymin=sample[i, 3], ymax=sample[i, 0], color='black', linewidth=1)
        else:
            ax.vlines(x=i, ymin=sample[i, 3], ymax=sample[i, 0] + 0.0003, color='black', linewidth=1)
    ax.grid()

def signal_chart(data, position, buy_column, sell_column, window=500):
    sample = data[-window:,]
    print("Shape of sample:", sample.shape)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    
    ohlc_plot_bars(data, window, ax)
    
    num_columns = sample.shape[1]
    print(f"Number of columns in sample: {num_columns}")
    
    for i in range(len(sample)):
        if sample[i, buy_column] == 1:
           # print(f'Compra en índice {i}')
            x = i
            y = sample[i, position]
            ax.annotate('', xy=(x, y), xytext=(x, y),
                        arrowprops=dict(width=1, headlength=10, headwidth=10, facecolor='green', edgecolor='green'))
        if sample[i, sell_column] == -1:
            #print(f'Venta en índice {i}')
            x = i
            y = sample[i, position]
            ax.annotate('', xy=(x, y), xytext=(x, y),
                        arrowprops=dict(width=1, headlength=10, headwidth=10, facecolor='red', edgecolor='red'))
 
    plt.show()


def performance(data, open_price, buy_column, sell_column, long_result_col, short_result_col):
    # Itera sobre las filas para calcular el rendimiento de las posiciones largas
    for i in range(len(data)):
        try:
            if data[i, buy_column] == 1:
                for a in range(i+1, min(i+1000, len(data))):
                    if data[a, buy_column] == 1 or data[a, sell_column] == -1:
                        data[a, long_result_col] = data[a, open_price] - data[i, open_price]
                        break
        except IndexError:
            pass

    # Itera sobre las filas para calcular el rendimiento de las posiciones cortas
    for i in range(len(data)):
        try:
            if data[i, sell_column] == -1:
                for a in range(i+1, min(i+1000, len(data))):
                    if data[a, buy_column] == 1 or data[a, sell_column] == -1:
                        data[a, short_result_col] = data[i, open_price] - data[a, open_price]
                        break
        except IndexError:
            pass
                    


# Ejemplo de uso
horizon = 'H1'
asset = 'USDJPY'
mydata = mass_import(asset, horizon)
mydata = signal(mydata)

# Verificar si las señales se han generado correctamente
print(mydata[-50:])  # Imprimir las últimas filas para verificar las señales

signal_chart(mydata, 3, 4, 5, window=500)  # Cambiar `position` a 3 para usar la columna 'close'

