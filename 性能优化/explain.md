## 🎯 一、`EXPLAIN` 是什么？

> `EXPLAIN` 是 MySQL（也适用于其他数据库如 PostgreSQL、Oracle）提供的一个命令，用于**查看 SQL 查询的执行计划（Execution Plan）**。

📌 它不真正执行查询，而是告诉我们：
- MySQL 会如何执行这个查询？
- 用到了哪些索引？
- 表之间怎么连接？
- 是否走了全表扫描？

---

## 📌 二、如何使用 `EXPLAIN`？

### ✅ 基本语法：

```sql
EXPLAIN SELECT * FROM users WHERE city = '北京';
```

或者：

```sql
EXPLAIN FORMAT=JSON SELECT * FROM users WHERE city = '北京';
```

> 💡 推荐使用 `FORMAT=JSON`，输出更清晰、信息更丰富。

---

## 🧩 三、`EXPLAIN` 输出字段详解（以 MySQL 为例）

下面是一个典型的 `EXPLAIN` 输出示例：

| id | select_type | table | partitions | type | possible_keys | key | key_len | ref | rows | filtered | Extra |
|----|---------------|-------|------------|------|------------------|-----|----------|-----|------|----------|-------|

接下来逐个解释每个字段的含义：

---

### 🔹 1. `id`
> **查询中每个 SELECT 的标识符**

- 如果是简单查询（只有一个 `SELECT`），`id` 通常是 `1`。
- 如果是子查询或联合查询（如 `UNION`），会有多行，`id` 会不同。

📌 **注意**：`id` 越大，执行顺序越靠后；`id` 相同的，从上往下执行。

---

### 🔹 2. `select_type`
> **查询类型，表示这个 SELECT 是什么类型的查询**

常见值：
| 值 | 含义 |
|----|------|
| `SIMPLE` | 简单查询（不包含子查询或 UNION） |
| `PRIMARY` | 主查询（在包含子查询的外部查询中） |
| `SUBQUERY` | 子查询中的第一个 SELECT |
| `DERIVED` | 派生表（如 `FROM (SELECT ...)`） |
| `UNION` | `UNION` 中的第二个及以后的 SELECT |
| `UNION RESULT` | `UNION` 的结果 |
| `MATERIALIZED` | 表示子查询的执行结果被“物化”为一个临时表，之后再被主查询使用|

📌 **重点**：看到 `UNION`、`DERIVED` 等，可能说明查询复杂，需要优化。

---

### 🔹 3. `table`
> **当前行对应的表名**

- 可能是真实表名，也可能是临时表（如 `derivedN`）。
- 如果是 `NULL`，说明是 `UNION` 或 `UNION RESULT` 的结果。

---

### 🔹 4. `partitions`
> **命中了哪些分区（仅在使用分区表时有效）**

- 如果表没有分区，这个字段可能是 `NULL`。
- 否则会显示实际命中分区名，如 `p0`、`p1`。

---

### 🔹 5. `type`
> **连接类型（访问类型），表示 MySQL 如何查找行**

📌 这是 **最关键的一列**，决定了查询性能！

常见值（从最好到最差）：

| 值 | 含义 | 说明 |
|----|------|------|
| `system` | 表只有一行（系统表） | 极少见 |
| `const` | 通过主键或唯一索引查到一行 | 很快，如 `WHERE id = 1` |
| `eq_ref` | 使用主键或唯一索引连接，每行只匹配一行 | 常见于 `JOIN` 中 |
| `ref` | 使用非唯一索引查找，可能匹配多行 | 比 `eq_ref` 差一点 |
| `ref_or_null` | 类似 `ref`，但额外包含 `NULL` 值的行 | 用于 `WHERE col = val OR col IS NULL` |
| `index_merge` | 使用多个索引的合并扫描 | 通常性能不错 |
| `unique_subquery` | 子查询中用到了唯一索引 | 优化后可提升 |
| `index_subquery` | 子查询中用到了非唯一索引 | 性能一般 |
| `range` | 使用索引范围扫描（如 `BETWEEN`, `>`, `<`） | 比 `ref` 差，但比 `ALL` 好 |
| `index` | 全索引扫描（扫描整个索引树） | 比全表扫描好，但效率不高 |
| `ALL` | 全表扫描（最差） | 警告！必须优化 |

