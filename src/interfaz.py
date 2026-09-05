import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np
 
from filtro_core import (
    grabar_audio,
    aplicar_filtro_media_movil,
    verificar_criterio_nyquist,
)
 
class InterfazLaboratorio:
    def __init__(self, root):
        self.root = root
        self.root.title("Laboratorio 1: Procesamiento de Señales")
        self.root.geometry("440x560")
 
        # Estado interno
        self.fs_original = 44100
        self.x_entrada = None      # señal cruda grabada
        self.y_filtrada = None     # señal luego de aplicar el filtro
        self.x_nyquist = None      # última señal re-muestreada
        self.fs_nyquist_real = None
 
        tk.Label(root, text="Filtro de Media Móvil", font=("Arial", 14, "bold")).pack(pady=10)
 
        # --- Paso 1: Grabación ---
        self.btn_grabar = tk.Button(root, text="1. Grabar Voz (3s)", command=self.ejecutar_grabacion,
                                     bg="lightcoral", width=32)
        self.btn_grabar.pack(pady=5)
 
        # --- Paso 2: Valor de M interactivo ---
        frame_m = tk.Frame(root)
        frame_m.pack(pady=8)
        tk.Label(frame_m, text="2. Valor de M:").pack(side=tk.LEFT, padx=5)
        self.entry_m = tk.Entry(frame_m, width=8)
        self.entry_m.insert(0, "15")
        self.entry_m.pack(side=tk.LEFT, padx=5)
        self.btn_filtrar = tk.Button(frame_m, text="Aplicar filtro", command=self.ejecutar_filtro,
                                      state=tk.DISABLED)
        self.btn_filtrar.pack(side=tk.LEFT, padx=5)
 
        # --- Paso 3: Graficar ---
        self.btn_grafica = tk.Button(root, text="3. Ver Gráficas (Entrada / Filtrada)",
                                      command=self.mostrar_graficas, state=tk.DISABLED, width=32)
        self.btn_grafica.pack(pady=5)
 
        # --- Paso 4: Reproducción antes/después ---
        self.btn_ruido = tk.Button(root, text="4. Reproducir Antes (Con Ruido)", command=self.play_ruido,
                                    state=tk.DISABLED, width=32)
        self.btn_ruido.pack(pady=5)
 
        self.btn_filtro = tk.Button(root, text="5. Reproducir Después (Filtrada)", command=self.play_filtro,
                                     state=tk.DISABLED, width=32)
        self.btn_filtro.pack(pady=5)
 
        # --- Paso 5: Frecuencia de muestreo interactiva (Nyquist) ---
        frame_fs = tk.Frame(root)
        frame_fs.pack(pady=10)
        tk.Label(frame_fs, text="6. Frecuencia deseada (Hz):").pack(side=tk.LEFT, padx=5)
        self.entry_fs = tk.Entry(frame_fs, width=8)
        self.entry_fs.insert(0, "8000")
        self.entry_fs.pack(side=tk.LEFT, padx=5)
 
        self.btn_nyquist = tk.Button(root, text="Re-muestrear y Verificar Nyquist",
                                      command=self.ejecutar_nyquist, state=tk.DISABLED, width=32)
        self.btn_nyquist.pack(pady=5)
 
        self.label_resultado = tk.Label(root, text="", font=("Arial", 10, "italic"), wraplength=400, justify="center")
        self.label_resultado.pack(pady=5)
 
        self.btn_play_nyquist = tk.Button(root, text="Reproducir señal re-muestreada",
                                           command=self.play_nyquist, state=tk.DISABLED, width=32)
        self.btn_play_nyquist.pack(pady=5)
 
    # ------------------------------------------------------------------
    # Paso 1: Grabación
    # ------------------------------------------------------------------
    def ejecutar_grabacion(self):
        self.btn_grabar.config(text="Grabando...", bg="orange")
        self.root.update()
 
        try:
            self.x_entrada = grabar_audio(duracion=3.0, fs_original=self.fs_original)
            self.y_filtrada = None
            self.x_nyquist = None
 
            self.btn_grabar.config(text="1. Volver a Grabar", bg="lightgreen")
            self.btn_filtrar.config(state=tk.NORMAL)
            self.btn_ruido.config(state=tk.NORMAL)
 
            # Se deshabilitan pasos que dependen del filtrado hasta aplicarlo de nuevo
            self.btn_grafica.config(state=tk.DISABLED)
            self.btn_filtro.config(state=tk.DISABLED)
            self.btn_nyquist.config(state=tk.DISABLED)
            self.btn_play_nyquist.config(state=tk.DISABLED)
            self.label_resultado.config(text="")
 
            messagebox.showinfo("Éxito", "Grabación completada.\nAhora define M y aplica el filtro.")
        except Exception as e:
            messagebox.showerror("Error", f"Falló la grabación: {str(e)}")
            self.btn_grabar.config(text="1. Grabar Voz (3s)", bg="lightcoral")
 
    # ------------------------------------------------------------------
    # Paso 2: Filtrado con M interactivo
    # ------------------------------------------------------------------
    def ejecutar_filtro(self):
        if self.x_entrada is None:
            messagebox.showwarning("Atención", "Primero graba una señal.")
            return
 
        try:
            M_puntos = int(self.entry_m.get())
        except ValueError:
            messagebox.showerror("Error", "M debe ser un número entero.")
            return
 
        try:
            self.y_filtrada = aplicar_filtro_media_movil(self.x_entrada, M_puntos)
            self.x_nyquist = None
            self.label_resultado.config(text="")
 
            self.btn_grafica.config(state=tk.NORMAL)
            self.btn_filtro.config(state=tk.NORMAL)
            self.btn_nyquist.config(state=tk.NORMAL)
            self.btn_play_nyquist.config(state=tk.DISABLED)
 
            messagebox.showinfo("Éxito", f"Filtro aplicado con M = {M_puntos}.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
 
    # ------------------------------------------------------------------
    # Paso 3: Gráficas separadas
    # ------------------------------------------------------------------
    def mostrar_graficas(self):
        t = np.linspace(0, 3.0, len(self.x_entrada))
        muestras_ver = 1000
 
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
 
        ax1.plot(t[:muestras_ver], self.x_entrada[:muestras_ver], color='green')
        ax1.set_title('Señal de entrada (con ruido) $x(n)$')
        ax1.set_ylabel('Amplitud')
        ax1.grid(True)
 
        ax2.plot(t[:muestras_ver], self.y_filtrada[:muestras_ver], color='blue', linewidth=1.2)
        ax2.set_title('Señal filtrada $y(n) = \\sum_{k=0}^{M-1} \\frac{1}{M} x(n-k)$')
        ax2.set_xlabel('Tiempo $t = nT$ [s]')
        ax2.set_ylabel('Amplitud')
        ax2.grid(True)
 
        plt.tight_layout()
        plt.show()
 
    # ------------------------------------------------------------------
    # Paso 4: Reproducción antes/después
    # ------------------------------------------------------------------
    def play_ruido(self):
        sd.play(self.x_entrada, self.fs_original)
 
    def play_filtro(self):
        if self.y_filtrada is None:
            messagebox.showwarning("Atención", "Primero aplica el filtro.")
            return
        sd.play(self.y_filtrada, self.fs_original)
 
    # ------------------------------------------------------------------
    # Paso 5: Verificación interactiva del criterio de Nyquist
    # ------------------------------------------------------------------
    def ejecutar_nyquist(self):
        if self.y_filtrada is None:
            messagebox.showwarning("Atención", "Primero aplica el filtro.")
            return
 
        try:
            fs_deseada = float(self.entry_fs.get())
        except ValueError:
            messagebox.showerror("Error", "La frecuencia deseada debe ser un número.")
            return
 
        try:
            self.x_nyquist, self.fs_nyquist_real, cumple = verificar_criterio_nyquist(
                self.y_filtrada, self.fs_original, fs_deseada
            )
 
            if cumple:
                texto = (f"fs solicitada: {fs_deseada:.0f} Hz  →  fs real: {self.fs_nyquist_real:.0f} Hz\n"
                          "✔ CUMPLE el criterio de Nyquist (voz clara).")
                self.label_resultado.config(text=texto, fg="darkgreen")
            else:
                texto = (f"fs solicitada: {fs_deseada:.0f} Hz  →  fs real: {self.fs_nyquist_real:.0f} Hz\n"
                          "✘ NO CUMPLE el criterio de Nyquist (esperar aliasing).")
                self.label_resultado.config(text=texto, fg="darkred")
 
            self.btn_play_nyquist.config(state=tk.NORMAL)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
 
    def play_nyquist(self):
        sd.play(self.x_nyquist, self.fs_nyquist_real)
 
 
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazLaboratorio(root)
    root.mainloop()