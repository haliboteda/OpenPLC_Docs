# ETS 能导入的产品文件怎么做出来

Type: research
Opened: 2026-10-03
Status: open
Blocked by: -

## Question

库里的 `OpenPLC_Bridge.knxprod` 只有 `Catalog.xml`、`Hardware.xml` 和一个应用程序 XML 三个文件，**没有 `knx_master.xml`、签名文件和哈希**；协议栈参考示例里的 `ref/knx/examples/knx-demo/knx-demo-tp.knxprod` 这三样都有。所以它很可能导不进 ETS（**没实测**）。它的 MaskVersion 是 `MV-57B0`（IP 设备），而这张图只做 TP（`0x07B0`）。本机装有 ETS5。

用什么工具、按什么步骤，从源 XML 生成一份 ETS5 能导入的 TP 产品文件；源 XML 放在哪个仓、怎么进版本控制，生成物要不要进。

2026-10-03 调查：用 OpenKNXproducer 4.3.12 加本机 ETS 5.7 的 DLL 已生成一份带签名的 TP 产品；现有那份连 ETS 的 schema 都不符合。见 [KEX-01-findings.md](../KEX-01-findings.md)。

## 怎么算答完

- 写出生成步骤，以及工具的出处（名字、版本、从哪来）
- 生成的一份 TP 产品文件在本机 ETS5 里导入成功，记下 ETS 的提示或日志位置
- 定下源文件的位置