📌 **重点关注**：如果 `type` 是 `ALL` 或 `index`，说明没有用上索引，需要检查是否建了合适的复合索引。

---

### 🔹 6. `possible_keys`
> **可能用到的索引（候选索引）**

- 列出所有可能被 MySQL 用来优化查询的索引。
- 如果是 `NULL`，说明没有可用的索引。

📌 **重点**：如果你的查询本该走索引，但 `possible_keys` 是 `NULL`，说明索引没建对。

---

### 🔹 7. `key`
> **实际用到的索引**

- 如果是 `NULL`，说明没有使用索引，走了 `ALL` 或 `index`。
- 例如：`idx_city_age`，表示用到了这个索引。

📌 **重点**：`key` ≠ `possible_keys`，只有实际用到了的才显示。

---

### 🔹 8. `key_len`
> **使用索引的长度（字节数）**

- 表示 MySQL 在执行查询时，使用了索引的多少个字节。
- 通常用于判断是否用上了全部的复合索引。

📌 **举例**：
- 复合索引 `(city, age)`，`city` 是 `VARCHAR(50)`，用 `utf8mb4` 编码 → 最大 50×4 = 200 字节。
- `age` 是 `INT` → 4 字节。
- 如果 `key_len = 204`，说明用了 `city` 和 `age` 全部字段。
- 如果 `key_len = 200`，说明只用了 `city`，没有用上 `age`。

📌 **重点**：`key_len` 小于索引总长度，说明**没有用上全部字段**，可能违反了最左前缀原则。

---

### 🔹 9. `ref`
> **显示与索引列比较的列或常量**

- 表示：哪些列或常量被用来和索引进行比较。
- 常见值：
  - `const`：常量（如 `WHERE id = 1`）
  - `users.city`：列名
  - `NULL`：没有比较

📌 **重点**：如果 `ref` 是 `NULL`，说明没用上索引。

---

### 🔹 10. `rows`
> **MySQL 估计需要扫描的行数**

- 估算值，不一定是真实值。
- 数值越小越好。

📌 **重点**：如果 `rows` 很大（比如几万、几十万），说明查询效率差，需要优化索引或查询逻辑。

---

### 🔹 11. `filtered`
> **表示当前表中满足 WHERE 条件的行所占百分比**

- 例如：`filtered = 50.00`，表示约 50% 的行满足条件。
- 结合 `rows`，可以估算出实际返回的行数。

📌 **重点**：如果 `filtered` 很低（比如 1%），说明过滤效果差，可能需要更精确的索引或条件。

---

### 🔹 12. `Extra`
> **附加信息，包含很多关键提示**

常见值（非常重要！）：

| 值 | 含义 | 优化建议 |
|----|------|-----------|
| `Using where` | 使用了 WHERE 条件过滤 | 正常，但如果 `type = ALL` 就危险 |
| `Using index` | 覆盖索引（查询字段都在索引中，无需回表） | ✅ 极佳！ |
| `Using index condition` | 使用了索引下推（Index Condition Pushdown） | ✅ 优化技术，提升性能 |
| `Using temporary` | 使用了临时表 | ❌ 性能差，需优化 |
| `Using filesort` | 使用了文件排序（非索引排序） | ❌ 性能差，需加索引 |
| `Using join buffer` | 使用了连接缓冲区 | 通常出现在大表 `JOIN` 时，可优化 |
| `Impossible WHERE` | WHERE 条件永远为假 | 说明 SQL 有问题 |
| `Select tables optimized away` | 查询结果可直接从索引中获取 | ✅ 极佳优化 |

