## ORM性能自查清单

|检查项	| 是否满足|
|---|---|
|是否在循环中访问外键字段？	|❌ / ✅|
|是否使用了 select_related 处理 ForeignKey？	|❌ / ✅|
|是否使用了 prefetch_related 处理 ManyToMany？	|❌ / ✅|
|是否用了 only() / defer() 精简字段？	|❌ / ✅|
|是否用 annotate() 做聚合，避免 Python 层统计？	|❌ / ✅|
|是否启用了 django-debug-toolbar 查看 SQL？	|❌ / ✅|
