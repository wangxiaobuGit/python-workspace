from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import json
import os
from datetime import datetime
import uuid
from github_trending import GitHubTrendingCrawler
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)
app.secret_key = 'ai-tools-navigator-secret-key-v1-enhanced'

# 数据文件路径
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'ai_tools.json')

# 初始化GitHub爬虫
github_crawler = GitHubTrendingCrawler(data_dir=os.path.join(os.path.dirname(__file__), 'data'))

# 初始化定时任务调度器
scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

def load_data():
    """加载 AI 工具数据"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"tools": [], "categories": []}

def save_data(data):
    """保存 AI 工具数据"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_tool_by_id(tool_id):
    """根据 ID 获取工具"""
    data = load_data()
    for tool in data['tools']:
        if tool['id'] == tool_id:
            return tool
    return None

def get_statistics():
    """获取网站统计信息"""
    data = load_data()
    stats = {
        'total_tools': len(data['tools']),
        'total_categories': len(data['categories']),
        'featured_tools': len([t for t in data['tools'] if t.get('is_featured', False)]),
        'avg_rating': round(sum(t.get('rating', 0) for t in data['tools']) / len(data['tools']) if data['tools'] else 0, 1)
    }
    return stats

def get_tools_by_category(category_name, limit=None):
    """根据分类获取工具"""
    data = load_data()
    tools = [tool for tool in data['tools'] if tool['category'] == category_name]
    if limit:
        tools = tools[:limit]
    return tools

def get_tools_by_region(region, limit=None):
    """根据地区获取工具"""
    data = load_data()
    tools = [tool for tool in data['tools'] if tool.get('region') == region]
    if limit:
        tools = tools[:limit]
    return tools

def get_featured_tools_by_category(category_name, limit=None):
    """获取指定分类的推荐工具"""
    data = load_data()
    tools = [tool for tool in data['tools'] 
             if tool['category'] == category_name and tool.get('is_featured', False)]
    if limit:
        tools = tools[:limit]
    return tools

def update_github_trending():
    """更新GitHub热门数据的定时任务"""
    try:
        github_crawler.update_trending_data()
        print("GitHub热门数据更新成功")
    except Exception as e:
        print(f"GitHub热门数据更新失败: {str(e)}")

# 添加定时任务：每6小时更新一次GitHub热门数据
scheduler.add_job(
    func=update_github_trending,
    trigger="interval",
    hours=6,
    id='github_trending_job'
)

@app.route('/')
def index():
    """首页 - 展示热门 AI 工具"""
    data = load_data()
    
    # 热门推荐工具
    featured_tools = [tool for tool in data['tools'] if tool.get('is_featured', False)][:6]
    
    # 最新更新（按评分排序）
    recent_tools = sorted(data['tools'], key=lambda x: x.get('rating', 0), reverse=True)[:6]
    
    # 中文工具专区
    chinese_tools = get_tools_by_category('中文AI工具', limit=6)
    
    # 开发者工具
    dev_tools = get_tools_by_category('开发者工具', limit=6)
    
    # 视频平台推荐
    video_platforms = get_tools_by_category('视频平台', limit=4)
    
    # 音乐平台推荐
    music_platforms = get_tools_by_category('音乐平台', limit=4)
    
    # 文档笔记工具
    doc_tools = get_tools_by_category('文档笔记', limit=4)
    
    # 生活实用工具
    life_tools = get_tools_by_category('生活实用', limit=4)
    
    # GitHub热门项目
    github_trending = github_crawler.load_trending_data()
    
    categories = data['categories']
    stats = get_statistics()
    
    return render_template('index.html', 
                         featured_tools=featured_tools,
                         recent_tools=recent_tools,
                         chinese_tools=chinese_tools,
                         dev_tools=dev_tools,
                         video_platforms=video_platforms,
                         music_platforms=music_platforms,
                         doc_tools=doc_tools,
                         life_tools=life_tools,
                         github_trending=github_trending,
                         categories=categories,
                         stats=stats)

