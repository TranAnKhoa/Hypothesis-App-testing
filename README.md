# 📊 Data Quality & Stability Validator

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![GUI](https://img.shields.io/badge/GUI-PyQt5-green)
![Status](https://img.shields.io/badge/Status-Stable-brightgreen)

## 💡 Overview

**Data Quality & Stability Validator** is a desktop application built with **Python** and **PyQt5**. 

Before feeding data into complex Optimization models or Forecasting algorithms, ensuring data reliability is crucial. This tool provides a streamlined interface for analysts to import raw data, perform statistical hypothesis testing, and visualize distributions to verify stability and consistency.

---

## 📺 Application Demo

See the tool in action:




https://github.com/user-attachments/assets/add0ebec-3bdc-49f3-9768-915e5a440691





---

## ✨ Key Features

### 1. Data Import & Handling
* 📂 **Excel Support:** Seamlessly browse and import `.xlsx` or `.csv` files.
* 🔢 **Flexible Selection:** Manually select specific columns/populations for comparison.

### 2. Statistical Validation (Hypothesis Testing)
Automated statistical tests to determine if data populations are significantly different or stable over time:
* **Two-Sample Testing:** T-Test, Z-Test (for checking stability between two datasets).
* **Multi-Sample Testing:** One-way **ANOVA** (Analysis of Variance) for comparing multiple groups/populations.

### 3. Advanced Visualization
Instant plotting to visualize data distribution and detect outliers:
* 📉 **Histograms & KDE:** For distribution shape analysis.
* 📦 **Box Plots:** For spotting outliers and quartiles.
* points **Scatter Plots:** For correlation checking.
* 📈 **Control Charts (R-Chart/X-bar):** For monitoring process stability.

---

## 📸 Screenshots

| Data Input Interface | Visualization & Results |
| :---: | :---: |
| ![Input Screen] <img width="1918" height="1022" alt="Screenshot 2026-01-10 013036" src="https://github.com/user-attachments/assets/97761993-635b-42a6-b9c5-a8aad5261f6a" />
| ![Chart Screen] <img width="796" height="1005" alt="Screenshot 2026-01-10 013012" src="https://github.com/user-attachments/assets/605483da-25e1-42e4-8e0d-f38a407ff4aa" />

---

## 🛠️ Tech Stack

* **Core Logic:** Python
* **GUI Framework:** PyQt5 (Qt Designer)
* **Data Manipulation:** Pandas, NumPy
* **Statistics:** SciPy, Statsmodels
* **Visualization:** Matplotlib, Seaborn

---

## 🤝 Contact

Developed by **Tran An Khoa & Nguyen Tien Dat**.
If you have any questions regarding the statistical methods or code structure, feel free to reach out via khoatran201105@gmail.com.
