# Content Review Mail System

通过邮件实现内容审核的双向通信系统。

## 功能特性

- ✅ **发送审核邮件** - 发送包含多候选文章的 HTML 邮件
- ✅ **解析回复指令** - 自动识别发布/重新生成/修改/跳过等指令
- ✅ **邮件双向对话** - 支持多轮邮件讨论和迭代
- ✅ **状态管理** - 记录待审核项目、处理历史
- ✅ **灵活配置** - 支持 Gmail/Outlook/163 等主流邮箱

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置邮箱

复制示例配置并编辑：

```bash
cp config/config.example.json config/config.json
# 编辑 config/config.json，填入你的邮箱信息
```

配置说明：

**Gmail：**
1. 开启两步验证
2. 生成应用专用密码
3. 使用应用密码代替邮箱密码

**163/QQ 邮箱：**
1. 设置 → 账户 → 开启 IMAP/SMTP 服务
2. 获取授权码（16位）

### 3. 发送审核邮件

```python
from content_review_mail import ContentReviewMail

crm = ContentReviewMail()

# 准备候选文章
candidates = [
    {
        'topic': '文章标题1',
        'angle_type': '实战派',
        'quality_score': 8.5,
        'uniqueness_score': 7.5,
        'word_count': 1500,
        'content': '文章内容...'
    },
    {
        'topic': '文章标题2',
        'angle_type': '深度派',
        'quality_score': 7.5,
        'uniqueness_score': 8.0,
        'word_count': 1800,
        'content': '文章内容...'
    }
]

# 发送审核邮件
result = crm.send_review_email(
    topic='AI Agent 发展趋势',
    candidates=candidates,
    to_email='reviewer@example.com'
)
print(f"邮件已发送: {result['message_id']}")
```

### 4. 检查审核回复

```python
# 检查新回复
responses = crm.check_replies()
for response in responses:
    print(f"收到回复: {response['action']} - {response['selected_index']}")
```

### 5. 启动自动监听

```bash
python scripts/content_review_mail.py
```

## 指令格式

回复邮件支持以下指令：

- `PUBLISH 1` - 发布第1个候选
- `REGEN 2` - 重新生成第2个候选
- `MODIFY 1: 新标题\n新内容` - 修改第1个候选
- `SKIP` - 跳过本次审核
- `DISCUSS: 问题描述` - 进入讨论模式

## 项目结构

```
content-review-mail/
├── config/
│   ├── config.example.json    # 配置示例
│   └── config.json            # 实际配置（不提交到git）
├── scripts/
│   ├── content_review_mail.py # 主程序
│   ├── send_review.py         # 发送审核示例
│   └── check_replies.py       # 检查回复示例
├── state/
│   └── mail_state.json        # 状态文件（自动创建）
├── logs/
│   └── *.log                  # 日志文件
├── README.md
├── requirements.txt
└── .gitignore
```

## 使用场景

1. **内容生成后审核** - AI 生成多版本内容，人工审核选择
2. **多轮迭代优化** - 根据反馈反复修改直到满意
3. **异步审核流程** - 发送邮件后无需等待，收到回复后自动处理
4. **移动端审核** - 直接在邮件客户端完成审核操作

## 注意事项

- 请妥善保管 `config/config.json`，包含邮箱密码等敏感信息
- 生产环境建议使用应用专用密码而非主密码
- 定期检查 `logs/` 目录下的日志文件

## License

MIT
