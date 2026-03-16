## 🐞 一、`perf` 是什么？

`perf` 是 Linux 内核自带的性能分析工具，可以用来：
- 查看程序运行时 CPU 占用
- 分析函数调用栈（Call Graph）
- 找出性能瓶颈（比如某个函数耗时太多）

---

## 🛠️ 二、基本用法：如何使用 `perf`

### 1. 安装 perf（一般默认已安装）
```bash
# Ubuntu/Debian
sudo apt install linux-tools-common linux-tools-generic

# CentOS/RHEL/Fedora
sudo yum install perf
# 或
sudo dnf install perf
```

---

### 2. 常用命令示例

#### ✅ 1. 统计程序中各函数的 CPU 使用情况
```bash
perf stat -e cpu-clock,task-clock,instructions,cache-references,cache-misses ./your_program
```

> 输出会告诉你程序运行时间、指令数、缓存命中率等。

---

#### ✅ 2. 采样并查看函数调用栈（采样分析）
```bash
perf record -g ./your_program
```

- `-g`：表示开启调用栈采样（即记录函数调用关系）
- 会生成一个文件：`perf.data`

---

#### ✅ 3. 查看采样结果（查看函数耗时排名）
```bash
perf report
```

- 会进入交互式界面，显示函数调用栈和耗时占比。
- 可以按 `Shift + F` 查看函数调用链。

---

## 🔥 三、如何生成并查看「火焰图」（Flame Graph）

火焰图是 perf 最强的可视化工具之一，能直观看出哪些函数占用了最多 CPU 时间。

### 1. 准备工具：安装 `flamegraph` 脚本

```bash
# 克隆 Brendan Gregg 的火焰图仓库
git clone https://github.com/brendangregg/FlameGraph.git
cd FlameGraph
```

> 这个仓库里有 `perf-flamegraph.pl` 脚本，专门用来生成火焰图。

---

### 2. 生成火焰图

假设你已经运行了：
```bash
perf record -g ./your_program
```

现在生成火焰图：

```bash
# 从 perf.data 生成火焰图
./perf-flamegraph.pl perf.data > flame.svg
```

> 生成的是一个 SVG 格式的火焰图，可以用浏览器打开。

---

### 3. 查看火焰图（推荐用浏览器打开）

```bash
# 用浏览器打开
firefox flame.svg
# 或
open flame.svg  # macOS
```

---

### 🔍 火焰图怎么看？

- **横轴**：函数调用链（从左到右是调用顺序）
- **纵轴**：调用栈深度（越往上，越接近顶层函数）
- **每个矩形**：表示一个函数，宽度代表它在采样中占用的时间比例
- **颜色**：通常为红色，表示热点（耗时多的函数）

> ✅ **重点**：越宽越红的矩形，就是性能瓶颈！

---

## 🧩 Tips：优化使用建议

| 场景 | 推荐命令 |
|------|-----------|
| 快速看 CPU 耗时 | `perf stat ./program` |
| 定位热点函数 | `perf record -g ./program` → `perf report` |
| 直观分析调用栈 | `perf-flamegraph.pl perf.data > flame.svg` |

---

## 🎉 总结

| 步骤 | 命令 |
|------|------|
| 1. 采样性能数据 | `perf record -g ./your_program` |
| 2. 查看函数调用 | `perf report` |
| 3. 生成火焰图 | `./perf-flamegraph.pl perf.data > flame.svg` |
| 4. 浏览火焰图 | 用浏览器打开 `flame.svg` |
