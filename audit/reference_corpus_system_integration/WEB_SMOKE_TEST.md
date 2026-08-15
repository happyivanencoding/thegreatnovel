# Web / Browser Smoke Evidence

## 结论

真实浏览器三路径：`BLOCKED`。

本机当前会话没有可调用的浏览器控制工具；因此本轮没有把 Python TestClient、静态
import、CLI 或 HTTP shell 请求冒充真实浏览器验证，也没有伪造 book/task/snapshot id。

## 已完成的非浏览器证据

这些测试使用 disposable `tmp_path` / 临时 workspace，不污染正式 `book/`：

- Original：`tests/integration/test_original_novel.py` 全部通过；首章选择路径检查最终
  Draft task 中存在 `REFERENCE_ONLY` planning context，且 prompt projection 不含
  `source_refs/source_book_ids`。其中已有 Web `TestClient` 页面回归也通过。
- Continuation：`tests/integration/test_planning_contract.py` 全部通过；Candidate task
  生成了 `reference_context_snapshot.json`、`reference_planning_context`，Corpus 未配置
  时状态为显式 `DISABLED`，现有 hard gate/contract 仍通过。
- Revision：`tests/integration/test_revision_workflow.py` 全部通过；Impact → PLANNING
  plan → PROSE draft task 的 snapshot、task metadata 和共享 Prose protocol 均存在。
- Normal Draft：`tests/integration/test_draft_approval.py` 全部通过；enabled、disabled、
  corrupt compatibility 和 compact prose projection 均覆盖。

## Web doctor

`uv run --no-sync novel web doctor` 已执行并退出码为 `0`：API health 为 `true`（HTTP
200）、frontend native JS/CSS 为 `true`、缺失路由为空，static assets/templates 均通过。
该检查证明 Web 运行时入口和静态资源完整；它不替代上面的真实浏览器点击路径。

## 缺失的真实浏览器记录

以下字段没有被伪造，等待具备浏览器控制能力后补录：

```text
Original browser book/handoff/task/snapshot id: 未执行
Continuation browser book/handoff/task/snapshot id: 未执行
Revision browser edition/campaign/unit/task/snapshot id: 未执行
```

当前可以确认的是“Web 代码线和业务函数可达、隔离测试通过”；不能确认“用户浏览器已
完成 Original/Continuation/Revision 三条真实点击路径”。
