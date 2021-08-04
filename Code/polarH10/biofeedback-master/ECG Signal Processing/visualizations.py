##------------------------------------- Polar H10--------------------------------------------------------------------##

# from band_pass_filters import bandpass_filters


# import pandas as pd
# import matplotlib.pyplot as plt

# import seaborn as sns


# df = pd.read_csv("df_ecg_Polar.csv", names=["Index", "ECG"])


# sns.set(
#     font="Verdana",
#     rc={
#         "axes.axisbelow": False,
#         "axes.edgecolor": "lightgrey",
#         "axes.facecolor": "None",
#         "axes.grid": False,
#         "axes.labelcolor": "dimgrey",
#         "axes.spines.right": False,
#         "axes.spines.top": False,
#         "figure.facecolor": "white",
#         "lines.solid_capstyle": "round",
#         "patch.edgecolor": "w",
#         "patch.force_edgecolor": True,
#         "text.color": "dimgrey",
#         "xtick.bottom": False,
#         "xtick.color": "dimgrey",
#         "xtick.direction": "out",
#         "xtick.top": False,
#         "ytick.color": "dimgrey",
#         "ytick.direction": "out",
#         "ytick.left": False,
#         "ytick.right": False,
#     },
# )
# sns.set_context(
#     "notebook", rc={"font.size": 16, "axes.titlesize": 20, "axes.labelsize": 18}
# )

# plt.style.use("ggplot")

# plt.figure(figsize=(12, 9))
# ax = plt.subplot(111)
# ax.spines["top"].set_visible(False)
# ax.spines["right"].set_visible(False)


# ax.get_xaxis().tick_bottom()
# ax.get_yaxis().tick_left()


# plt.xticks(range(0, 9000, 1000), fontsize=14)
# plt.yticks(range(-500, 1000, 500), fontsize=14)


# plt.ylabel("Voltage in millivolts", fontsize=16)
# plt.title(
#     "Overlay (Raw & Filtered) Electrocardiogram (ECG) on a PolarH10 device", fontsize=22
# )

# plt.xlabel(
#     "\nData source: www.github.com/pareeknikhil | "
#     "Author: Nikhil Pareek (nikhilpareek.com / @pareeknikhil)",
#     fontsize=10,
# )


# plt.plot(df["ECG"])
# # plt.show()

# filter_data = bandpass_filters(
#     df, 130, low_pass_cutoff_freq=50, high_pass_cutoff_freq=2, notch_cutoff_freq=60,
# )


# plt.plot(filter_data)
# plt.show()


##------------------------------------- Figure 4 Cyton board--------------------------------------------------------------------##


from band_pass_filters import bandpass_filters


import pandas as pd
import matplotlib.pyplot as plt

import seaborn as sns


df = pd.read_csv("df_ecg_cyton.csv", names=["Index", "ECG", "Time"])


sns.set(
    font="Verdana",
    rc={
        "axes.axisbelow": False,
        "axes.edgecolor": "lightgrey",
        "axes.facecolor": "None",
        "axes.grid": False,
        "axes.labelcolor": "dimgrey",
        "axes.spines.right": False,
        "axes.spines.top": False,
        "figure.facecolor": "white",
        "lines.solid_capstyle": "round",
        "patch.edgecolor": "w",
        "patch.force_edgecolor": True,
        "text.color": "dimgrey",
        "xtick.bottom": False,
        "xtick.color": "dimgrey",
        "xtick.direction": "out",
        "xtick.top": False,
        "ytick.color": "dimgrey",
        "ytick.direction": "out",
        "ytick.left": False,
        "ytick.right": False,
    },
)
sns.set_context(
    "notebook", rc={"font.size": 16, "axes.titlesize": 20, "axes.labelsize": 18}
)


plt.figure(figsize=(12, 9))
ax = plt.subplot(111)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)


ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()


# plt.xticks(range(0, 16000, 1000), fontsize=14)
# plt.yticks(range(-500, 9000, 500), fontsize=14)


plt.subplot(2, 1, 1)
plt.plot(df.ECG[200:])
plt.ylabel("Voltage in millivolts", fontsize=16)
plt.title(
    "Overlay (Filtered & Raw) Electrocardiogram (ECG) on OpenBCI-Cyton device",
    fontsize=22,
)
plt.show()

filter_data = bandpass_filters(
    df, 250, low_pass_cutoff_freq=50, high_pass_cutoff_freq=2, notch_cutoff_freq=60,
)

plt.style.use("ggplot")

plt.subplot(2, 1, 2)
plt.plot(filter_data[200:])

plt.ylabel("Voltage in millivolts", fontsize=16)
plt.xlabel(
    "\nData source: www.github.com/pareeknikhil | "
    "Author: Nikhil Pareek (nikhilpareek.com / @pareeknikhil)",
    fontsize=10,
)
plt.show()
