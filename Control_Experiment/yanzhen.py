import matplotlib.pyplot as plt
from pylab import mpl
import matplotlib.font_manager as fm

# 初始化两个空列表来存储数据
# 数据采样频率为100Hz
# 设置显示中文字体
mpl.rcParams["font.sans-serif"] = ["SimHei"]
# 禁用unicode负号
plt.rcParams['axes.unicode_minus'] = False

Frequency = []  # 频率
Magnitude = []  # 幅值
Phase = []  # 相位
Magnitude_Curve = []  # 幅值拟合
Phase_Curve = []  # 相位拟合

# 打开文件
with open('modelBodeCompareAz.txt', 'r') as file:
    # 逐行读取文件
    for line in file:
        # 移除行尾的换行符并分割行
        columns = line.strip().split()
        Frequency.append(eval(columns[0]))
        Magnitude.append(eval(columns[1]))
        Phase.append(eval(columns[2]))
        Magnitude_Curve.append(eval(columns[3]))
        Phase_Curve.append(eval(columns[4]))

wide = 1

'''
plt.figure(figsize=(10, 3))
plt.plot(Frequency, Magnitude, 'b-', lw=wide, label='数值解')
# plt.scatter(time, velocity, label='数据', color='blue', s=[5] * len(velocity))
plt.plot(Frequency, Magnitude_Curve, 'r-', lw=wide, label='解析解')
plt.xlabel('频率 (Hz)')
plt.xscale('log')
plt.ylabel('幅值 (dB)')
plt.title('系统的频率特性曲线')
# plt.ylim(-150, 150)
plt.legend()
plt.show()

plt.figure(figsize=(10, 3))
plt.plot(Frequency, Phase, 'b-', lw=wide, label='数值解')
# plt.scatter(time, velocity, label='数据', color='blue', s=[5] * len(velocity))
plt.plot(Frequency, Phase_Curve, 'r-', lw=wide, label='解析解')
plt.xlabel('频率 (Hz)')
plt.xscale('log')
plt.ylabel('相角 (deg)')
plt.title('系统的频率特性曲线')
# plt.ylim(-150, 150)
plt.legend()
plt.show()
'''

# 创建一个包含两个子图的画布，1行2列
fig, axs = plt.subplots(2, 1, figsize=(10, 6))  # 调整figsize为(10, 6)以适应两个子图

# 第一个子图（上）
axs[0].plot(Frequency, Magnitude, 'b-', lw=wide, label='数值解')
axs[0].plot(Frequency, Magnitude_Curve, 'r-', lw=wide, label='解析解')
axs[0].set_xscale('log')
axs[0].set_ylabel('幅值 (dB)')
axs[0].set_title('系统的频率特性曲线')
axs[0].legend()
axs[0].grid(True)
axs[0].set_xlim(0.1, 100)
axs[0].set_ylim(-70, -10)

axs[0].scatter(5, -31.598, color='#90FF90', marker='o', s = 100)  # 单独显示这个点，颜色为红色

# 添加标注
axs[0].annotate(f'x = 5.001\ny = -31.598',  # 标注内容
                (5.001, -31.598),  # 标注位置
                textcoords="offset points",  # 相对于点的位置
                xytext=(-50, -30))

# 第二个子图（下）
axs[1].plot(Frequency, Phase, 'b-', lw=wide, label='数值解')
axs[1].plot(Frequency, Phase_Curve, 'r-', lw=wide, label='解析解')
axs[1].set_xlabel('频率 (Hz)')
axs[1].set_xscale('log')
axs[1].set_ylabel('相角 (deg)')
axs[1].legend()
axs[1].grid(True)
axs[1].set_xlim(0.1, 100)
axs[1].set_ylim(-800, 100)

axs[1].scatter(5, -120.045, color='#90FF90', marker='o', s = 100)  # 单独显示这个点，颜色为红色

# 添加标注
axs[1].annotate(f'x = 5.001\ny = -120.045',  # 标注内容
                (5, -120.045),  # 标注位置
                textcoords="offset points",  # 相对于点的位置
                xytext=(-20, -30))

# 调整子图间距
plt.tight_layout()

ax = plt.gca()
tick_font = fm.FontProperties(family='Times New Roman')
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontproperties(tick_font)

plt.show()
