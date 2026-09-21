# app 版本号怎么从 sketch 传到 core

Type: grilling
Opened: 2026-09-21
Status: resolved
Blocked by: -

## Question

烧录前要比版本，就得让**板子报出自己这一版 app 的版本号**。而版本号由用户写在 sketch 里。

⚠️ **拦路的是 Arduino 的编译模型**：core 编译成 `libcore.a` 是独立的一次编译，**不读 `.ino` 的内容**。
所以用户在 `.ino` 里写 `#define`，`cores/.../udp_server.c` 编译时取不到。

约束（用户 2026-09-21 定）：**用户只接触 `.ino`，不会去建或找 `.h` 文件。**

四个候选：

| | 怎么做 | 用户写什么 |
|---|---|---|
| **A** | core 只声明 `extern const char openplc_app_version[];` 不定义，宏让 sketch 定义它 | `.ino` 里 `OPENPLC_APP_VERSION(1, 0, 0);` |
| **B** | 在 A 之上，`prebuild.sh` 先粗查 sketch 里有没有这个词 | 同 A |
| **D** | `prebuild.sh` 解析源码取出版本号，生成头文件给 core include | `.ino` 里 `#define OPENPLC_APP_VERSION "1.2.3"` |
| **E** | 用 Arduino 官方的 `build_opt.h`（`-D` 发给所有编译单元） | sketch 目录建 `build_opt.h` |

## 怎么算答完

1. 选定一个，写出**用户在 `.ino` 里实际要敲的那一行**
2. 写明**漏写版本号时会发生什么**，以及用户看到的报错长什么样
3. 写明 `.version` 文件（上位机比对用）**从哪里取值**，并论证它和固件里那一份不会分叉
4. 写明要删 / 要改 `$CORE_REPO` 的哪几处

## Answer

2026-09-21 定

**选 A+B。**

**1 · 用户在 `.ino` 里敲这一行，不用写 `#include`**：

```cpp
OPENPLC_APP_VERSION(1, 0, 0);

void setup() { /* ... */ }
void loop()  { /* ... */ }
```

不用 `#include` 的原因：Arduino IDE 自动给每个 `.ino` 插 `#include <Arduino.h>`，宏挂在它下面。

**2 · 漏写时**：`prebuild.sh` 粗查 sketch 里有没有出现 `OPENPLC_APP_VERSION` 这个词，
没有就退出非零，报错文案自己写（要指出该加哪一行）。
**粗查故意不解析值** —— 误判方向只会是「该拦没拦」，由链接器兜底（`undefined reference`）。

**3 · `.version` 从 ELF 里提取那个符号**，`postbuild.sh` 做。
这样它**就是固件里跑的那一份**，不存在分叉。

**4 · 要改 `$CORE_REPO`**：

| 哪里 | 改什么 |
|---|---|
| 新的公共头文件 | 定义宏，展开成 `extern "C" const char openplc_app_version[] = "maj.min.pat"` |
| `cores/arduino/Arduino.h` | 加一行 include，让用户不必自己写 |
| `cores/arduino/stm32/IAP_config.h` | 删掉 `OPENPLC_FW_VERSION` 的 `"0.0.0"` fallback；**那段注释描述了不存在的 `.version` 文件和比对行为，一并改掉** |
| `libraries/OpenPLC_IAP/src/udp_server.c` | 用 `extern` 声明那个符号 |
| `system/extras/prebuild.sh` | 加粗查 |
| `system/extras/postbuild.sh` | 从 ELF 提取符号，生成 `.version` |

### ⚠️ 一个少了就不工作的细节

宏必须写成 `extern "C"`：**C++ 里命名空间作用域的 `const` 变量默认是 internal linkage**，
不加就不导出符号，core 链接不到，而且报的是「undefined reference」，查起来很绕。
它同时解决 name mangling 和 linkage 两件事。

**宏的完整定义（含三条范围断言）写在 [版本号的格式和比大小的规则](VER-05-version-format-and-comparison.md) 里，本票不重复。**

### 为什么不是 D

D 靠 `prebuild.sh` 用文本匹配**猜预处理器会算出什么**，而这件事只有编译器算得准。两个会撞上的场景：

- **条件编译**：`#ifdef DEBUG_BUILD` 两个分支各写一个版本号，`grep | head -1` 取到的和实际编译的不是一个
- **注释掉的旧版本**：不排除 `//` 的正则会抓到被注释那行

后果是**板子报的版本、sketch 自己用的、`.version` 里的，三份可能互不相同，而且没有任何东西会发现**。

### 为什么不是 E

`build_opt.h` 是 Arduino 官方机制、这个 core 也已经支持（`prebuild.sh` 在处理它，
经 `platform.txt:25` 的 `"@{build.opt.path}"` 发给所有编译单元）。
**但它是 sketch 目录下一个单独的文件**，与「用户只接触 `.ino`」冲突。

## 引出了什么新的未知

三条，各自已开票：

- [identity 怎么同时报卡包版本和 app 版本](VER-04-how-does-identity-carry-both-versions.md)
- [版本号的格式和比大小的规则](VER-05-version-format-and-comparison.md)
- [强制烧录这个开关长什么样](VER-06-what-does-the-force-switch-look-like.md)
