# 黄金向量由谁更新

Type: grilling
Opened: 2026-10-02
Status: resolved
Blocked by: -

## Question

`golden_vectors.h` 留在 `$BOOT`，给 T1-16 编译用；生成它的 `gen_vectors.py` 要调出货的 IAPTool，归 `$TEST` 契约层。证书格式一变，它要重新生成：是 `$TEST` 跨仓去写 `$BOOT` 里的那个文件，还是 `$TEST` 只比对、不一致就报错、由人去 `$BOOT` 更新。

## 怎么算答完

写明谁在什么时候生成、写到哪、不一致时谁报错，以及这和决策 76「不互相读写文件」怎么对得上。

## Answer

2026-10-02 定（用户按推荐定，九件一次定完）。`$TEST` 只比对、不写：用出货的 IAPTool 在临时目录重新生成，和 `$BOOT` 提交的 `golden_vectors.h` 比，不一样就判失败并打出去 `$BOOT` 更新的命令。符合决策 76 不互相写文件。

## 引出了什么新的未知

没有。
