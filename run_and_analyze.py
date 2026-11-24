import sys
import glob
import subprocess
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

WORK_DIR = "/home/fadli/geant4-work/gamma_attenuation"
BUILD_DIR = f"{WORK_DIR}/build"
EXE = f"{BUILD_DIR}/gamma_attenuation"
VIS_MAC = f"{WORK_DIR}/vis_slab.mac"

MATERIALS = {
    "Al": "G4_Al",
    "Fe": "G4_Fe",
    "Pb": "G4_Pb",
}
THICKNESSES = list(range(1, 11))  # 1 sampai 10 cm
N0 = 10000.0


def open_geant4_vis(mac_file=VIS_MAC):
    """Membuka aplikasi Geant4 dengan makro visualisasi."""
    print(f"Membuka Geant4 dengan makro: {mac_file}")
    subprocess.run([EXE, mac_file], cwd=BUILD_DIR, check=False)


def exp_model(x, mu):
    return np.exp(-mu * x)


def run_batch():
    for mat_label, g4_mat in MATERIALS.items():
        for t in THICKNESSES:
            out_prefix = f"attenuation_{mat_label}_t{t}"
            mac_path = f"{WORK_DIR}/auto_{mat_label}_t{t}.mac"

            mac_content = f"""/run/initialize
/control/verbose 0
/run/verbose 0
/attenuation/slab/material {g4_mat}
/analysis/setFileName {out_prefix}
/attenuation/slab/thickness {float(t)} cm
/run/beamOn {int(N0)}
"""
            with open(mac_path, "w", encoding="utf-8") as f:
                f.write(mac_content)

            print(f"Menjalankan {mat_label} | ketebalan = {t} cm ...")
            subprocess.run([EXE, mac_path], cwd=BUILD_DIR, check=True)


def analyze():
    plt.figure(figsize=(8.5, 5.5))
    plotted = False
    summary_mu = {}

    for mat_label in MATERIALS:
        x_list, n_list = [], []
        for t in THICKNESSES:
            matches = sorted(glob.glob(f"{BUILD_DIR}/attenuation_{mat_label}_t{t}*.csv"))
            if not matches:
                continue
            df = pd.read_csv(matches[0], comment="#")
            n_passed = 0 if df.empty else len(df)
            x_list.append(float(t))
            n_list.append(float(n_passed))

        if not x_list:
            print(f"[!] Tidak ada data CSV untuk {mat_label}.\n")
            continue

        x_vals = np.array(x_list, dtype=float)
        n_vals = np.array(n_list, dtype=float)
        ratio = n_vals / N0

        valid = n_vals > 0
        if np.sum(valid) >= 2:
            popt, _ = curve_fit(
                exp_model, x_vals[valid], ratio[valid], p0=[0.2], bounds=(0.0, np.inf)
            )
            mu_fit = float(popt[0])
        elif np.sum(valid) == 1:
            mu_fit = float(-np.log(ratio[valid][0]) / x_vals[valid][0])
        else:
            mu_fit = np.nan

        summary_mu[mat_label] = mu_fit
        print(f"=== Material: {mat_label} ===")
        for x, n, r in zip(x_vals, n_vals, ratio):
            print(f"  x = {x:4.1f} cm | N = {int(n):5d} | N/N0 = {r:.4f}")
        print(f"  -> mu = {mu_fit:.4f} cm^-1\n")

        plt.scatter(x_vals, ratio, label=f"{mat_label} (simulasi)")
        if not np.isnan(mu_fit):
            x_smooth = np.linspace(x_vals.min(), x_vals.max(), 200)
            plt.plot(
                x_smooth,
                exp_model(x_smooth, mu_fit),
                linestyle="--",
                label=f"{mat_label} fit ($\\mu={mu_fit:.3f}\\text{{ cm}}^{{-1}}$)",
            )
            plotted = True

    print("=== Perbandingan Koefisien Atenuasi Linear (mu) ===")
    for mat_label, mu_val in summary_mu.items():
        print(f"  {mat_label}: {mu_val:.4f} cm^-1")

    if plotted:
        plt.xlabel("Ketebalan Pelat, $x$ (cm)")
        plt.ylabel("Rasio Transmisi, $N / N_0$")
        plt.title("Atenuasi Foton Gamma 662 keV (1–10 cm) pada Al, Fe, dan Pb")
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        out_png = f"{BUILD_DIR}/attenuation_1_10cm.png"
        plt.savefig(out_png, dpi=300)
        print(f"\nGrafik tersimpan di: {out_png}")


if __name__ == "__main__":
    if "--vis" in sys.argv or "--open-geant4" in sys.argv:
        open_geant4_vis()
    else:
        run_batch()
        analyze()
        if "--no-vis" not in sys.argv:
            open_geant4_vis()
