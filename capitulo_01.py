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

def delete_row(data, number):
    data = data[number:,]
    
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
                    


def ohlc_plot_candles(data, window):
    sample = data[-window:,]
    
    for i in range(len(sample)):
        
        plt.vlines(x = i, ymin=sample[i,2], ymax=sample[i,1], color='black',linewidth=1)
        
        if sample[i,3] > sample[i,0]:
            plt.vlines(x=i, ymin=sample[i,0], ymax=sample[i,3], color='green', linewidth=3)
            
        if sample[i,3] < sample[i,0]:
            plt.vlines(x=i, ymin=sample[i,3], ymax=sample[i,0], color='red', linewidth=3)
        
        if sample[i,3] == sample[i,0]:
            plt.vlines(x=i, ymin=sample[i,3], ymax=sample[i,0] + 0.0003, color='black', linewidth=1)
        plt.grid()
        
def ma(data, lookback, close, position):
    # Agrega una columna extra para almacenar la media móvil
    data = add_column(data, 1)
    
    for i in range(len(data)):
        try:
            data[i, position] = np.mean(data[i - lookback + 1:i + 1, close])
        except IndexError:
            pass
    
    # Elimina las filas iniciales donde la media móvil no se puede calcular
    data = delete_row(data, lookback - 1)
    
    return data

def smoothed_ma(data, alpha, lookback, close, position):
    
    lookback = (2*lookback) - 1 
    
    alpha = alpha/(lookback + 1 )
    
    beta = 1 - alpha
    
    data[lookback + 1 , position] = (data[lookback+1,close]*alpha) + (data[lookback,position] * beta)
    
    for i in range(lookback +2 , len(data)):
        
        try:
            data[i, position] = (data[i, close]*alpha) + (data[i-1, position]*beta)
        except IndexError:
            pass
    return data

def rsi(data, lookback, close , position):
    
    data = add_column(data, 5)
    
    for i in range(len(data)):
        data[i, position] = data[i,close] - data[i-1,close]
    
    for i in range(len(data)):
        if data[i, position] > 0:
            data[i, position +1] = data[i, position]
        elif data[i, position] < 0:
            data[position +2 ] =abs(data[i,position])
    data = smoothed_ma(data, 2, lookback,position +1 , position +3)
    data = smoothed_ma(data, 2, lookback,position +2 , position +4)
    
    data[:, position + 5] = data[:, position + 3 ] / data[:, position + 4]
    data[:, position + 6] = (100 - (100/(1+data[:,position + 5])))
    
    data = delete_row(data, position, 6)
    data = delete_row(data, lookback)
    
    return data

def signal_marubozu(data,open_column,high_column, low_column, close_column,buy_column, sell_column):
    
    data = add_column(data, 5)
    
    for i in range(len(data)):
        
        try:
            if data[i, close_column] > data[i,open_column] and data[i, high_column] == data[i,close_column] and \
                data[i, low_column] == data[i,open_column] and data[i,buy_column] == 0:
                    data[i + 1, buy_column] == 1 
            elif [i, close_column] < data[i,open_column] and data[i, high_column] == data[i,open_column] and \
                data[i, low_column] == data[i,close_column] and data[i,sell_column] == 0:
                    data[i + 1, buy_column] == -1 
        except IndexError:
            pass
    return data

def signal_Three_Candles(data, open_column, high_column, low_column, close_column, buy_column, sell_column, threshold):
    # Asegúrate de que hay suficiente espacio para nuevas columnas
    if data.shape[1] <= buy_column or data.shape[1] <= sell_column:
        data = add_column(data, max(buy_column, sell_column) - data.shape[1] + 1)
    
    # Itera a través de los datos
    for i in range(len(data) - 3):  # Ajusta el rango para evitar IndexError
        try:
            body_current = data[i, close_column] - data[i, open_column]
            body_prev1 = data[i - 1, close_column] - data[i - 1, open_column]
            body_prev2 = data[i - 2, close_column] - data[i - 2, open_column]
            
            # Verificar que los cuerpos sean similares dentro del umbral
            if abs(body_current - body_prev1) <= threshold and abs(body_prev1 - body_prev2) <= threshold:
                if body_current > 0 and data[i, close_column] > data[i - 1, close_column] > data[i - 2, close_column] > data[i - 3, close_column] and data[i, buy_column] == 0:
                    data[i + 1, buy_column] = 1
                elif body_current < 0 and data[i, close_column] < data[i - 1, close_column] < data[i - 2, close_column] < data[i - 3, close_column] and data[i, sell_column] == 0:
                    data[i + 1, sell_column] = -1
        except IndexError:
            continue
    
    return data