@app.route('/category/<category_name>')
def category(category_name):
    """分类页面 - 支持排序和分页"""
    data = load_data()
    price_type = request.args.get('price_type', '')
    min_rating = request.args.get('min_rating', type=float)
    sort_by = request.args.get('sort_by', 'rating')
    page = request.args.get('page', 1, type=int)
    per_page = 12

    # 筛选分类
    tools = [tool for tool in data['tools'] if tool['category'] == category_name]

    # 价格类型筛选
    if price_type:
        tools = [tool for tool in tools if tool.get('price_type') == price_type]

    # 评分筛选
    if min_rating:
        tools = [tool for tool in tools if tool.get('rating', 0) >= min_rating]

    # 排序
    if sort_by == 'rating':
        tools.sort(key=lambda x: x.get('rating', 0), reverse=True)
    elif sort_by == 'views':
        tools.sort(key=lambda x: x.get('views', 0), reverse=True)
    elif sort_by == 'updated_at':
        tools.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
    elif sort_by == 'name':
        tools.sort(key=lambda x: x['name'].lower())

    # 分页
    total_tools = len(tools)
    total_pages = (total_tools + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    tools_page = tools[start:end]

    categories = data['categories']
    current_category = next((cat for cat in categories if cat['name'] == category_name), None)

    # 获取所有价格类型
    price_types = sorted(list(set(tool.get('price_type', '免费') for tool in data['tools'])))

    return render_template('category.html',
                         tools=tools_page,
                         category_name=category_name,
                         current_category=current_category,
                         categories=categories,
                         price_types=price_types,
                         total_tools=total_tools,
                         page=page,
                         total_pages=total_pages,
                         current_price_type=price_type,
                         current_min_rating=min_rating,
                         current_sort_by=sort_by)

@app.route('/tool/<int:tool_id>')
def tool_detail(tool_id):
    """工具详情页"""
    tool = get_tool_by_id(tool_id)
    if not tool:
        return redirect(url_for('index'))
    
    data = load_data()
    # 获取相关工具（同分类的其他工具）
    related_tools = [t for t in data['tools'] 
                    if t['category'] == tool['category'] and t['id'] != tool_id][:4]
    
    return render_template('tool_detail.html',
                         tool=tool,
                         related_tools=related_tools)

@app.route('/search')
def search():
    """搜索页面 - 支持高级筛选、排序和分页"""
    query = request.args.get('q', '').strip()
    category = request.args.get('category', '')
    price_type = request.args.get('price_type', '')
    min_rating = request.args.get('min_rating', type=float)
    sort_by = request.args.get('sort_by', 'rating')  # rating, views, updated_at, name
    page = request.args.get('page', 1, type=int)
    per_page = 12

    data = load_data()
    results = data['tools'].copy()

    # 文本搜索
    if query:
        results = [tool for tool in results if (
            query.lower() in tool['name'].lower() or
            query.lower() in tool['description'].lower() or
            any(query.lower() in tag.lower() for tag in tool['tags'])
        )]

    # 分类筛选
    if category:
        results = [tool for tool in results if tool['category'] == category]

    # 价格类型筛选
    if price_type:
        results = [tool for tool in results if tool.get('price_type') == price_type]

    # 评分筛选
    if min_rating:
        results = [tool for tool in results if tool.get('rating', 0) >= min_rating]

    # 排序
    if sort_by == 'rating':
        results.sort(key=lambda x: x.get('rating', 0), reverse=True)
    elif sort_by == 'views':
        results.sort(key=lambda x: x.get('views', 0), reverse=True)
    elif sort_by == 'updated_at':
        results.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
    elif sort_by == 'name':
        results.sort(key=lambda x: x['name'].lower())

    # 分页
    total_results = len(results)
    total_pages = (total_results + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    results_page = results[start:end]

    # 获取所有价格类型（用于筛选器）
    price_types = sorted(list(set(tool.get('price_type', '免费') for tool in data['tools'])))

    return render_template('search.html',
                         query=query,
                         results=results_page,
                         categories=data['categories'],
                         price_types=price_types,
                         total_results=total_results,
                         page=page,
                         total_pages=total_pages,
                         per_page=per_page,
                         # 当前筛选条件
                         current_category=category,
                         current_price_type=price_type,
                         current_min_rating=min_rating,
                         current_sort_by=sort_by)

@app.route('/admin')
def admin():
    """管理后台首页"""
    data = load_data()
    return render_template('admin.html',
                         tools=data['tools'],
                         categories=data['categories'])

@app.route('/admin/tool/add', methods=['GET', 'POST'])
def admin_add_tool():
    """添加工具"""
    if request.method == 'POST':
        data = load_data()
        
        # 生成新的 ID
        max_id = max([tool['id'] for tool in data['tools']], default=0)
        new_id = max_id + 1
        
        new_tool = {
            'id': new_id,
            'name': request.form['name'],
            'description': request.form['description'],
            'url': request.form['url'],
            'category': request.form['category'],
            'tags': [tag.strip() for tag in request.form['tags'].split(',') if tag.strip()],
            'rating': float(request.form['rating']),
            'is_featured': 'is_featured' in request.form,
            'logo': request.form['logo'] or 'https://via.placeholder.com/64'
        }
        
        data['tools'].append(new_tool)
        save_data(data)
        
        return redirect(url_for('admin'))
    
    data = load_data()
    return render_template('admin_add_tool.html', categories=data['categories'])

@app.route('/admin/tool/<int:tool_id>/edit', methods=['GET', 'POST'])
def admin_edit_tool(tool_id):
    """编辑工具"""
    data = load_data()
    tool = get_tool_by_id(tool_id)
    
    if not tool:
        return redirect(url_for('admin'))
    
    if request.method == 'POST':
        tool['name'] = request.form['name']
        tool['description'] = request.form['description']
        tool['url'] = request.form['url']
        tool['category'] = request.form['category']
        tool['tags'] = [tag.strip() for tag in request.form['tags'].split(',') if tag.strip()]
        tool['rating'] = float(request.form['rating'])
        tool['is_featured'] = 'is_featured' in request.form
        tool['logo'] = request.form['logo'] or tool.get('logo', 'https://via.placeholder.com/64')
        
        save_data(data)
        return redirect(url_for('admin'))
    
    return render_template('admin_edit_tool.html', tool=tool, categories=data['categories'])

@app.route('/admin/tool/<int:tool_id>/delete', methods=['POST'])
def admin_delete_tool(tool_id):
    """删除工具"""
    data = load_data()
    data['tools'] = [tool for tool in data['tools'] if tool['id'] != tool_id]
    save_data(data)
    return redirect(url_for('admin'))

@app.route('/api/tools')
def api_tools():
    """API: 获取所有工具"""
    data = load_data()
    return jsonify(data['tools'])

@app.route('/api/categories')
def api_categories():
    """API: 获取所有分类"""
    data = load_data()
    return jsonify(data['categories'])

@app.route('/api/search')
def api_search():
    """API: 搜索工具"""
    query = request.args.get('q', '').strip()
    data = load_data()
    
    if query:
        results = []
        for tool in data['tools']:
            if (query.lower() in tool['name'].lower() or 
                query.lower() in tool['description'].lower() or
                any(query.lower() in tag.lower() for tag in tool['tags'])):
                results.append(tool)
    else:
        results = data['tools']
    
    return jsonify(results)

@app.route('/api/stats')
def api_stats():
    """API: 获取网站统计信息"""
    stats = get_statistics()
    return jsonify(stats)

@app.route('/api/tools/random')
def api_random_tools():
    """API: 获取随机推荐工具"""
    data = load_data()
    import random
    random_tools = random.sample(data['tools'], min(3, len(data['tools'])))
    return jsonify(random_tools)

@app.route('/api/github/trending')
def api_github_trending():
    """API: 获取GitHub热门项目"""
    trending_data = github_crawler.load_trending_data()
    return jsonify(trending_data)

@app.route('/api/tools/category/<category_name>')
def api_tools_by_category(category_name):
    """API: 根据分类获取工具"""
    limit = request.args.get('limit', type=int)
    tools = get_tools_by_category(category_name, limit)
    return jsonify(tools)

@app.route('/api/tools/region/<region>')
def api_tools_by_region(region):
    """API: 根据地区获取工具"""
    limit = request.args.get('limit', type=int)
    tools = get_tools_by_region(region, limit)
    return jsonify(tools)

@app.route('/admin/github/update', methods=['POST'])
def admin_update_github():
    """管理后台：手动更新GitHub热门数据"""
    try:
        success = github_crawler.update_trending_data(force=True)
        if success:
            flash('GitHub热门数据更新成功', 'success')
        else:
            flash('GitHub热门数据更新失败', 'error')
    except Exception as e:
        flash(f'更新失败: {str(e)}', 'error')
    
    return redirect(url_for('admin'))

if __name__ == '__main__':
    # 确保数据目录存在
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    # 启动应用
    app.run(host='0.0.0.0', port=12001, debug=True)