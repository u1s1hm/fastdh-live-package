# FastDH 字段指南

本表供 Agent 生成内容包和给出控制台配置清单使用，不是 FastDH 导入格式，也不新增直播交付文件。`producer default` 是逐场运营建议，不是平台默认。每一行还要标注值的来源状态：`platform default`（手册明确默认）、`producer default`（本场运营建议）、`set`（本场明确设置）、`inherit`（保留现有值）、`clear`（明确清空）或 `needs readback`。平台没有说明的枚举、默认或恢复能力保持 `needs readback`。

| group | field | applies when | confirmed options | producer default | rationale / source | verification state | local config pointer / runtime result |
|---|---|---|---|---|---|---|---|
| identity | Agent Profile | every scene | name, display name, Agents.md, Soul.md | one Agent for one live scene | manual 3.1-3.2 | confirmed | actual Agent ID |
| identity | Scenario category | live programme | `Live` | `Live` | manual 4.1 | confirmed | actual Scenario ID |
| identity | Scenario status | publish target | `draft`, `active`, `paused`, `archived` | `active` after review | manual 4.2 | confirmed | published revision |
| identity | management title | every scene | non-empty Scenario name | Chinese title when requested | manual 4.3; operating convention | needs readback | exact title |
| runtime | live mode | live script | `manual`, `auto_online`, `auto_online_prologue`, `auto_knowledge`, `auto_knowledge_prologue` | `manual` for supplied LiveScript | manual 8.1 | confirmed | selected value |
| runtime | content ending | live script | `graceful`, `loop` | ask per scene | manual 8.2 | confirmed | loop bounds |
| speech_language | generated script language | automatic mode | English, Chinese, French, Spanish, Russian | project language | manual 8.6 | confirmed | language |
| speech_language | live line interval | live script | 100-120000 ms; platform default 1200 | retain default unless pacing requires change | manual 8.3 | confirmed | saved value |
| runtime | resume live after interruption | interactive live | 0-300 s; platform default 30 | ask per scene | manual 8.4 | confirmed | saved value |
| runtime | chunking | live speech | Medium, Sentence, Line, Hybrid | ask when pacing matters | manual 8.5 | confirmed | saved value |
| speech_language | voice emotion | when the console exposes an emotion control | no handout-backed options or default | needs readback; describe desired feeling in content terms | observed in operations, absent from manual source | needs readback | exact UI label, value, and runtime effect |
| context | memory retrieval | memory needed | `disabled`, `llm`, `always`, `hybrid` | `disabled`; result limit 6 if enabled | manual 5.1-5.3; operating convention | confirmed | mode and count |
| context | memory results | memory enabled | 1-50; platform default 6 | 6 | manual 5.2 | confirmed | saved value |
| context | knowledge retrieval | source-backed claims | same four modes; library and domain required when enabled | follow named source | manual 6.1-6.4 | confirmed | library, collection, domain, order |
| context | capability authorization | any | derived from configuration; no Scenario model input | let platform derive capabilities | manual 4.5-4.6, 12 | confirmed | derived capabilities |
| audience | selected-comment queue | comment interaction | enabled/disabled; max 1-200, default 20; expiry empty or 1-86400 | ask whether ordinary comments enter | manual 9 | confirmed | queue settings |
| orchestration | programme sequence | fixed programme | enabled/disabled; 1-based loop bounds | enabled when ordered content is requested | manual 10.1-10.2 | confirmed | ordered element IDs |
| orchestration | element type | programme | Live section, Queued performances, Prerecorded digital-human video, Transition | use approved types only | manual 10.3 | confirmed | timeline |
| orchestration | live end condition | Live section | `Script exhausted` | `Script exhausted` | manual 10.10 | confirmed | line range and source hash |
| orchestration | offline video end condition | offline video | `Brain reports video ended` | `Brain reports video ended` | manual 10.10; operating convention | confirmed | playback end event |
| orchestration | queued performance | interaction window | max 1-10; default 1; Set duration default 30 | one per approved window | manual 10.9-10.12 | confirmed | count, duration, timing |
| orchestration | block audience comments | element | checked/unchecked | checked for real-time speech; interaction windows are the approved route | manual 10.14; operating convention | confirmed | per-element state |
| orchestration | template switch | element/rule | keep current, fixed category, LLM-assisted; graceful/hard; required optional | only for a real base change | manual 10.7, 11.4 | confirmed | category and mode |
| orchestration | interaction window | approved performance slot | Queued performances; per-visit max 1-10; duration or video-ended behavior | define position, duration, request quota, and stop policy per scene | manual 10.9-10.12 | confirmed | element ID and settings |
| interaction | trigger | rule | Comments, Gifts, Buttons, Cards; enabled/disabled | every configured rule enabled; omit unrequested rules | manual 11.1; operating instruction | confirmed | event type and order |
| interaction | match condition | rule | keyword, event property ID, optional LLM condition; exact matching is not established | use only matching behavior the operator has verified | manual 11.2; substring preview observed | needs readback | rule test evidence |
| interaction | action | rule | Speak text, Generate reply, Performance deployment, Internal/External capability, Switch template | choose from approved experience | manual 11.4 | confirmed | ordered steps |
| interaction | timing | rule | After current speech, Immediately | `After current speech` unless interruption approved | manual 11.4 | confirmed | timing |
| interaction | return | rule | Resume previous content, Stay active, Finish | ask per scene; fixed content normally resumes | manual 11.5 | confirmed | return path |
| interaction | failure | rule | Abort remaining steps, Continue optional steps | preserve selected platform behavior | manual 11.5 | confirmed | saved choice; runtime unverified |
| interaction | cooldown | rule | 0-86400 s; Per session, Per viewer | ask per rule | manual 11.5 | confirmed | rule ID and value |
| interaction | expiry | rule | 1-86400 s; empty semantics/default needs readback | ask when timing is intended | manual 11.5 | confirmed | saved value |
| validation | save state | configuration groups | identity, runtime, speech_language, audience; partial save possible | require all intended groups read back | manual 17.2-17.4 | confirmed | saved/partial groups |
| validation | runtime result | production test | Brain session, events, actions, actual IDs | separate readback from real playback | manual 14, 17.4 | confirmed | runtime evidence |

