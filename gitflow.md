# 🌐 Git Flow 架构图（中文标注版）

```mermaid
graph TD
    A[main<br>主分支<br>生产环境] -->|创建分支| B[develop<br>开发基线<br>集成所有功能]

    B -->|创建分支| C[feature/xxx<br>功能分支<br>开发新功能]

    C -->|PR 合并| B

    B -->|创建分支| D[release/xxx<br>发布分支<br>版本发布前测试与修复]

    D -->|PR 合并| A
    D -->|PR 合并| B

    A -->|紧急修复创建| E[hotfix/xxx<br>紧急修复分支<br>修复线上严重问题]

    E -->|PR 合并| A
    E -->|PR 合并| B

    classDef branch fill:#f0f8ff,stroke:#333,stroke-width:1px;
    classDef main fill:#d4edda,stroke:#28a745,stroke-width:2px;
    classDef develop fill:#fff3cd,stroke:#ffc107,stroke-width:2px;
    classDef feature fill:#cce5ff,stroke:#007bff,stroke-width:1.5px;
    classDef release fill:#d1ecf1,stroke:#17a2b8,stroke-width:1.5px;
    classDef hotfix fill:#f8d7da,stroke:#dc3545,stroke-width:1.5px;

    class A main
    class B develop
    class C feature
    class D release
    class E hotfix
```

# 🌐 优化后的git flow架构图（增加个人开发分支）
```mermaid
graph TD
    A[main<br>主分支<br>生产环境] -->|创建分支| B[develop<br>开发基线<br>集成所有功能]

    B -->|创建分支| C[feature/xxx<br>功能分支<br>开发新功能]

    C -->|PR 合并| B

    B -->|创建分支| D[release/xxx<br>发布分支<br>版本发布前测试与修复]

    D -->|PR 合并| A
    D -->|PR 合并| B

    A -->|紧急修复创建| E[hotfix/xxx<br>紧急修复分支<br>修复线上严重问题]

    E -->|PR 合并| A
    E -->|PR 合并| B

    %% 新增：个人开发分支（仅本地使用）
    B -->|创建分支（本地）| F[xxx_dev<br>个人开发分支<br>仅限本地使用<br>开发完成后合并回 develop]

    F -->|PR 合并| B

    %% 样式定义（保持一致性）
    classDef branch fill:#f0f8ff,stroke:#333,stroke-width:1px;
    classDef main fill:#d4edda,stroke:#28a745,stroke-width:2px;
    classDef develop fill:#fff3cd,stroke:#ffc107,stroke-width:2px;
    classDef feature fill:#cce5ff,stroke:#007bff,stroke-width:1.5px;
    classDef release fill:#d1ecf1,stroke:#17a2b8,stroke-width:1.5px;
    classDef hotfix fill:#f8d7da,stroke:#dc3545,stroke-width:1.5px;
    classDef personal fill:#ffebee,stroke:#d32f2f,stroke-width:1.5px,font-weight:normal;

    class A main
    class B develop
    class C feature
    class D release
    class E hotfix
    class F personal

    %% 图注说明（可选，不影响渲染）
    %% 注意：严禁将 xxx_dev 推送至远程！开发完成后合并回 develop 并删除。
```

