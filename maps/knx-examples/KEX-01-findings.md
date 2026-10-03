# ETS 能导入的产品文件怎么做出来 —— 调查发现

票：[ETS 能导入的产品文件怎么做出来](issues/KEX-01-how-to-make-an-ets-importable-product.md)。2026-10-03，**票未答完**：还差在 ETS5 里实际导入一次。

## 结论

| 是什么 | 为什么 / 出处 |
|---|---|
| 生成工具用 **OpenKNXproducer v4.3.12** 的 `knxprod` 子命令（[releases/v4.3.12](https://github.com/OpenKNX/OpenKNXproducer/releases/tag/v4.3.12)，GPL-3.0），解压即用，签名时调用本机 ETS 的 DLL | 本机实际跑通；thelsing 的 CreateKnxProd 已归档（2022-07 起不再更新） |
| 本机 ETS 是 **5.7**（`ETS5.exe` 5.7.743，`Knx.Ets.XmlSigning.dll` 5.7.227），源 XML 的命名空间必须是 `http://knx.org/xml/project/20` | OpenKNXproducer 要求 ETS 5.7 对应的命名空间完全一致（`OpenKNX.Toolbox.Sign/SignHelper.cs:422-445`）；thelsing 原样的 `project/11` 报 `Could not find ETS path for namespace 11` |
| 库里现有的 `OpenPLC_Bridge.knxprod` **导不进 ETS 5.7** | 用 ETS 自带的 project/20 XSD 校验，三个 XML 都不合规（缺必填属性、用了 schema 里没有的元素和属性）；另外没签名、没哈希，MaskVersion 是 `MV-57B0`、介质是 IP |
| TP 产品（`MV-07B0`）**已生成**，通过 XSD 校验，签名和哈希都有 | 现在是 `$ETSPROD/OpenPLC_TP.knxprod`，源是同目录的 `OpenPLC_TP.xml`（对象表照 KEX-02） |

## 生成步骤（本机跑过）

1. 解压 `OpenKNXproducer-4.3.12.zip`
2. 源 XML 写成单个文件（Catalog、ApplicationPrograms、Hardware 放在同一个 `<Manufacturer>` 下），命名空间 project/20，ID 末尾 4 位写 `0000`（签名时会替换成哈希）
3. `OpenKNXproducer-x64.exe knxprod -V <knx_project_20.xsd> -o out.knxprod src.xml`（XSD 从 `Knx.Ets.Xml.ObjectModel.dll` 里取出；不加 `-V` 就跳过校验）
4. 在 ETS5 里导入 —— **没测**

## 还没验

- 生成的包能在 ETS5 里导入
- 导入后 ETS 能给 thelsing 协议栈下载应用（加载过程照 demo 抄的）—— 要等新的 STKNX 数据链路层上板
（源 XML 和生成物的位置已定：都放 `OpenPLC_ETS_Prod`，用户 2026-10-03）
