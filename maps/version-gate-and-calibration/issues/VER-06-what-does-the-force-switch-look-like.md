# 强制烧录这个开关长什么样

Type: grilling
Opened: 2026-09-21
Status: resolved
Blocked by: -

## Question

用户 2026-09-21 定：**版本低了拒绝烧录；要强制就勾菜单里的选项，IAPTool 再强制烧。**
开关本身的形态还没定。

Arduino IDE 侧的机制是现成的 —— `boards.txt` 的 menu，照
[`menu.upload_method`](../../../../open_plc_arduino/boards.txt) 抄：

```
menu.forceflash=Force flash (ignore version)
OPEN-PLC.menu.forceflash.no=No
OPEN-PLC.menu.forceflash.yes=Yes
OPEN-PLC.menu.forceflash.yes.upload.???=???
```

要定的：

1. **选项怎么传到 IAPTool** —— 走 `upload.options`？还是新加一个变量？两条路径（`cdctransfer` / `ethtransfer`）都要通
2. **默认值**：`No`。但 ⚠️ **Arduino IDE 的菜单选择是粘住的** —— 用户勾过一次 `Yes`，
   除非他自己改回来，**之后每次烧录都是强制**。要不要想办法让它一次性？想不了的话要在文档里写明
3. **IAPTool 侧的开关形态**：命令行加 `--force`？环境变量？
4. ~~**强制烧录时板子侧要不要留痕**~~ —— **2026-09-21 用户定：不用记。**
   板子上也确实没地方记（事件日志这一版删了），要记就得动扇区 15 的布局，不划算

## 怎么算答完

1. 写出 `boards.txt` 要加的那几行，以及它怎么到达 IAPTool
2. 写明默认值，以及**「菜单粘住」这件事怎么处理**（能解决就解决，不能就写进说明）
3. 写出 IAPTool 侧的参数名和行为
4. 写明强制烧录时**上位机**的输出。⚠️ **板子侧不留痕已定**（用户 2026-09-21）

## Answer

2026-09-21 定

**选 T：菜单照做，「一次性」由 IAPTool 自己保证。**

### 1 · 菜单

`boards.txt` 加一个和 `Upload method` 平级的菜单项，两个子项，默认「否」：

```
menu.forceflash=低版本强制烧录
OPEN-PLC.menu.forceflash.no=否
OPEN-PLC.menu.forceflash.no.upload.force_flag=
OPEN-PLC.menu.forceflash.yes=是
OPEN-PLC.menu.forceflash.yes.upload.force_flag=--force
```

⚠️ **必须用新变量名 `upload.force_flag`，不能复用 `upload.options`** ——
后者已被 `menu.upload_method` 的四个选项各自设过，两个菜单设同一个属性会互相覆盖。
还要在 `boards.txt` 顶层给 `OPEN-PLC.upload.force_flag=` 一个默认空值，
否则选了 SWD 那两条路时变量没定义。

⚠️ **两条 upload.pattern 现在没有引用任何选项变量**，要各加一个 `{upload.force_flag}`：

```
tools.cdctransfer.upload.pattern=... "{serial.port}" {upload.force_flag}
tools.ethtransfer.upload.pattern=... "{serial.port}" {upload.force_flag}
```

### 2 · 为什么不靠菜单自己变回「否」

**做不到。** Arduino IDE 2 的菜单选择存在 IDE 自己的配置里、按 sketch 路径索引，
**不在 sketch 目录**；IDE 在内存里持有它，上传工具是它启动的子进程，
改任何文件都不会让 IDE 重读。`sketch.yaml` 那套在 IDE 2 里至今是 feature request。

### 3 · 一次性怎么实现

IAPTool 在用户目录放一个标记文件（如 `~/.openplc/force_used`）：

| IAPTool 收到 | 标记 | 做什么 |
|---|---|---|
| `--force` | 不存在 | 强制烧录。**只有烧成功才写标记** |
| `--force` | 存在 | **拒绝**，提示「强制烧录已用过一次，请到 工具 ▸ 低版本强制烧录 改回『否』」 |
| 不带 `--force` | 任意 | **删掉标记**，然后正常比对版本 |

**关键在最后一行**：把菜单拨回「否」这个动作本身就是重置 ——
IAPTool 只要看见一次「不带 `--force` 的调用」，就知道开关关了。
它不需要读 IDE 的任何东西，也不需要改 IDE 的任何东西。

### 4 · 失败重试不受影响

**标记只在烧录成功之后才写。** 所以第一次强制烧到一半失败了，标记没写，
直接重试即可 —— 不需要「同板同版本 N 分钟内算一次」那种带时间窗的规则。

### 5 · 输出

- 强制成功：`*** FORCE FLASH — version check skipped. This was one-shot; the next force will be refused. ***`
- 被标记拦下：明确指出去哪个菜单改回「否」
- **板子侧不留痕**（用户 2026-09-21 定，且事件日志这一版已删，板上没地方记）

## 引出了什么新的未知

没有。
