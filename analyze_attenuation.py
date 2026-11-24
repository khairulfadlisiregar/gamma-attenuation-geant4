import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

BUILD_DIR = "/home/fadli/geant4-work/gamma_attenuation/build"
N0 = 10000.0
materials = {
    "Al": "attenuation_Al*.csv",
    "Fe": "attenuation_Fe*.csv",
    "Pb": "attenuation_Pb*.csv",
}

def exp_model(x, mu):
    return np.exp(-mu * x)

plt.figure(figsize=(8, 5))
plotted_any = False

for mat, pattern in materials.items():
    files = sorted(glob.glob(f"{BUILD_DIR}/{pattern}"))
    if not files:
        print(f"[!] Tidak ada file CSV untuk {mat} ({pattern}) — dilewati.\n")
        continue

    dfs = [pd.read_csv(f, comment="#") for f in files]
    data = pd.concat(dfs, ignore_index=True)

    if data.empty:
        print(f"[!] File CSV untuk {mat} kosong — dilewati.\n")
        continue

    if "thickness_cm" not in data.columns:
        data = data.iloc[:, :2]
        data.columns = ["thickness_cm", "energy_keV"]

    counts = data.groupby("thickness_cm").size().sort_index()
    x_vals = counts.index.to_numpy(dtype=float)
    n_vals = counts.to_numpy(dtype=float)
    ratio = np.clip(n_vals / N0, 1e-12, 1.0)

    if len(x_vals) >= 2:
        popt, _ = curve_fit(exp_model, x_vals, ratio, p0=[0.2], bounds=(0.0, np.inf))
        mu_fit = float(popt[0])
    else:
        mu_fit = float(-np.log(ratio[0]) / x_vals[0])

    print(f"=== Material: {mat} ===")
    for x, n, r in zip(x_vals, n_vals, ratio):
        print(f"  x = {x:4.1f} cm | N = {int(n):5d} | N/N0 = {r:.4f}")
    print(f"  -> Koefisien atenuasi linear mu = {mu_fit:.4f} cm^-1\n")

    plt.scatter(x_vals, ratio, label=f"{mat} (simulasi)")
    if len(x_vals) >= 2:
        x_smooth = np.linspace(x_vals.min(), x_vals.max(), 200)
        plt.plot(x_smooth, exp_model(x_smooth, mu_fit), linestyle="--", label=f"{mat} fit ($\\mu={mu_fit:.3f}\\text{{ cm}}^{{-1}}$)")
    else:
        x_smooth = np.linspace(0.0, x_vals[0], 100)
        plt.plot(x_smooth, exp_model(x_smooth, mu_fit), linestyle="--", label=f"{mat} ($\\mu={mu_fit:.3f}\\text{{ cm}}^{{-1}}$)")
    plotted_any = True

if plotted_any:
    plt.xlabel("Ketebalan Pelat, $x$ (cm)")
    plt.ylabel("Rasio Transmisi, $N / N_0$")
    plt.title("Atenuasi Foton Gamma 662 keV pada Al, Fe, dan Pb")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    out_img = f"{BUILD_DIR}/attenuation_comparison.png"
    plt.savefig(out_img, dpi=300)
    print(f"Grafik disimpan ke: {out_img}")
