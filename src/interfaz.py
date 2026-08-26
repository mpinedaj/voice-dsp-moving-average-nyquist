import tkinter as tk
from tkinter import messagebox
import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np

from filtro_core import grabar_y_procesar

class InterfazLaboratorio:
    def __init__(self, root):
        self.root = root
        self.root.title("Laboratorio 1: Procesamiento de Señales")
        self.root.geometry("400x350")
        
        self.datos = None
        
        tk.Label(root, text="Filtro de Media Móvil", font=("Arial", 14, "bold")).pack(pady=10)
        
        self.btn_grabar = tk.Button(root, text="1. Grabar Voz (3s)", command=self.ejecutar_grabacion, bg="lightcoral", width=30)
        self.btn_grabar.pack(pady=5)
        
        self.btn_grafica = tk.Button(root, text="2. Ver Gráfica en el Tiempo", command=self.mostrar_grafica, state=tk.DISABLED, width=30)
        self.btn_grafica.pack(pady=5)
        
        self.btn_ruido = tk.Button(root, text="3. Reproducir Antes (Con Ruido)", command=self.play_ruido, state=tk.DISABLED, width=30)
        self.btn_ruido.pack(pady=5)
        
        self.btn_filtro = tk.Button(root, text="4. Reproducir Después (Filtrada)", command=self.play_filtro, state=tk.DISABLED, width=30)
        self.btn_filtro.pack(pady=5)
        
        self.btn_nyq_ok = tk.Button(root, text="5. Nyquist OK (Voz Clara)", command=self.play_nyquist_ok, state=tk.DISABLED, width=30)
        self.btn_nyq_ok.pack(pady=5)
        
        self.btn_nyq_fail = tk.Button(root, text="6. Nyquist FAIL (Aliasing)", command=self.play_nyquist_fail, state=tk.DISABLED, width=30)
        self.btn_nyq_fail.pack(pady=5)

    def ejecutar_grabacion(self):
        self.btn_grabar.config(text="Grabando y calculando matriz...", bg="orange")
        self.root.update()
        
        try:
            self.datos = grabar_y_procesar(duracion=3.0, M_puntos=15)
            
            self.btn_grabar.config(text="1. Volver a Grabar", bg="lightgreen")
            self.btn_grafica.config(state=tk.NORMAL)
            self.btn_ruido.config(state=tk.NORMAL)
            self.btn_filtro.config(state=tk.NORMAL)
            self.btn_nyq_ok.config(state=tk.NORMAL)
            self.btn_nyq_fail.config(state=tk.NORMAL)
            
            messagebox.showinfo("Éxito", "Grabación y filtrado completados.\nCálculo finalizado exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Falló el procesamiento: {str(e)}")
            self.btn_grabar.config(text="1. Grabar Voz (3s)", bg="lightcoral")

    def mostrar_grafica(self):
        t = np.linspace(0, 3.0, len(self.datos['x_entrada']))
        muestras_ver = 1000 
        
        plt.figure(figsize=(10, 4))
        plt.plot(t[:muestras_ver], self.datos['x_entrada'][:muestras_ver], label='Entrada ruidosa $x(n)$', alpha=0.5, color='gray')
        plt.plot(t[:muestras_ver], self.datos['y_filtrada'][:muestras_ver], label='Salida filtrada $y(n)$', color='blue', linewidth=1.2)
        plt.title('Filtrado por Media Móvil: $y(n) = \\sum_{k=0}^{M-1} \\frac{1}{M} x(n-k)$')
        plt.xlabel('Tiempo $t = nT$ [s]')
        plt.ylabel('Amplitud')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def play_ruido(self):
        sd.play(self.datos['x_entrada'], self.datos['fs_original'])

    def play_filtro(self):
        sd.play(self.datos['y_filtrada'], self.datos['fs_original'])

    def play_nyquist_ok(self):
        sd.play(self.datos['x_nyquist_ok'], self.datos['fs_real_ok'])

    def play_nyquist_fail(self):
        sd.play(self.datos['x_nyquist_fail'], self.datos['fs_real_fail'])

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazLaboratorio(root)
    root.mainloop()