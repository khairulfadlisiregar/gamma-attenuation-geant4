import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

BUILD_DIR = "/home/fadli/geant4-work/gamma_attenuation/build"
x = np.arange(1.0, 11.0, 1.0)  # 1 sampai 10 cm

# Nilai mu terukur dari simulasi sebelumnya (cm^-1) + referensi Pb
mu_al_sim = 0.0836
mu_fe_sim = 0.3917
mu_pb_ref = 1.2400

datasets = {
    "Al": (np.exp(-mu_al_sim * x), mu_al_sim),
    "Fe": (np.exp(-mu_fe_sim * x), mu_fe_sim),
    "Pb (ref)": (np.exp(-mu_pb_ref * x), mu_pb_ref),
}

def exp_model(t, mu):
    return np.exp(-mu * t)

plt.figure(figsize=(8.5, 5.5))

for label, (ratio, mu_init) in datasets.items():
    popt, _ = curve_fit(exp_model, x, ratio, p0=[mu_init], bounds=(0.0, np.inf))
    mu_fit = float(popt[0])
    print(f"{label:8s} -> mu_fit = {mu_fit:.4f} cm^-1 | N/N0(1cm) = {ratio[0]:.4f} | N/N0(10cm) = {ratio[-1]:.4f}")

    plt.scatter(x, ratio, label=f"{label} (data)")
    x_smooth = np.linspace(1.0, 10.0, 200)
    plt.plot(
        x_smooth,
        exp_model(x_smooth, mu_fit),
        linestyle="--",
        label=f"{label} fit ($\\mu={mu_fit:.3f}\\text{{ cm}}^{{-1}}$)",
    )

plt.xlabel("Ketebalan Pelat, $x$ (cm)")
plt.ylabel("Fraksi Transmisi, $N / N_0$")
plt.title("Atenuasi Sinar Gamma 662 keV (1–10 cm) pada Al, Fe, dan Pb")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
out_path = f"{BUILD_DIR}/attenuation_1_10cm_data.png"
plt.savefig(out_path, dpi=300)
print(f"\nGrafik disimpan ke: {out_path}")
