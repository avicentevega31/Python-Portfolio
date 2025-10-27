import requests
import pandas as pd
import matplotlib.pyplot as plt

# ========================================================================================
# 📌 Scraping del Tipo de Cambio SUNAT (Perú)
# ========================================================================================
# Este script consulta el endpoint oficial de SUNAT,
# recorriendo un rango de fechas definido por el usuario
# y consolidando los resultados en un DataFrame histórico.
# ========================================================================================
# Autor: Adrian Vicente Vega
# LinkedIn: https://www.linkedin.com/in/avicentevega31/
# Contacto: +51 936 239 994 / a.vicentevega31@gmail.com
# ========================================================================================

# ==============================
# 🔹 Parámetros de entrada
# ==============================
fecha_inicio = "01/01/2015"
fecha_fin    = "26/10/2025"

# Convertir a datetime
dt_inicio = pd.to_datetime(fecha_inicio, format="%d/%m/%Y")
dt_fin    = pd.to_datetime(fecha_fin, format="%d/%m/%Y")

# Generar lista de meses entre inicio y fin
meses = pd.date_range(start=dt_inicio, end=dt_fin, freq="MS")

# ==============================
# 🔹 Bucle de scraping
# ==============================
dataframes = []

for dt in meses:
    resp = requests.post(
        "https://e-consulta.sunat.gob.pe/cl-at-ittipcam/tcS01Alias/listarTipoCambio", 
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/json; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://e-consulta.sunat.gob.pe/cl-at-ittipcam/tcS01Alias",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Origin": "https://e-consulta.sunat.gob.pe"
        }, 
        json = {
            "anio": dt.year, 
            "mes": dt.month - 1, 
            "token": "."
        }
    )

    if resp.status_code != 200:
        continue
    
    try:
        data_json = resp.json()
    except:
        continue
    
    if not data_json:
        continue

    df_raw = pd.DataFrame.from_records(data_json)
    if df_raw.empty:
        continue

    # Pivotear: cada fecha con Compra y Venta
    df = (
        df_raw.pivot(index="fecPublica", columns="codTipo", values="valTipo")
        .rename(columns={"C": "Compra", "V": "Venta"})
        .reset_index()
    )
    df["Compra"] = df["Compra"].astype(float)
    df["Venta"]  = df["Venta"].astype(float)
    df["Fecha"]  = pd.to_datetime(df["fecPublica"], format="%d/%m/%Y")
    df = df.drop(columns=["fecPublica"])
    dataframes.append(df)

# ==============================
# 🔹 Consolidado histórico
# ==============================
df_hist = pd.concat(dataframes, ignore_index=True)
df_hist = df_hist.sort_values("Fecha").reset_index(drop=True)
df_hist = df_hist[(df_hist["Fecha"] >= dt_inicio) & (df_hist["Fecha"] <= dt_fin)]
df_hist = df_hist.set_index("Fecha")

# ==============================
# 🔹 Exportar a Excel
# ==============================
nombre_archivo = f"tipo_cambio_{dt_inicio.strftime('%Y%m%d')}_{dt_fin.strftime('%Y%m%d')}.xlsx"
df_hist.to_excel(nombre_archivo)

# ==============================
# ✅ Resultado
# ==============================
print(df_hist.head())
print(f"\nArchivo exportado: {nombre_archivo}")

# ==============================
# 🔹 Visualización
# ==============================
plt.figure(figsize=(20, 8))
plt.plot(df_hist.index, df_hist["Compra"], marker="o", linestyle="-", linewidth=1, markersize=0.5, label="Compra")
plt.plot(df_hist.index, df_hist["Venta"], marker="s", linestyle="-", linewidth=1, markersize=0.5, label="Venta")
plt.title("SUNAT - Tipo de Cambio Oficial Histórico ", fontsize=20)
plt.xlabel("Fecha", fontsize=12)
plt.ylabel("Tipo de Cambio (S/.)", fontsize=12)
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
