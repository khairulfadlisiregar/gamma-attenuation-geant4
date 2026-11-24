# gamma-attenuation-geant4

Simulasi atenuasi foton gamma 662 keV pada pelat **Al**, **Fe**, dan **Pb** (ketebalan **1–10 cm**) menggunakan Geant4 serta analisis/visualisasi rasio transmisi ($N/N_0$) dan koefisien atenuasi linear ($\mu$) dengan Python.

## Menjalankan Visualisasi Geant4
1. Masuk ke folder `build` lalu jalankan makro visualisasi `vis_slab.mac`:
   `cd build && ./gamma_attenuation ../vis_slab.mac`

## Menjalankan Analisis & Ekspor Tabel
- `python3 plot_from_data.py`
- `python3 export_table_and_plot.py`