## 保存状态规则

每个字段在生成摘要中只出现一个最终值和一个来源状态。新建场景没有可继承值时使用 `set` 或明确的 `platform default`；迁移场景只有用户要求保留才写 `inherit`；清空知识、循环、过期时间或旧规则时写 `clear`，不能用空白含糊表示。上传侧保存后必须逐组回读；`Partially saved` 时只接受成功组的实际回读值，失败组保持待处理。关闭未保存板块出现的高层确认弹窗属于上传流程观察，生成技能只提示上传侧先保存并回读，不把它写成内容包字段。

## 无点播场景

若本场明确不提供互动点播，编排中不创建空的 `Queued performances` 元素，规则中不生成无目标的 `Performance deployment` 步骤，也不因存在 LIPSYNC 底板就宣称有点播窗口。普通评论回复可单独存在，但必须在访谈和规则中与点播体验分开描述。

## 固定默认的边界

“Brain reports video ended + block audience comments”是本技能对实时口播/固定视频元素的运营默认，须按本场内容重新确认；它不等于所有互动窗口都屏蔽评论。媒体播放失败、超时和恢复属于 FastDH 兜底，本技能不为它们增加脚本或验收分支。

平台能力自动推导，不生成授权勾选项。数字人媒体由使用者按别名上传；本技能维护别名、映射和文档引用，不代替上传或生成平台 ID。实际 ID、revision、source hash、playback instance 和事件结果只能在控制台或 Brain 回读后填写。

## 三个独立配置面

选评评论队列（§9）、节目中的互动点播窗口（§10）和弹幕规则（§11）分别记录、分别保存、分别回读。普通评论生成回复与指令点播是不同体验：不能因为存在一个就宣称另一个已配置。每次访问可执行的表演数量、可接收的请求数量，以及点播视频期间是否暂停计时也是三个不同问题，必须分别询问和填写。所有实际创建的弹幕规则启用；未被用户选择的互动规则不创建。一个案例中的 13 个固定口播、6 个离线视频、6 个互动窗口或 7 条启用规则都是案例数据，不是默认值；PETOPIA 的临时别名也不迁移。

严格整条匹配、返场、精确代码、窗口内恢复、接收/播放次数等能力只在当前控制台回读或实播证据存在时写入定稿。历史上看见 `111` 的子串命中时，可以把 `1111`、`hi111` 作为反例记录，但不能把它当作平台全局规则或自动生成默认。

运营观察表明现有底板首尾帧相同，Brain 视频结束有利于自然切换；指定时长或脚本结束可能出现跳帧。长口播可能引发重复动作，短口播可能静默。因此先按自然语义和情感转折分段，再按情感换底板；用实测音频或语言/语速区间估算，不用固定时长、行数或占比硬切。以上是运营观察，不是平台字段默认；静态配置、预览和保存成功都不能证明实播。

逐条互动交接字段以 [互动交接两表](interaction-tables.md) 为唯一填写规范；此处为概览，不另维护第二份规则值。
