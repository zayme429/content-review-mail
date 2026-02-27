# 内容生产管线 - 部署配置指南

## 概述

自动化内容生产管线，支持：
- 主题驱动的文献采集（Tavily Search）
- LLM 生成 3 篇独立候选文章
- 审核邮件发送（含主题、文献集合、完整文章）
- 邮件回复自动接收（SendClaw）
- 微信公众号草稿箱推送

---

## 一、环境准备

```bash
# 克隆仓库
git clone https://github.com/zayme429/content-review-mail.git
cd content-review-mail/content-pipeline

# 安装 Python 依赖
pip install -r requirements.txt

# 安装 wenyan-cli（微信发布工具）
npm install -g wenyan-cli
```

---

## 二、配置 secrets.json

```bash
cp config/secrets.example.json config/secrets.json
```

编辑 `config/secrets.json`，填入以下配置：

```json
{
  "wechat": {
    "app_id": "你的微信公众号 AppID",
    "app_secret": "你的微信公众号 AppSecret"
  },
  "smtp": {
    "host": "smtp.163.com",
    "port": 465,
    "secure": true,
    "user": "你的163邮箱",
    "pass": "163邮箱授权码（不是登录密码）",
    "from": "你的163邮箱"
  },
  "review": {
    "recipient": "你的审核收件邮箱（用于接收审核邮件）",
    "zapier_email": "你的SendClaw邮箱（用于接收回复）"
  },
  "tavily": {
    "api_key": "你的 Tavily API Key"
  },
  "moonshot": {
    "api_key": "你的 Moonshot API Key（如不用 OpenClaw 内置则填写）"
  },
  "sendclaw": {
    "api_key": "你的 SendClaw API Key",
    "email": "你的handle@sendclaw.com",
    "bot_id": "你的 SendClaw Bot ID"
  }
}
```

---

## 三、注册各服务账号

### 1. Tavily Search（文献采集）
- 注册：https://tavily.com
- 免费版每月 1000 次搜索，够用
- 拿到 API Key 填入 `secrets.json` → `tavily.api_key`

### 2. SendClaw（审核回复收件）

> ⚠️ 必须在**本地电脑**执行注册命令，不能在服务器上注册（服务器 IP 可能被限制）

```bash
# 在本地电脑执行（Mac/Linux）
curl -X POST https://sendclaw.com/api/bots/register \
  -H "Content-Type: application/json" \
  -d '{"name":"你的Bot名称","handle":"你的handle","senderName":"显示名称"}'
```

> handle 只能用小写字母、数字、下划线，例如 `my_review_bot`

返回示例：
```json
{
  "botId": "xxx",
  "email": "你的handle@sendclaw.com",
  "apiKey": "sk_xxx",
  "claimToken": "xxxx-XXXX"
}
```

填入 `secrets.json`：
- `sendclaw.api_key` → `apiKey`
- `sendclaw.email` → `email`
- `sendclaw.bot_id` → `botId`
- `review.zapier_email` → `email`（同上，作为审核回复地址）

**验证账号（可选但推荐）：**
1. 访问 https://sendclaw.com/dashboard
2. 注册/登录账号
3. 输入 `claimToken` 验证 Bot，解锁更高限额

### 3. Moonshot API（LLM 生成）
- 注册：https://platform.moonshot.cn
- 拿到 API Key 填入 `secrets.json` → `moonshot.api_key`
- 或者通过 OpenClaw 内置配置（`openclaw configure --section llm`）

### 4. 微信公众号
- 登录微信公众平台：https://mp.weixin.qq.com
- 开发 → 基本配置 → 拿到 AppID 和 AppSecret
- 填入 `secrets.json` → `wechat`

### 5. 163 邮箱 SMTP
- 登录 163 邮箱 → 设置 → POP3/SMTP/IMAP
- 开启 SMTP 服务，生成授权码
- 填入 `secrets.json` → `smtp.pass`（填授权码，不是登录密码）

---

## 四、运行

```bash
# 手动指定主题
python3 pipeline_v3.py --topic "你的主题"

# 使用配置文件中的 weekly_focus（待实现）
python3 pipeline_v3.py

# 自动从热点选题（待实现）
python3 pipeline_v3.py --auto
```

---

## 五、审核流程

1. 运行后，审核邮件发送到 `review.recipient`
2. 邮件包含：本期主题、文献集合、3 篇候选文章
3. **回复审核意见**：直接回复邮件（Reply-To 自动指向 SendClaw 地址）
4. 回复格式：
   - `选A` / `选B` / `选C` — 选择发布哪篇
   - `修改1 [意见]` — 修改指定候选
   - `重新生成 [方向]` — 按新方向重写
5. Agent 通过 heartbeat 定时轮询 SendClaw，自动处理回复

---

## 六、定时运行（可选）

```bash
# 编辑 crontab
crontab -e

# 每天早上 8 点自动运行
0 8 * * * cd /path/to/content-pipeline && python3 pipeline_v3.py >> logs/cron.log 2>&1
```

---

## 七、迁移到新实例

1. `git clone` 仓库
2. 安装依赖
3. 复制并填写 `secrets.json`（所有配置在这一个文件里）
4. SendClaw 账号跟你走，新实例只需填入同一个 API Key

**无需重新配置任何第三方服务。**
