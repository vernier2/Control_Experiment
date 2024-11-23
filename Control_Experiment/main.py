import matplotlib.pyplot as plt
from pylab import mpl
import numpy as np
from scipy.optimize import curve_fit

# 初始化两个空列表来存储数据
# 数据采样频率为100Hz
# 设置显示中文字体
mpl.rcParams["font.sans-serif"] = ["SimHei"]
# 禁用unicode负号
plt.rcParams['axes.unicode_minus'] = False

time = []
for i in range(2500):
    time.append(i / 100)

velocity = []  # 速度
location = []  # 位置
directives = []  # 指令

# 打开文件
with open('直流偏置\\velPosDataAz.txt', 'r') as file:
    # 逐行读取文件
    for line in file:
        # 移除行尾的换行符并分割行
        columns = line.strip().split()
        # 假设每行都有两列数据
        if len(columns) == 2:
            velocity.append(eval(columns[0]))  # 第一列数据
            location.append(eval(columns[1]))  # 第二列数据

with open('直流偏置\\identDataAz.txt', 'r') as file:
    # 逐行读取文件
    for line in file:
        # 移除行尾的换行符并分割行
        columns = line.strip().split()
        # 假设每行都有两列数据
        if len(columns) == 2:
            directives.append(eval(columns[0]))  # 第一列数据

# 确保位置的范围为0~360°
for i in range(len(location)):
    if location[i] < 0:
        location[i] += 360

# 可以认为5s后系统稳定，将数据都取为5s后
velocity = velocity[500:]
location = location[500:]

plt.figure(figsize=(10, 3))
plt.plot(time[500:], velocity, 'b-')
# plt.scatter(location, velocity, s=[5] * len(location))
plt.xlabel('时间 (s)')
plt.ylabel('位置 (deg)')
plt.title('给定为3500的时间-位置数据曲线图')
plt.show()


# 对位置与速度数做连续与平滑处理（1°中的速度做平均处理）
total_data = []
for i in range(360):
    total_data.append([])
for i in range(len(location)):
    for j in range(360):
        if j < location[i] < j + 1:
            total_data[j].append(velocity[i])

velocity_smooth = []
location_smooth = []
for i in range(360):
    location_smooth.append(i)
    velocity_smooth.append(sum(total_data[i]) / len(total_data[i]))  # 取1°中的平均

#  处理结束
plt.figure(figsize=(10, 3))
plt.plot(location_smooth, velocity_smooth, 'b-')
plt.xlabel('角度 (deg)')
plt.ylabel('角速度 (deg/s)')
plt.title('给定为3500的位置-速度曲线图')
plt.show()

velocity = []  # 速度
location = []  # 位置
directives = []  # 指令

# 打开文件
with open('直流偏置+正弦相应\\velPosDataAz.txt', 'r') as file:
    # 逐行读取文件
    for line in file:
        # 移除行尾的换行符并分割行
        columns = line.strip().split()
        # 假设每行都有两列数据
        if len(columns) == 2:
            velocity.append(eval(columns[0]))  # 第一列数据
            location.append(eval(columns[1]))  # 第二列数据

with open('直流偏置+正弦相应\\identDataAz.txt', 'r') as file:
    # 逐行读取文件
    for line in file:
        # 移除行尾的换行符并分割行
        columns = line.strip().split()
        # 假设每行都有两列数据
        if len(columns) == 2:
            directives.append(eval(columns[0]))  # 第一列数据

# 确保位置的范围为0~360°
for i in range(len(location)):
    if location[i] < 0:
        location[i] += 360


plt.figure(figsize=(10, 3))
plt.plot(time[1000:], velocity[1000:], 'b-')
# plt.scatter(location, velocity, s=[5] * len(location))
plt.xlabel('时间 (s)')
plt.ylabel('位置 (deg)')
plt.title('直流偏置+5Hz正弦的时间-位置数据曲线图')
plt.show()


upp = 1300
wide = 1
velocity = velocity[1000:upp]
location = location[1000:upp]
directives = directives[1000:upp]
time = time[1000:upp]

directives = np.array(directives)
directives -= 3500
directives /= 20
for i in range(len(time)):
    # velocity[i] -= 604
    velocity[i] -= velocity_smooth[int(location[i])]

plt.figure(figsize=(10, 3))
plt.plot(time, velocity, 'b-', lw=wide, label='输出响应')
plt.plot(time, directives, 'r-', lw=wide, label='0.05给定')
plt.axhline(y=0, color='gray', linewidth=0.75)
plt.xlabel('时间 (s)')
plt.ylabel('速度 (deg/s)')
plt.title('去除偏置的5Hz正弦响应曲线')
plt.legend()
# plt.ylim(-200, 200)
plt.show()

# 定义正弦函数模型

velocity = np.array(velocity)
directives = np.array(directives)
time = np.array(time)


def sine_function(x, A, B, C):
    return A * np.sin(B * x + C)


# 使用curve_fit进行拟合
params, params_covariance = curve_fit(sine_function, time, velocity, p0=[150, 2 * 3.14 * 10, 0])

# 打印拟合参数
A, B, C = params
print(f"拟合参数：A={A}, B={B}, C={C}")

# 使用拟合参数生成模型数据
plt.figure(figsize=(10, 3))
plt.plot(time, velocity, 'b--', lw=wide, label='数据')
# plt.scatter(time, velocity, label='数据', color='blue', s=[5] * len(velocity))
plt.plot(time, sine_function(time, *params), 'r', lw=wide, label='拟合曲线')
plt.axhline(y=0, color='gray', linewidth=0.75)
plt.xlabel('时间 (s)')
plt.ylabel('速度 (deg/s)')
plt.title('去除偏置的5Hz正弦响应拟合曲线')
plt.ylim(-150, 150)
plt.legend()
plt.show()