📌 **重点**：
- 出现 `Using temporary` 或 `Using filesort`，说明查询效率差，**必须优化**。
- 出现 `Using index` 是**大利好**，说明走的是覆盖索引，性能极佳。

---

## ✅ 四、实战建议

### 🔍 如何用 `EXPLAIN` 诊断慢查询？

1. **看 `type`**：是否是 `ALL`？如果是，必须加索引。
2. **看 `key`**：是否真的用了索引？如果 `key = NULL`，说明没用上。
3. **看 `key_len`**：是否用上了复合索引的全部字段？
4. **看 `Extra`**：有没有 `Using temporary` 或 `Using filesort`？
5. **看 `rows` 和 `filtered`**：估算扫描行数是否过大？

---

## 🎁 五、高效使用 `EXPLAIN`

- ✅ 用 `EXPLAIN FORMAT=JSON` 看更清晰的执行计划。
- ✅ 用 `EXPLAIN FORMAT=TRADITIONAL` 看更详细的输出。
- ✅ 在生产环境使用时，避免频繁执行，以免影响性能。
- ✅ 结合 `SHOW PROFILE` 和 `Performance Schema` 做更深入分析。

---

## 📣 总结：

> 📌 **`EXPLAIN` 就是 SQL 查询的“体检报告”** —— 它告诉你：  
> “你这个查询，**走不走索引？**  
> **会不会全表扫描？**  
> **有没有临时表或文件排序？**”


## 问答

### select_type: MATERIALIZED是什么意思？
MySQL 把这个子查询的结果先“存”起来（变成临时表），然后用这张“临时表”去参与后续的查询或连接操作。


**什么情况下会出现MATERIALIZED**  
+ 带IN的子查询（尤其是大表）
```sql
SELECT * FROM users 
WHERE city IN (SELECT city FROM cities WHERE population > 100万);
```
 MySQL 会把子查询的结果（满足条件的城市列表）物化成一个临时表，再用这张表去做 IN 匹配。

 + 带EXISTS的子查询（且子查询结果需要重复使用）
```sql
SELECT * FROM orders o
WHERE EXISTS (
    SELECT 1 FROM order_items oi 
    WHERE oi.order_id = o.id AND oi.amount > 100
);
```
MySQL 可能会将子查询的结果“物化”为临时表，以提升执行效率。


**优化器判断物化比重复执行子查询更高效**  

MySQL 优化器会根据：

子查询结果大小
是否会被多次使用
是否能建立索引
👉 如果判断“物化”后性能更好，就会自动选择 MATERIALIZED。


**MATERIALIZED 是好是坏？**  

✅ 优点：

避免重复执行子查询（尤其是大表）。
可以对物化后的临时表建立索引，提升后续查询效率。
⚠️ 缺点：

需要额外的内存或磁盘空间来存储临时表。
如果子查询结果非常大，可能造成性能瓶颈。
📌 总结：MATERIALIZED 本身不是“坏”字段，而是 MySQL 优化器为了提升性能所做的智能决策。

**如何查看MATERIALIZED 的子查询结果？**  

虽然不能直接看到临时表内容，但可以通过以下方式辅助分析：

1. 使用 EXPLAIN FORMAT=JSON 会更清晰地显示子查询的物化过程。

2. 观察 Extra 字段
- 如果看到 Using materialized table 或类似提示，说明确实物化了。
- 如果看到 Using index 在临时表上，说明优化器还对临时表做了索引优化。


**建议**  

| 场景 | 建议 |
|---|---|
|子查询结果很大（上万行）| 考虑是否可以改写为 JOIN，避免物化开销|
|子查询被多次使用| MATERIALIZED 是合理选择，不必担心|
|rows 很大，Extra 有 Using temporary|说明物化后性能仍差，需优化索引或改写 SQL|