def signal_tasuki(data, open_column, close_column, buy_column, sell_column):
    # Asegurarse de que haya suficiente espacio para las nuevas columnas
    data = add_column(data, 5)
    
    # Iterar sobre los datos
    for i in range(2, len(data) - 1):  # Comenzar desde el tercer elemento y detenerse un elemento antes del final
        try:
            # Patrón alcista
            if data[i, close_column] < data[i, open_column] and \
               data[i, close_column] < data[i - 1, open_column] and \
               data[i, close_column] > data[i - 2, close_column] and \
               data[i - 1, close_column] > data[i - 1, open_column] and \
               data[i - 1, open_column] > data[i - 2, close_column] and \
               data[i - 2, close_column] > data[i - 2, open_column]:
                data[i + 1, buy_column] = 1

            # Patrón bajista
            elif data[i, close_column] > data[i, open_column] and \
                 data[i, close_column] > data[i - 1, open_column] and \
                 data[i, close_column] < data[i - 2, close_column] and \
                 data[i - 1, close_column] < data[i - 1, open_column] and \
                 data[i - 1, open_column] < data[i - 2, close_column] and \
                 data[i - 2, close_column] < data[i - 2, open_column]:
                data[i + 1, sell_column] = -1
        
        except IndexError:
            # Ignorar índices fuera de rango
            pass
    
    return data


def signal_three_Methods(data, open_column, high_column, low_column, close_column, buy_column, sell_column):
    # Asegurarse de que haya suficiente espacio para las nuevas columnas
    data = add_column(data, 5)
    
    # Iterar sobre los datos
    for i in range(4, len(data) - 1):  # Comenzar desde el índice 4 y detenerse un elemento antes del final
        try:
            # Patrón alcista
            if (data[i, close_column] > data[i, open_column] and
                data[i, close_column] > data[i - 4, high_column] and
                data[i, low_column] < data[i - 1, low_column] and
                data[i - 1, close_column] < data[i - 4, close_column] and
                data[i - 1, low_column] > data[i - 4, low_column] and
                data[i - 2, close_column] < data[i - 4, close_column] and
                data[i - 2, low_column] > data[i - 4, low_column] and
                data[i - 3, close_column] < data[i - 4, close_column] and
                data[i - 3, low_column] > data[i - 4, low_column] and
                data[i - 4, close_column] > data[i - 4, open_column]):
                data[i + 1, buy_column] = 1

            # Patrón bajista
            elif (data[i, close_column] < data[i, open_column] and
                  data[i, close_column] < data[i - 4, low_column] and
                  data[i, high_column] > data[i - 1, high_column] and
                  data[i - 1, close_column] > data[i - 4, close_column] and
                  data[i - 1, high_column] < data[i - 4, high_column] and
                  data[i - 2, close_column] > data[i - 4, close_column] and
                  data[i - 2, high_column] < data[i - 4, high_column] and
                  data[i - 3, close_column] > data[i - 4, close_column] and
                  data[i - 3, high_column] < data[i - 4, high_column] and
                  data[i - 4, close_column] < data[i - 4, open_column]):
                data[i + 1, sell_column] = -1

        except IndexError:
            # Ignorar índices fuera de rango
            pass

    return data

