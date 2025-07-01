from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'ai-tools-navigator-secret-key'

# 数据文件路径
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'ai_tools.json')

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

@app.route('/')
def index():
    """首页 - 展示热门 AI 工具"""
    data = load_data()
    featured_tools = [tool for tool in data['tools'] if tool.get('is_featured', False)]
    recent_tools = sorted(data['tools'], key=lambda x: x.get('rating', 0), reverse=True)[:6]
    categories = data['categories']
    
    return render_template('index.html', 
                         featured_tools=featured_tools,
                         recent_tools=recent_tools,
                         categories=categories)

@app.route('/category/<category_name>')
def category(category_name):
    """分类页面"""
    data = load_data()
    tools = [tool for tool in data['tools'] if tool['category'] == category_name]
    categories = data['categories']
    
    # 获取当前分类信息
    current_category = next((cat for cat in categories if cat['name'] == category_name), None)
    
    return render_template('category.html',
                         tools=tools,
                         category_name=category_name,
                         current_category=current_category,
                         categories=categories)

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
    """搜索页面"""
    query = request.args.get('q', '').strip()
    data = load_data()
    
    if query:
        # 搜索工具名称、描述和标签
        results = []
        for tool in data['tools']:
            if (query.lower() in tool['name'].lower() or 
                query.lower() in tool['description'].lower() or
                any(query.lower() in tag.lower() for tag in tool['tags'])):
                results.append(tool)
    else:
        results = []
    
    return render_template('search.html',
                         query=query,
                         results=results,
                         categories=data['categories'])

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

if __name__ == '__main__':
    # 确保数据目录存在
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    
    # 启动应用
    app.run(host='0.0.0.0', port=12000, debug=True)