# 🌐 详细版 git flow架构图
```mermaid
graph TD
    A[main<br>主分支<br>生产环境] -->|创建分支| B[develop<br>开发基线<br>集成所有功能]

    B -->|创建分支（本地）| C[feature/xxx<br>功能分支<br>开发新功能<br>✓ 合并后建议删除]

    C -->|PR 合并| B
    C -->|push| D[origin/feature/xxx<br>远程功能分支<br>用于 PR 和代码审查]

    D -->|PR| B

    B -->|创建分支（本地）| E[release/xxx<br>发布分支<br>版本发布前测试与修复<br>✓ 合并后建议删除]

    E -->|PR 合并| A
    E -->|PR 合并| B
    E -->|push| F[origin/release/xxx<br>远程发布分支<br>暂存待发布的版本]

    F -->|PR| A
    F -->|PR| B

    A -->|紧急修复创建（本地）| G[hotfix/xxx<br>紧急修复分支<br>修复线上严重问题<br>✓ 合并后建议删除]

    G -->|PR 合并| A
    G -->|PR 合并| B
    G -->|push| H[origin/hotfix/xxx<br>远程紧急修复分支<br>用于审查和合并]

    H -->|PR| A
    H -->|PR| B

    %% 新增：个人开发分支（仅本地使用）
    B -->|创建分支（本地）| I[xxx_dev<br>个人开发分支<br>仅限本地使用<br>开发完成后合并回 develop<br>✓ 合并后建议删除]

    I -->|PR 合并| B
    I -->|push| J[origin/xxx_dev<br>远程个人分支<br>可选：用于协作或备份]

    J -->|PR| B

    %% ================ 样式定义 =================
    classDef main fill:#d4edda,stroke:#28a745,stroke-width:2px,font-weight:bold;
    classDef develop fill:#fff3cd,stroke:#ffc107,stroke-width:2px,font-weight:bold;
    classDef feature fill:#cce5ff,stroke:#007bff,stroke-width:1.5px,font-weight:normal;
    classDef release fill:#d1ecf1,stroke:#17a2b8,stroke-width:1.5px,font-weight:normal;
    classDef hotfix fill:#f8d7da,stroke:#dc3545,stroke-width:1.5px,font-weight:normal;
    classDef personal fill:#ffebee,stroke:#d32f2f,stroke-width:1.5px,font-weight:normal;

    classDef local fill:#cce,stroke:#333,stroke-width:1px;
    classDef remote fill:#cce,stroke:#333,stroke-width:1px,stroke-dasharray:5 5;

    %% ================ 分支类型标注 =================
    class A main
    class B develop
    class C feature,local
    class D remote
    class E release,local
    class F remote
    class G hotfix,local
    class H remote
    class I personal,local
    class J remote

    %% ================ 合并箭头样式 =================
    linkStyle 0 stroke:#080,stroke-width:2px
    linkStyle 1 stroke:#080,stroke-width:2px
    linkStyle 2 stroke:#080,stroke-width:2px
    linkStyle 3 stroke:#080,stroke-width:2px
    linkStyle 4 stroke:#080,stroke-width:2px
    linkStyle 5 stroke:#080,stroke-width:2px
    linkStyle 6 stroke:#080,stroke-width:2px
    linkStyle 7 stroke:#080,stroke-width:2px
    linkStyle 8 stroke:#080,stroke-width:2px
    linkStyle 9 stroke:#080,stroke-width:2px
```
**解释说明**  
> 💡 图中，本地直接提PR/MR 属于 本地git MR方式（单仓模式），不用将本地分支推送到远端，即可直接创建从本地分支到远端的主库的MR。


# ✅ 总结
1. ✅ 使用 标准 Git Flow 工作流图 作为参考（如 Atlassian 官方图）。
2. ✅ 所有合并操作必须遵循 “从下往上” 的原则：feature → develop，develop → release，release → main。
3. ✅ 紧急修复（hotfix）是例外，但必须通过专用分支完成，不能直接合并 main 到 develop

# Q&A
## 🔍 为什么不能把 main 合并到 develop？
**原因一：破坏开发基线的稳定性**  
+ develop 是所有新功能的集成点。
+ 如果 main 的代码被合并到 develop，可能会引入未经测试的生产代码，污染开发环境。

**原因二：违反“单向流动”原则**  
+ Git Flow 设计为 从开发 → 发布 → 生产 的单向流程。
+ 任何“反向合并”都可能导致分支污染、版本混乱、CI/CD 失效等问题。

**原因三：紧急修复（hotfix）的处理方式已提供了“反向”通道**
+ 在 Git Flow 中，hotfix 分支是从 main 创建的，修复完成后合并回 main 和 develop。
+ 这正是 “从 main 向 develop 合并” 的唯一合法场景！
但注意：这是通过 hotfix 分支完成的，不是直接在 main 和 develop 之间建立箭头
