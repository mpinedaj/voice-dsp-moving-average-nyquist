import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

# ALGORITMO MATEMÁTICO: FILTRO DE MEDIA MÓVIL (PEINE)
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

# PARTE 1: ADQUISICIÓN DE VOZ Y ATENUACIÓN DE RUIDO BLANCO
fs_original = 44100  
duracion = 3.0       

print("Grabando señal de voz con ruido de fondo... (3 segundos)")
audio_raw = sd.rec(int(duracion * fs_original), samplerate=fs_original, channels=1, dtype='float32')
sd.wait()
x_entrada = audio_raw.flatten()

ruido_blanco = np.random.normal(0, 0.02, size=len(x_entrada))
x_ruidosa = x_entrada + ruido_blanco

M_puntos = 15
y_filtrada = filtro_media_movil_matematico(x_ruidosa, M_puntos)

t = np.linspace(0, duracion, len(x_ruidosa))
muestras_ver = 1000 

plt.figure(figsize=(10, 4))
plt.plot(t[:muestras_ver], x_ruidosa[:muestras_ver], label='Entrada ruidosa $x(n)$', alpha=0.5, color='gray')
plt.plot(t[:muestras_ver], y_filtrada[:muestras_ver], label=f'Salida filtrada $y(n)$ ($M={M_puntos}$)', color='blue', linewidth=1.2)
plt.title('Filtrado por Media Móvil: $y(n) = \\sum_{k=0}^{M-1} \\frac{1}{M} x(n-k)$')
plt.xlabel('Tiempo $t = nT$ [s]')
plt.ylabel('Amplitud')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

print("Reproduciendo señal sin filtrar...")
sd.play(x_ruidosa, fs_original)
sd.wait()

print("Reproduciendo señal filtrada...")
sd.play(y_filtrada, fs_original)
sd.wait()

# PARTE 2: VERIFICACIÓN EXPERIMENTAL DEL CRITERIO DE NYQUIST
# Criterio: fs >= 2 * f_max (Pérdida de información si fs < fs_nyquist)

fs_cumple = 16000  
paso_cumple = int(fs_original / fs_cumple)
x_nyquist_ok = y_filtrada[::paso_cumple]

fs_incumple = 2500 
paso_incumple = int(fs_original / fs_incumple)
x_nyquist_fail = y_filtrada[::paso_incumple]

print(f"\n[Nyquist OK] Reproduciendo a fs = {fs_cumple} Hz (Voz clara)...")
sd.play(x_nyquist_ok, fs_cumple)
sd.wait()

print(f"[Nyquist FAIL] Reproduciendo a fs = {fs_incumple} Hz (Voz distorsionada por Aliasing)...")
sd.play(x_nyquist_fail, fs_incumple)
sd.wait()