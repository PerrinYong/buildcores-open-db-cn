# open-db-cn

中国大陆增量产品事实目录。

用途：

- 存放来自中国大陆市场的补充产品事实（优先京东联盟相关来源）。
- 与 `open-db-upstream/open-db/` 共同构成 `buildcores-open-db-cn` 的产品事实并集。

约束：

- 不写入价格、促销、库存等市场事实字段。
- 新增或修改的产品必须可归并到统一 `product_id`。
- 建议目录结构与 `open-db-upstream/open-db/` 保持相同品类层级。
