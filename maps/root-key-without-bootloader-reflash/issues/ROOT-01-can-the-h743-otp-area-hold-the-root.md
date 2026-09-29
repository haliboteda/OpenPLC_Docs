# H743 的 OTP 区能不能存根公钥

Type: research
Opened: 2026-09-30
Status: resolved
Blocked by: -

## Question

STM32H743IIK 有没有用户可写的 OTP 区；有的话多大、怎么写（能不能由 bootloader 自己在运行时写，不用 ST-Link）、写一次之后还能不能改或作废、读保护和 RDP 下是什么行为。出处只认 ST 的参考手册 RM0433 和数据手册。它能不能满足「用户不用 ST-Link、换根不重烧 bootloader」，和现有 owner 区比多了什么、少了什么。

## 怎么算答完

一张表：有没有、容量、写入方式、可否更换、出处（手册章节号）；一句结论：能不能用来存根，以及和 owner 区相比的差别。

## Answer

2026-09-30 定（查 RM0433 Rev 8、DS12110 Rev 11，未上板）：**STM32H743 没有用户 OTP 区**，芯片上也没有别的一次性存储既放得下 64 字节公钥、又能由 bootloader 运行时自己写；根只能继续放在 owner 区这种普通 flash 里。逐项见 [ROOT-01-findings.md](../ROOT-01-findings.md)。

## 引出了什么新的未知

- [M2 归属与信任](../../../docs/modules/M2-ownership.md) 说 WRP「清除需要 ST-Link/J-Link 物理访问」，RM0433 §4.5.2 写的是 RDP 0/1 下软件可随时改 WRP → 记进 [work/TODO.md](../../../work/TODO.md)
