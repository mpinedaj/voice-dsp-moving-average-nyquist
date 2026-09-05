import numpy as np
import sounddevice as sd
 
# Ecuación: y(n) = sum_{k=0}^{M-1} (1/M) * x(n - k)
def filtro_media_movil_matematico(x, M):
    N = len(x)
    y = np.zeros(N)
 
    for n in range(N):
        suma_acumulada = 0.0
        for k in range(M):
            if n - k >= 0:
                suma_acumulada += x[n - k]
        y[n] = (1.0 / M) * suma_acumulada
 
    return y
 
 
def grabar_audio(duracion=3.0, fs_original=44100):
    audio_raw = sd.rec(int(duracion * fs_original), samplerate=fs_original, channels=1, dtype='float32')
    sd.wait()
    return audio_raw.flatten()
 
 
def aplicar_filtro_media_movil(x_entrada, M_puntos):
    M_puntos = int(M_puntos)
    if M_puntos < 1:
        raise ValueError("M debe ser un entero mayor o igual a 1.")
    return filtro_media_movil_matematico(x_entrada, M_puntos)
 
 
def verificar_criterio_nyquist(senal, fs_original, fs_deseada, fs_max_senal=4000.0):
    if fs_deseada <= 0:
        raise ValueError("La frecuencia deseada debe ser mayor a 0 Hz.")
 
    fs_deseada = min(fs_deseada, fs_original)
 
    paso = max(1, int(round(fs_original / fs_deseada)))
    senal_remuestreada = senal[::paso]
    fs_real = fs_original / paso
 
    cumple_nyquist = fs_real >= (2 * fs_max_senal)
 
    return senal_remuestreada, fs_real, cumple_nyquist