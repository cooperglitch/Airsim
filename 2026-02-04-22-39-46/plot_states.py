import pandas as pd
import matplotlib.pyplot as plt

# ------------------ Load log ------------------
log_file = "drone_path_20260209_192234.csv" # change this
df = pd.read_csv(log_file)

t = df["time"]

# ------------------ Position ------------------
plt.figure()
plt.plot(t, df["x"], label="x")
plt.plot(t, df["y"], label="y")
plt.plot(t, df["z"], label="z")
plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.title("Position States vs Time")
plt.legend()
plt.grid()
plt.show()

# ------------------ Velocity ------------------
plt.figure()
plt.plot(t, df["vx"], label="vx")
plt.plot(t, df["vy"], label="vy")
plt.plot(t, df["vz"], label="vz")
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.title("Velocity States vs Time")
plt.legend()
plt.grid()
plt.show()

# ------------------ Orientation ------------------
plt.figure()
plt.plot(t, df["roll"], label="roll")
plt.plot(t, df["pitch"], label="pitch")
plt.plot(t, df["yaw"], label="yaw")
plt.xlabel("Time (s)")
plt.ylabel("Angle (rad)")
plt.title("Orientation vs Time")
plt.legend()
plt.grid()
plt.show()

# ------------------ Control vs Response ------------------
plt.figure()
plt.plot(t, df["yaw"], label="Yaw")
plt.plot(t, df["yawRate"], "--", label="Yaw Rate Command")
plt.xlabel("Time (s)")
plt.title("Yaw Response to Command")
plt.legend()
plt.grid()
plt.show()

# ------------------ 3D Trajectory ------------------
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.plot(df["x"], df["y"], df["z"])
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_zlabel("Z (m)")
ax.set_title("3D Flight Trajectory")
plt.show()
