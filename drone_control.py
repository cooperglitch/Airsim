import airsim
import time
import keyboard
import csv
import os
from datetime import datetime

# ------------------ AirSim setup ------------------
client = airsim.MultirotorClient()
client.confirmConnection()

# ------------------ Logging setup ------------------
os.makedirs("flightLogs", exist_ok=True)
log_path = f"flightLogs/drone_path_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
print(f"[LOG] Saving flight to: {log_path}")

logFile = open(log_path, "w", newline="")
writer = csv.writer(logFile)

writer.writerow([
    "time", "command",
    "vx", "vy", "vz", "yawRate",
    "x", "y", "z",
    "roll", "pitch", "yaw",
    "lat", "lon", "alt"
])

# ------------------ Control parameters ------------------
VEL = 2.5          # m/s
YAW_RATE = 25.0    # deg/s

vx = vy = vz = 0.0
yawRate = 0.0
currentCmd = "idle"

flying = False
running = True

start_time = time.time()

# ------------------ Main control loop ------------------
while running:

    vx = vy = vz = 0.0
    yawRate = 0.0
    currentCmd = "idle"

    # ---- Takeoff ----
    if keyboard.is_pressed("y") and not flying:
        client.enableApiControl(True)
        client.armDisarm(True)
        client.takeoffAsync().join()
        client.moveToZAsync(-10, 2).join()
        flying = True
        currentCmd = "takeoff"

    # ---- Land ----
    if keyboard.is_pressed("l") and flying:
        client.landAsync().join()
        client.armDisarm(False)
        client.enableApiControl(False)
        flying = False
        currentCmd = "land"

    if not flying:
        time.sleep(0.05)
        continue

    # ---- Translation ----
    if keyboard.is_pressed("w"):
        vx = VEL
        currentCmd = "forward"
    elif keyboard.is_pressed("s"):
        vx = -VEL
        currentCmd = "backward"

    if keyboard.is_pressed("a"):
        vy = -VEL
        currentCmd = "left"
    elif keyboard.is_pressed("d"):
        vy = VEL
        currentCmd = "right"

    if keyboard.is_pressed("z"):
        vz = -VEL
        currentCmd = "up"
    elif keyboard.is_pressed("c"):
        vz = VEL
        currentCmd = "down"

    # ---- Yaw ----
    if keyboard.is_pressed("q"):
        yawRate = -YAW_RATE
        currentCmd = "yawLeft"
    elif keyboard.is_pressed("e"):
        yawRate = YAW_RATE
        currentCmd = "yawRight"

    # ---- Exit ----
    if keyboard.is_pressed("esc"):
        running = False
        break

    # ---- Send command ----
    client.moveByVelocityBodyFrameAsync(
        vx, vy, vz, 0.1,
        drivetrain=airsim.DrivetrainType.MaxDegreeOfFreedom,
        yaw_mode=airsim.YawMode(True, yawRate)
    )

    # ---- Read state ----
    pose = client.simGetVehiclePose()
    gps = client.getGpsData()

    pos = pose.position
    q = pose.orientation
    roll, pitch, yaw = airsim.to_eularian_angles(q)

    # ---- Log state ----
    writer.writerow([
        time.time() - start_time,
        currentCmd,
        vx, vy, vz, yawRate,
        pos.x_val, pos.y_val, pos.z_val,
        roll, pitch, yaw,
        gps.gnss.geo_point.latitude,
        gps.gnss.geo_point.longitude,
        gps.gnss.geo_point.altitude
    ])

    time.sleep(0.05)

# ------------------ Cleanup ------------------
if flying:
    client.landAsync().join()
    client.armDisarm(False)
    client.enableApiControl(False)

logFile.close()
print("Session Ended Safely")
