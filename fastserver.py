import matplotlib.pyplot as plt
import numpy as np

# 生成随机数据
np.random.seed(42)
x = np.random.rand(50) * 10
y = np.random.rand(50) * 10

# 创建散点图
plt.figure(figsize=(8, 6))
plt.scatter(x, y, color='blue', alpha=0.7, label='Data Points')

# 添加标题和标签
plt.title('Basic Scatter Plot', fontsize=14)
plt.xlabel('X-axis', fontsize=12)
plt.ylabel('Y-axis', fontsize=12)
plt.legend()

# 显示网格
plt.grid(True, linestyle='--', alpha=0.5)

plt.show()