# H743 的 OTP 区能不能存根公钥

Type: research
Opened: 2026-09-30
Status: open
Blocked by: -

## Question

STM32H743IIK 有没有用户可写的 OTP 区；有的话多大、怎么写（能不能由 bootloader 自己在运行时写，不用 ST-Link）、写一次之后还能不能改或作废、读保护和 RDP 下是什么行为。出处只认 ST 的参考手册 RM0433 和数据手册。它能不能满足「用户不用 ST-Link、换根不重烧 bootloader」，和现有 owner 区比多了什么、少了什么。

## 怎么算答完

一张表：有没有、容量、写入方式、可否更换、出处（手册章节号）；一句结论：能不能用来存根，以及和 owner 区相比的差别。
