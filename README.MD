# Git-Miner-Demo-Website

### Tab1: 展示仓库的基本信息
- 目标仓库的首页README.md：数据来源：/home/+username+/.gitminer/repoID/repo/{README, readme}.{MD, md}
---
- commits总数：可在LOCSumLastCommit+repoID表中对commit列求和获得
- contributors数量：可在LOCSumLastCommit+repoID表中求元组数量获得
- 建立时间：在CommitByDay+repoID表中取第一个commit的时间

以上三项样式为一行，模仿GitHub仓库首页上面那种
---
- Top10 commits数量贡献者：样式为表，数据在LOCSumLastCommit
