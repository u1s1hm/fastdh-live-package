# 互动交接两表

依据运营手册 §11（2026-11-24 核对，手册未注明发布版本）。这些是运营交接字段，不是 JSON/API 字段。写在现有 Media_Resources_and_Pending_Checks.md 的互动节；不要增加另一份配置文件。两表通过 Rule ID 关联，步骤按 Step 排序。中文译本保留表头、ID、枚举与资源类别，翻译自然语言；Chinese name 在两侧均保持中文管理名，Spoken language 仍指正式播出语言。

每格填实际值或 `EMPTY`（明确留空）、`N/A`（不适用）、`PENDING: 原因`（待核）。不要以空格或破折号代替状态。Basis 写用户选择、手册章节或实际回读来源；示例值不是默认。每个配置值只在对应表格单元维护，正文引用 Rule ID/Step，不再维护第二份值。

## 逐规则表：中文字段说明

固定表头见下方示例。

- Rule ID：稳定本地标识；Order：后台列表顺序；Chinese name：非空中文管理名；Enabled：本场配置的弹幕规则为 true，未要求的规则不创建。
- Event：Comments / Gifts / Buttons / Cards，分别对应 audience.message / audience.gift / audience.button / audience.card。
- Keywords：Any keywords 的实际文本；§11.2 是 Unicode 规范化、大小写无关的字面子串匹配。Match semantics 明写实际语义，不写成整条精确匹配。
- Property ID：Gift/Button/Card 对应 gift_id/button_id/card_id；Comments 填 N/A。属性条件始终生效。
- LLM condition：实际语义条件；关键词未命中才由模型判断，模型失败或无模型不视作命中。不能借该条件把已命中的子串再约束为精确匹配。
- Acknowledgement：即时确认原文，可 EMPTY；它可先于后续动作发生，不代表动作成功。其语言遵循 Spoken language。
- Timing：After current speech / Immediately；后者请求立即处理，不能据此认定外部媒体停止。
- Completion：Resume previous content / Stay active / Finish。Failure：Abort remaining steps / Continue optional steps。逐场选择；这里交接平台字段，不设计视频失败兜底。
- Cooldown seconds：0–86400，0 无冷却；Cooldown scope：Per session / Per viewer，后者需要稳定观众 ID。Expiry seconds：手册只证实 1–86400 的作用及范围，未说明空值语义或默认；不需要时可填 PENDING 并回读确认，不能自行宣称 EMPTY 等于无限期。
- Basis：本场取值依据及待核项。不要把建议说成已保存值。

## 逐有序动作表：中文字段说明

- Rule ID、Step：关联规则和 1 起连续步骤序号；每规则 1–8 步，按显示顺序执行。
- Action：Speak text / Generate reply / Performance deployment / Internal capability / External capability / Switch template。
- Text or prompt：Speak text 填完整台词，Generate reply 填可执行的实际回复指令，不写“自然回复”占位；其余不需要文本时 N/A。指令由上传侧映射到当前可用提示配置，入口未证实则记录待核，不能只存在检查表就宣称进入上下文。
- Spoken language：发声步骤的实际语言；纯 Switch template 为 N/A。不因中文译本把 English 改成 Chinese。
- Capability、Parameters：仅适用内部/外部能力步骤；填实际名称、版本及符合注册 Schema 的参数。其它动作 N/A，不臆造参数。Performance deployment 是检索和播放流程，与切换模板不同。
- Template mode：仅 Speak text、Generate reply、Switch template 适用；Keep current template / Fixed category / LLM-assisted selection。
- Template category：Fixed category 填用户实际已处理模板类别，并与媒体映射、video_template_category 关联；不能把本地文件名、示例别名或建议别名当已登记类别。Keep current template 为 N/A；模型辅助不硬填固定类别。
- Required switch：存在切换时 true/false；保持当前模板时 N/A。
- Switch trigger：只在播报步骤附加切换时填 Before this speech / After this speech；独立 Switch template 动作填 N/A。
- Basis：值来源、模板映射引用与待核入口。与规则表同样区分配置预期和实际结果。

## 填写示例（合成场景，禁止直接套入项目）

假定用户要求普通英语聊天，并接受包含 111 的评论切换到其已确认类别 demo_base。两项可以单独选择或并存。这里的 demo_base、冷却和策略均为示例选择。规则遵循首条命中的启用规则；具体指令在兜底回复前。

| Rule ID | Order | Chinese name | Enabled | Event | Keywords | Match semantics | Property ID | LLM condition | Acknowledgement | Timing | Completion | Failure | Cooldown seconds | Cooldown scope | Expiry seconds | Basis |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R01 | 1 | 切换指定模板 | true | Comments | 111 | Unicode normalized case-insensitive substring | N/A | EMPTY | EMPTY | After current speech | Resume previous content | Abort remaining steps | 0 | Per session | 60 | 合成用户选择；§11；类别见资源映射；未上传 |
| R02 | 2 | 普通评论回复 | true | Comments | EMPTY | LLM semantic decision | N/A | 普通问候或与本场主题有关的问题，不处理模板指令 | EMPTY | After current speech | Resume previous content | Abort remaining steps | 0 | Per session | 60 | 合成用户选择；§11；模型命中待预览 |

| Rule ID | Step | Action | Text or prompt | Spoken language | Capability | Parameters | Template mode | Template category | Required switch | Switch trigger | Basis |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R01 | 1 | Switch template | N/A | N/A | N/A | N/A | Fixed category | demo_base | true | N/A | 合成映射类别；§11.4；不是点播原视频 |
| R02 | 1 | Generate reply | Answer the current comment in one or two natural English sentences, using Soul's voice. Answer directly; do not invent viewer reactions or claim a template switch succeeded. | English | N/A | N/A | Keep current template | N/A | N/A | N/A | 合成用户方向；提示配置入口待回读 |

仅选聊天时保留 R02 及其动作，Order 改为 1，ID 不变；仅选切换时只保留 R01。无规则时保留两表表头和零数据行，在同节写“本场无互动规则；规则数 0，步骤数 0”，不创建假规则。

## 正反例与证据

对以上子串示例：111、1111、hi111 都应命中 R01；普通评论不命中 R01，由 R02 的模型条件决定，不能静态保证模型回复。若用户要求只有整条 111 才切换，则 1111、hi111 是不应命中的反例，当前子串配置却会命中：需求未满足，标待核并停止该规则定稿，不能声称精确命中。不要擅自改成模型精确判断或新增规则。

静态检查只核字段、关联、顺序和预期。Deterministic preview 不调用模型或播放；Real LLM/OpenFM; no playback 使用模拟外部结果，仍不是实播。上传侧保存回读记录实际配置；实播另记录事件、实际模板切换和回复语言。无评论屏蔽、冷却、过期等干扰的测试前提要注明。单独切换模板不证明播放了原视频，不承诺窗口内返场。
