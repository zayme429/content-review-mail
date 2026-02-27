#!/usr/bin/env python3
"""
邮件发送模块 - 发送HTML格式完整文章
已根据反馈优化排版和内容展示
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ReviewMailSender:
    """审核邮件发送器 - 优化版"""
    
    def __init__(self, smtp_config: dict):
        self.smtp = smtp_config
        
    def send_html_review_email(self, to: str, candidates: list, article_date: str) -> bool:
        """
        发送HTML格式的审核邮件（完整文章 + 优化排版）
        
        Args:
            to: 收件人邮箱
            candidates: 候选文章列表（包含完整内容）
            article_date: 文章日期
        """
        try:
            # 构建HTML邮件
            html = self._build_html_email(candidates, article_date)
            
            # 创建邮件
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f'📄 内容审核 - {article_date} ({len(candidates)}篇完整文章)'
            msg['From'] = f"Content Bot <{self.smtp['from']}>"
            msg['To'] = to
            msg['Reply-To'] = 'zaymeclawstart.rpd217@zapiermail.com'  # Zapier邮箱
            
            msg.attach(MIMEText(html, 'html', 'utf-8'))
            
            # 发送
            server = smtplib.SMTP_SSL(self.smtp['host'], self.smtp['port'])
            server.login(self.smtp['user'], self.smtp['pass'])
            server.sendmail(self.smtp['from'], to, msg.as_string())
            server.quit()
            
            logger.info(f"✅ HTML审核邮件已发送到: {to}")
            return True
            
        except Exception as e:
            logger.error(f"❌ 发送邮件失败: {e}")
            return False
    
    def _build_html_email(self, candidates: list, article_date: str) -> str:
        """构建HTML邮件内容"""
        
        # 构建候选文章HTML
        candidates_html = ""
        for i, c in enumerate(candidates, 1):
            # 清理内容中的HTML标签防止冲突
            content = c.get('content', '').replace('<', '&lt;').replace('>', '&gt;')
            
            candidates_html += f"""
            <div class="candidate">
                <div class="candidate-header">
                    <h2>候选 {i}：{c['topic']}</h2>
                    <div class="meta">类型：{c.get('angle_type', '标准')} | 字数：{len(content)}字 | 质量分：{c.get('quality_score', 0)}</div>
                </div>
                <div class="content">{content}</div>
            </div>
            """
        
        # 完整HTML模板
        html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body {{ 
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
    line-height: 1.8; 
    color: #333; 
    max-width: 800px; 
    margin: 0 auto; 
    padding: 20px; 
    background: #f5f7fa; 
}}
.header {{ 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    color: white; 
    padding: 30px; 
    border-radius: 12px; 
    margin-bottom: 30px; 
    text-align: center; 
}}
.header h1 {{ margin: 0; font-size: 24px; }}
.header p {{ margin: 10px 0 0 0; opacity: 0.9; }}
.info-box {{ 
    background: #e7f3ff; 
    border-left: 4px solid #0066cc; 
    padding: 15px 20px; 
    margin: 20px 0; 
    border-radius: 0 8px 8px 0; 
}}
.candidate {{ 
    background: white; 
    border-radius: 12px; 
    padding: 25px; 
    margin: 20px 0; 
    box-shadow: 0 2px 8px rgba(0,0,0,0.1); 
}}
.candidate-header {{ 
    border-bottom: 2px solid #667eea; 
    padding-bottom: 15px; 
    margin-bottom: 20px; 
}}
.candidate h2 {{ 
    color: #667eea; 
    margin: 0 0 10px 0; 
    font-size: 20px; 
}}
.candidate .meta {{ 
    color: #666; 
    font-size: 14px; 
    margin-bottom: 15px; 
}}
.candidate .content {{ 
    font-size: 15px; 
    color: #444; 
    white-space: pre-wrap; 
    line-height: 1.8;
}}
.actions {{ 
    background: #fff3cd; 
    border-left: 4px solid #ffc107; 
    padding: 20px; 
    margin: 30px 0; 
    border-radius: 0 8px 8px 0; 
}}
.actions h3 {{ margin-top: 0; color: #856404; }}
.actions code {{ 
    background: #f8f9fa; 
    padding: 2px 8px; 
    border-radius: 4px; 
    font-family: monospace; 
    font-size: 14px; 
}}
.footer {{ 
    margin-top: 40px; 
    padding-top: 20px; 
    border-top: 2px solid #ddd; 
    color: #999; 
    font-size: 13px; 
    text-align: center; 
}}
</style>
</head>
<body>
<div class="header">
    <h1>📄 内容审核通知</h1>
    <p>{article_date} | {len(candidates)}篇候选文章 | 请审核后回复</p>
</div>

<div class="info-box">
    <strong>💡 系统工作流说明：</strong><br>
    • 接收方式：Zapier Webhook（解决IMAP端口限制）<br>
    • 回复地址：zaymeclawstart.rpd217@zapiermail.com<br>
    • 内容偏好：实战派、配置代码、成本数据（根据反馈固化）<br>
    • 反馈机制：自动记录选择，优化后续生成
</div>

{candidates_html}

<div class="actions">
    <h3>🎯 审核操作指南</h3>
    <p><strong>直接回复此邮件即可：</strong></p>
    <p>• <code>发布 1</code> / <code>发布 2</code> / <code>发布 3</code> — 发布指定候选到微信公众号</p>
    <p>• <code>重新生成 [方向描述]</code> — 按新方向重写（如：重新生成 更侧重实操案例）</p>
    <p>• <code>修改 1 [意见]</code> — 针对性优化（如：修改 1 增加数据支撑）</p>
    <p>• <code>跳过</code> — 今日不发布</p>
</div>

<div class="footer">
    <p>AI内容自动生成系统 v2.0 | 生成时间：{article_date}</p>
    <p>总字数：{sum(len(c.get('content','')) for c in candidates)} 字</p>
</div>
</body>
</html>
"""
        return html


# 兼容性：保留旧的方法名
def send_review_email(to: str, candidates: list, article_date: str, smtp_config: dict) -> bool:
    """兼容旧调用的函数"""
    sender = ReviewMailSender(smtp_config)
    return sender.send_html_review_email(to, candidates, article_date)


if __name__ == '__main__':
    # 测试
    config = {
        'host': 'smtp.163.com',
        'port': 465,
        'user': '13257667003@163.com',
        'pass': 'XUnhjmQwxUa7pKFt',
        'from': '13257667003@163.com'
    }
    
    test_candidates = [
        {
            'topic': '测试文章1',
            'angle_type': '实战派',
            'quality_score': 8.5,
            'content': '这是测试内容...'
        }
    ]
    
    sender = ReviewMailSender(config)
    sender.send_html_review_email('test@example.com', test_candidates, '20260226')
