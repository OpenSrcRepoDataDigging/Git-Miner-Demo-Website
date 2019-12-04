# Git-Miner-Demo-Website

## 在图的旁边对指标做一定的文字解释，可以显著提升展示效果。这一点在以后再添加，写在这里以备忘。

### Tab1: 展示仓库的基本信息
- 目标仓库的首页README.md：数据来源：/home/+username+/.gitminer/repoID/repo/{README, readme}.{MD, md}
---
- commits总数：可在LOCSumLastCommit+repoID表中对commit列求和获得
- contributors数量：可在LOCSumLastCommit+repoID表中求元组数量获得
- 建立时间：在CommitByDay+repoID表中取第一个commit的时间

以上三项样式为一行，模仿GitHub仓库首页上面那种
---
- Top10 commits数量贡献者：样式为表，数据在LOCSumLastCommit表中。orderby
- Top10 总体-个人贡献(相对)相似度： 数据来源：CommitTimesListByDay+repoID表+Python的Frechet距离计算。

    这部分Frechet距离的计算应在仓库初始化时进行，同时将计算结果存入数据库中。
    
    **排序应按照commit数量排序，不按照弗雷歇距离排序。以呈现出一种错落有致的效果。因此在存储Frechet距离的表中可同时存入commit数量**
    
    echarts参考：https://www.echartsjs.com/examples/en/editor.html?c=dataset-encode0&theme=light 其中纵轴为人名，横轴为相似度，颜色深浅代表commit数量
    
    
### Tab2：贡献演化

#### 总commit曲线
- 数据在CommitListByDay+repoID表中，All那一列。
- echarts参考：https://www.echartsjs.com/examples/en/editor.html?c=line-simple

#### 总-分类commit曲线
- 数据在"ClassifiedCommitList" + repoID表中，All那一列。数据格式为add-del-fix-mod。
- echarts参考 https://www.echartsjs.com/examples/en/editor.html?c=line-stack

#### 条形码
- 总的条形码
- Top5(orderby commits数量)的条形码
- 数据来源：CommitListByDay+repoID表中
- 涉及到数据库的连接，嵌套子查询可以解决
#### Top5贡献折线图
- 数据在ClassfiedCommitList+repoID中，与条形码数据一致
- echarts参考 https://www.echartsjs.com/examples/en/editor.html?c=line-stack 建议与总-分类commit曲线选择不同的色调以区分不同的图

### Tab3：空间分布
- heatmap。已实现

### Tab4：协作关系

#### 贡献者网络 - 无向带权图
- 数据在ContributorNetworkMatrix+repoID中，形式为邻接矩阵
- echarts参考：https://www.echartsjs.com/examples/en/editor.html?c=graph  只取一个类别