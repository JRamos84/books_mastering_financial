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
frame_M15 = mt5.TIMEFRAME_M15
frame_M30 = mt5.TIMEFRAME_M30
frame_H1 = mt5.TIMEFRAME_H1
frame_H4 = mt5.TIMEFRAME_H4
frame_D1 = mt5.TIMEFRAME_D1
frame_W1 = mt5.TIMEFRAME_W1
frame_M1 = mt5.TIMEFRAME_MN1
frame_M5 = mt5.TIMEFRAME_M5

def get_quotes(time_frame, year=2024, month=1, day=1, asset='EURUSD'):
    timezone = pytz.timezone('Etc/UTC')
    time_from = datetime.datetime(2024, 1, 10, tzinfo=timezone)
    time_to = datetime.datetime(2024, 2,10,  tzinfo=timezone) # Fecha actual en UTC
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
    elif time_frame == 'D1':
        data = get_quotes(frame_D1, 2000, 1, 1, asset=asset)
    elif time_frame == 'M5':
        data = get_quotes(frame_M5, 2000, 1, 1, asset=asset)

    if data is not None:
        data = data.iloc[:, 1:5]  # Seleccionar columnas relevantes
        data = data.round(decimals=5)

    return data

def add_column(data, times):
    for i in range(times):
        new = np.zeros((len(data), 1), dtype=float)
        data = np.append(data, new, axis=1)
    return data

def delete_column(data, index, times):
    for i in range(times):
        data = np.delete(data, index, axis=1)
    return data

def add_row(data, times):
    for i in range(times):
        columns = np.shape(data)[1]
        new = np.zeros((1, columns), dtype=float)
        data = np.append(data, new, axis=0)
    return data

def delete_row(data, number):
    return data[number:,]

def rounding(data, how_far):
    return data.round(decimals=how_far)

def signal(data):
    data = add_column(data, 5)
    for i in range(len(data)):
        try:
            if data[i, 2] < data[i - 5, 2] and data[i, 2] < data[i - 13, 2] and data[i, 2] > data[i - 21, 2] and data[i, 3] > data[i - 1, 3] and data[i, 4] == 0:
                data[i + 1, 4] = 1
            elif data[i, 1] > data[i - 5, 1] and data[i, 1] > data[i - 13, 1] and data[i, 1] < data[i - 21, 1] and data[i, 3] < data[i - 1, 3] and data[i, 5] == 0:
                data[i + 1, 5] = -1
        except IndexError:
            pass
    return data

def ohlc_plot_bars(data, window):
    sample = data[-window:, :]
    for i in range(len(sample)):
        plt.vlines(x=i, ymin=sample[i, 2], ymax=sample[i, 1], color='black', linewidth=1)
        if sample[i, 3] > sample[i, 0]:
            plt.vlines(x=i, ymin=sample[i, 0], ymax=sample[i, 3], color='black', linewidth=1)
        elif sample[i, 3] < sample[i, 0]:
            plt.vlines(x=i, ymin=sample[i, 3], ymax=sample[i, 0], color='black', linewidth=1)
        else:
            plt.vlines(x=i, ymin=sample[i, 3], ymax=sample[i, 0] + 0.0003, color='black', linewidth=1)
    plt.grid()
    plt.show()

# Ejemplo de uso

# Paso 1: Importar datos
asset = 'USDJPY'
time_frame = 'M5'
data = mass_import(asset, time_frame)

if data is not None:
    # Convertir DataFrame a numpy array
    data_array = data.to_numpy()

    # Paso 2: Generar señales
    data_with_signals = signal(data_array)

    # Paso 3: Plotear datos OHLC con señales
    ohlc_plot_bars(data_with_signals, window=100)
else:
    print("No se pudieron obtener datos para el análisis.")

# Finalizar conexión a MetaTrader 5
mt5.shutdown()
