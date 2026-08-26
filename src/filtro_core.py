import numpy as np
import sounddevice as sd

# Ecuación: y(n) = sum_{k=0}^{M-1} (1/M) * x(n - k)
def filtro_media_movil_matematico(x, M):
    N = len(x)
    y = np.zeros(N)
    
    for n in range(N):
        suma_acumulada = 0.0
        for k in range(M):
            if n - k >= 0:  # Condición de causalidad t_x <= t_y
                suma_acumulada += x[n - k]
        y[n] = (1.0 / M) * suma_acumulada
        
    return y

def grabar_y_procesar(duracion=3.0, fs_original=44100, M_puntos=15):
    # Grabación
    audio_raw = sd.rec(int(duracion * fs_original), samplerate=fs_original, channels=1, dtype='float32')
    sd.wait()
    x_entrada = audio_raw.flatten()
    
    # Filtrado con el algoritmo matemático
    y_filtrada = filtro_media_movil_matematico(x_entrada, M_puntos)
    
    # Verificación Criterio de Nyquist
    # Cumple
    fs_cumple = 16000  
    paso_cumple = int(fs_original / fs_cumple)
    x_nyquist_ok = y_filtrada[::paso_cumple]
    fs_real_ok = fs_original / paso_cumple 
    
    # Falla
    fs_incumple = 2500 
    paso_incumple = int(fs_original / fs_incumple)
    x_nyquist_fail = y_filtrada[::paso_incumple]
    fs_real_fail = fs_original / paso_incumple 
    
    return {
        'fs_original': fs_original,
        'x_entrada': x_entrada,
        'y_filtrada': y_filtrada,
        'fs_real_ok': fs_real_ok,
        'x_nyquist_ok': x_nyquist_ok,
        'fs_real_fail': fs_real_fail,
        'x_nyquist_fail': x_nyquist_fail
    }