def signal_hikkake(data, open_column, high_column, low_column, close_column, buy_signal, sell_signal):
    # Asegurarse de que haya suficientes columnas para las señales
    data = add_column(data, 5)
    
    # Iterar sobre los datos, comenzando desde el índice 4 y terminando antes del final
    for i in range(4, len(data) - 1):  # Ajustado para evitar acceso fuera de rango
        try:
            # Patrón alcista
            if (data[i, close_column] > data[i - 3, high_column] and
                data[i, close_column] > data[i - 4, close_column] and
                data[i - 1, low_column] < data[i, open_column] and
                data[i - 1, close_column] < data[i, close_column] and
                data[i - 1, high_column] <= data[i - 3, high_column] and
                data[i - 2, low_column] < data[i, open_column] and
                data[i - 2, close_column] < data[i, close_column] and
                data[i - 2, high_column] <= data[i - 3, high_column] and
                data[i - 3, high_column] < data[i - 4, high_column] and
                data[i - 3, low_column] > data[i - 4, low_column] and
                data[i - 4, close_column] > data[i - 4, open_column]):
                data[i + 1, buy_signal] = 1

            # Patrón bajista
            elif (data[i, close_column] < data[i - 3, low_column] and
                  data[i, close_column] < data[i - 4, close_column] and
                  data[i - 1, high_column] > data[i, open_column] and
                  data[i - 1, close_column] > data[i, close_column] and
                  data[i - 1, low_column] >= data[i - 3, low_column] and
                  data[i - 2, high_column] > data[i, open_column] and
                  data[i - 2, close_column] > data[i, close_column] and
                  data[i - 2, low_column] >= data[i - 3, low_column] and
                  data[i - 3, low_column] > data[i - 4, low_column] and
                  data[i - 3, high_column] < data[i - 4, high_column] and
                  data[i - 4, close_column] < data[i - 4, open_column]):
                data[i + 1, sell_signal] = -1

        except IndexError:
            # Ignorar índices fuera de rango
            pass

    return data



def signal_quintuples(data, open_column, close_column, buy_column, sell_column, body_max_size):
    data = add_column(data, 5)
    for i in range(len(data)):
        try:
            # Bullish pattern
            if data[i, close_column] > data[i, open_column] and \
               data[i, close_column] > data[i - 1, close_column] and \
               (data[i, close_column] - data[i, open_column]) < body_max_size and \
               data[i - 1, close_column] > data[i - 1, open_column] and \
               data[i - 1, close_column] > data[i - 2, close_column] and \
               (data[i - 1, close_column] - data[i - 1, open_column]) < body_max_size and \
               data[i - 2, close_column] > data[i - 2, open_column] and \
               data[i - 2, close_column] > data[i - 3, close_column] and \
               (data[i - 2, close_column] - data[i - 2, open_column]) < body_max_size and \
               data[i - 3, close_column] > data[i - 3, open_column] and \
               data[i - 3, close_column] > data[i - 4, close_column] and \
               (data[i - 3, close_column] - data[i - 3, open_column]) < body_max_size and \
               data[i - 4, close_column] > data[i - 4, open_column] and \
               (data[i - 4, close_column] - data[i - 4, open_column]) < body_max_size and \
               data[i, buy_column] == 0:
                data[i + 1, buy_column] = 1
            # Bearish pattern
            elif data[i, close_column] < data[i, open_column] and \
                 data[i, close_column] < data[i - 1, close_column] and \
                 (data[i, open_column] - data[i, close_column]) < body_max_size and \
                 data[i - 1, close_column] < data[i - 1, open_column] and \
                 data[i - 1, close_column] < data[i - 2, close_column] and \
                 (data[i - 1, open_column] - data[i - 1, close_column]) < body_max_size and \
                 data[i - 2, close_column] < data[i - 2, open_column] and \
                 data[i - 2, close_column] < data[i - 3, close_column] and \
                 (data[i - 2, open_column] - data[i - 2, close_column]) < body_max_size and \
                 data[i - 3, close_column] < data[i - 3, open_column] and \
                 data[i - 3, close_column] < data[i - 4, close_column] and \
                 (data[i - 3, open_column] - data[i - 3, close_column]) < body_max_size and \
                 data[i - 4, close_column] < data[i - 4, open_column] and \
                 (data[i - 4, open_column] - data[i - 4, close_column]) < body_max_size and \
                 data[i, sell_column] == 0:
                data[i + 1, sell_column] = -1
        except IndexError:
            pass
    return data



