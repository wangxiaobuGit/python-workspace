# AI 工具导航网站

一个基于 Flask 的 AI 工具导航网站，帮助用户发现和使用各种优秀的人工智能工具。

## 🌟 功能特性

### 核心功能
- **工具展示**: 精美的卡片式布局展示 AI 工具
- **分类浏览**: 按功能分类（图像生成、写作助手、编程辅助等）
- **搜索功能**: 支持工具名称、描述、标签的全文搜索
- **工具详情**: 详细的工具介绍页面，包含评分、标签、使用指南
- **管理后台**: 完整的 CRUD 操作，支持添加、编辑、删除工具

### 界面特性
- **响应式设计**: 完美适配桌面端和移动端
- **现代化 UI**: 基于 Bootstrap 5 的美观界面
- **深色主题**: 支持浅色/深色主题切换
- **动画效果**: 流畅的过渡动画和交互效果
- **图标支持**: 丰富的 Bootstrap Icons 图标

### 技术特性
- **Flask 框架**: 轻量级 Python Web 框架
- **JSON 数据存储**: 简单易用的数据管理
- **模板引擎**: Jinja2 模板渲染
- **静态资源**: 优化的 CSS 和 JavaScript
- **SEO 友好**: 良好的页面结构和元数据

## 🚀 快速开始

### 环境要求
- Python 3.7+
- pip 包管理器

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd ai-tools-navigator
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **运行应用**
```bash
python app.py
```

4. **访问网站**
打开浏览器访问 `http://localhost:12000`

### Docker 部署（可选）

1. **构建镜像**
```bash
docker build -t ai-tools-navigator .
```

2. **运行容器**
```bash
docker run -p 12000:12000 ai-tools-navigator
```

## 📁 项目结构

```
ai-tools-navigator/
├── app.py                 # Flask 应用主文件
├── requirements.txt       # Python 依赖
├── README.md             # 项目说明
├── Dockerfile            # Docker 配置
├── data/
│   └── ai_tools.json     # 工具数据文件
├── templates/            # HTML 模板
│   ├── base.html         # 基础模板
│   ├── index.html        # 首页
│   ├── category.html     # 分类页面
│   ├── tool_detail.html  # 工具详情
│   ├── search.html       # 搜索页面
│   ├── admin.html        # 管理后台
│   ├── admin_add_tool.html    # 添加工具
│   └── admin_edit_tool.html   # 编辑工具
└── static/               # 静态文件
    ├── css/
    │   └── style.css     # 自定义样式
    ├── js/
    │   └── main.js       # JavaScript 功能
    └── images/           # 图片资源
```

## 🎯 页面功能

### 首页 (/)
- 展示热门推荐工具
- 分类快速导航
- 高评分工具展示
- 统计数据概览

### 分类页面 (/category/<name>)
- 按分类展示工具列表
- 支持排序和筛选
- 网格/列表视图切换
- 相关分类推荐

### 工具详情 (/tool/<id>)
- 详细的工具信息
- 评分和标签展示
- 使用指南
- 相关工具推荐
- 分享和收藏功能

### 搜索页面 (/search)
- 全文搜索功能
- 搜索结果排序
- 热门搜索推荐
- 搜索历史记录

### 管理后台 (/admin)
- 工具列表管理
- 添加新工具
- 编辑工具信息
- 删除工具
- 数据统计

## 🔧 配置说明

### 数据文件格式
工具数据存储在 `data/ai_tools.json` 文件中，格式如下：

```json
{
  "tools": [
    {
      "id": 1,
      "name": "工具名称",
      "description": "工具描述",
      "url": "https://example.com",
      "category": "分类名称",
      "tags": ["标签1", "标签2"],
      "rating": 4.5,
      "is_featured": true,
      "logo": "https://example.com/logo.png"
    }
  ],
  "categories": [
    {
      "name": "分类名称",
      "description": "分类描述",
      "icon": "🎨"
    }
  ]
}
```

### 环境变量
可以通过环境变量配置应用：

- `FLASK_ENV`: 运行环境 (development/production)
- `FLASK_DEBUG`: 调试模式 (True/False)
- `PORT`: 端口号 (默认 12000)

## 🎨 自定义主题

### 修改颜色主题
编辑 `static/css/style.css` 文件中的 CSS 变量：

```css
:root {
    --primary-color: #0d6efd;
    --secondary-color: #6c757d;
    /* 其他颜色变量 */
}
```

### 添加新功能
1. 在 `app.py` 中添加路由
2. 创建对应的 HTML 模板
3. 更新导航菜单
4. 添加必要的 CSS 和 JavaScript

## 📱 移动端适配

网站采用响应式设计，自动适配不同屏幕尺寸：

- **桌面端**: 完整功能和布局
- **平板端**: 优化的卡片布局
- **手机端**: 简化的界面和触摸友好的交互

## 🔒 安全考虑

- 输入验证和过滤
- XSS 防护
- CSRF 保护（生产环境建议启用）
- 文件上传安全（如需要）

## 🚀 性能优化

- 图片懒加载
- CSS/JS 压缩
- 缓存策略
- CDN 加速（Bootstrap、图标等）

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [Flask](https://flask.palletsprojects.com/) - Web 框架
- [Bootstrap](https://getbootstrap.com/) - UI 框架
- [Bootstrap Icons](https://icons.getbootstrap.com/) - 图标库
- 所有贡献者和用户

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue
- 发送邮件
- 社交媒体

---

**享受探索 AI 工具的乐趣！** 🤖✨