def atr(data, lookback, high_column, low_column, close_column, position):
    # Añadir una columna para almacenar el ATR
    data = add_column(data, 1)
    
    # Calcular el rango verdadero para cada fila
    for i in range(len(data)):
        try:
            # Calcular el rango verdadero
            data[i, position] = max(
                data[i, high_column] - data[i, low_column],  # Rango de hoy
                abs(data[i, high_column] - data[i - 1, close_column]),  # Alto de hoy menos cierre de ayer
                abs(data[i, low_column] - data[i - 1, close_column])   # Bajo de hoy menos cierre de ayer
            )
        except ValueError:
            pass
    
    # Inicializar el primer valor del ATR
    data[0, position] = 0
    
    # Aplicar un promedio móvil suavizado al ATR
    data = smoothed_ma(data, 2, lookback, position, position + 1)
    
    # Eliminar la columna temporal utilizada para el cálculo
    data = delete_column(data, position, 1)
    
    # Eliminar las filas que no tienen suficientes datos para el ATR completo
    data = delete_row(data, lookback)
    
    return data

def signal_double_trouble(data, open_column, high_column, low_column, close_column,
           atr_column, buy_column, sell_column):
    # Asegúrate de añadir una columna extra para las señales de compra/venta
    data = add_column(data, 5)  
    
    for i in range(len(data)):
        try:
            # Verificación para evitar acceso a índices negativos
            if i >= 1 and i < len(data):
                # Patrón alcista
                if data[i, close_column] > data[i, open_column] and \
                   data[i, close_column] > data[i - 1, close_column] and \
                   data[i - 1, close_column] > data[i - 1, open_column] and \
                   data[i, high_column] - data[i, low_column] > (2 * data[i - 1, atr_column]) and \
                   data[i, close_column] - data[i, open_column] > data[i - 1, close_column] - data[i - 1, open_column] and \
                   data[i, buy_column] == 0:
                    data[i + 1, buy_column] = 1
                
                # Patrón bajista
                elif data[i, close_column] < data[i, open_column] and \
                     data[i, close_column] < data[i - 1, close_column] and \
                     data[i - 1, close_column] < data[i - 1, open_column] and \
                     data[i, high_column] - data[i, low_column] > (2 * data[i - 1, atr_column]) and \
                     data[i, open_column] - data[i, close_column] > data[i - 1, open_column] - data[i - 1, close_column] and \
                     data[i, sell_column] == 0:
                    data[i + 1, sell_column] = -1

        except IndexError:
            # Captura cualquier error de índice, posiblemente causado por el acceso a datos fuera de rango
            pass

    return data

def signal_double_trouble_atr_threshold(data, open_column, high_column, low_column, close_column,
           atr_column, buy_column, sell_column, atr_threshold):
    data = add_column(data, 5)
    
    for i in range(len(data)):
        try:
            # Bullish pattern
            if data[i, close_column] > data[i, open_column] and \
               data[i, close_column] > data[i - 1, close_column] and \
               data[i - 1, close_column] > data[i - 1, open_column] and \
               data[i, high_column] - data[i, low_column] > (2 * data[i - 1, atr_column]) and \
               data[i, close_column] - data[i, open_column] > data[i - 1, close_column] - data[i - 1, open_column] and \
               data[i - 1, atr_column] > atr_threshold and \
               data[i, buy_column] == 0:
                data[i + 1, buy_column] = 1

            # Bearish pattern
            elif data[i, close_column] < data[i, open_column] and \
                 data[i, close_column] < data[i - 1, close_column] and \
                 data[i - 1, close_column] < data[i - 1, open_column] and \
                 data[i, high_column] - data[i, low_column] > (2 * data[i - 1, atr_column]) and \
                 data[i, open_column] - data[i, close_column] > data[i - 1, open_column] - data[i - 1, close_column] and \
                 data[i - 1, atr_column] > atr_threshold and \
                 data[i, sell_column] == 0:
                data[i + 1, sell_column] = -1
        except IndexError:
            pass
    
    return data



























