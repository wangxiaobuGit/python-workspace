// 主要 JavaScript 功能

document.addEventListener('DOMContentLoaded', function() {
    // 初始化主题
    initTheme();
    
    // 初始化工具提示
    initTooltips();
    
    // 初始化图片懒加载
    initLazyLoading();
    
    // 初始化搜索功能
    initSearch();
    
    // 初始化动画
    initAnimations();
});

// 主题切换功能
function initTheme() {
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    const html = document.documentElement;
    
    // 获取保存的主题
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
    
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = html.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            setTheme(newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }
    
    function setTheme(theme) {
        html.setAttribute('data-bs-theme', theme);
        if (themeIcon) {
            themeIcon.className = theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
        }
    }
}

// 初始化工具提示
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// 图片懒加载
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    } else {
        // 降级处理
        images.forEach(img => {
            img.src = img.dataset.src;
        });
    }
}

// 搜索功能增强
function initSearch() {
    const searchInput = document.querySelector('input[name="q"]');
    if (searchInput) {
        // 搜索建议
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                showSearchSuggestions(this.value);
            }, 300);
        });
        
        // 搜索历史
        loadSearchHistory();
    }
}

// 显示搜索建议
function showSearchSuggestions(query) {
    if (query.length < 2) return;
    
    // 这里可以调用 API 获取搜索建议
    // 暂时使用静态数据
    const suggestions = [
        'ChatGPT', 'Midjourney', 'GitHub Copilot', 'Stable Diffusion',
        '图像生成', '写作助手', '编程辅助', '音频处理'
    ].filter(item => item.toLowerCase().includes(query.toLowerCase()));
    
    // 显示建议（可以实现下拉菜单）
    console.log('搜索建议:', suggestions);
}

// 加载搜索历史
function loadSearchHistory() {
    const history = JSON.parse(localStorage.getItem('searchHistory') || '[]');
    // 可以在搜索页面显示历史记录
}

// 保存搜索历史
function saveSearchHistory(query) {
    if (!query.trim()) return;
    
    let history = JSON.parse(localStorage.getItem('searchHistory') || '[]');
    history = history.filter(item => item !== query); // 去重
    history.unshift(query); // 添加到开头
    history = history.slice(0, 10); // 只保留最近10条
    
    localStorage.setItem('searchHistory', JSON.stringify(history));
}

// 动画初始化
function initAnimations() {
    // 滚动动画
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);
    
    // 观察所有卡片
    document.querySelectorAll('.card').forEach(card => {
        observer.observe(card);
    });
}

// 工具卡片交互
function initToolCards() {
    const toolCards = document.querySelectorAll('.tool-card');
    
    toolCards.forEach(card => {
        // 鼠标悬停效果
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
        
        // 点击效果
        card.addEventListener('click', function(e) {
            if (e.target.tagName !== 'A' && e.target.tagName !== 'BUTTON') {
                const detailLink = this.querySelector('a[href*="/tool/"]');
                if (detailLink) {
                    window.location.href = detailLink.href;
                }
            }
        });
    });
}

// 表单验证增强
function enhanceFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!this.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
                
                // 显示第一个错误字段
                const firstInvalid = this.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                    showToast('请检查表单中的错误', 'error');
                }
            }
            
            this.classList.add('was-validated');
        });
        
        // 实时验证
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (this.checkValidity()) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                } else {
                    this.classList.remove('is-valid');
                    this.classList.add('is-invalid');
                }
            });
        });
    });
}

// 显示提示消息
function showToast(message, type = 'info') {
    // 创建 toast 元素
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    // 添加到页面
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }
    
    toastContainer.appendChild(toast);
    
    // 显示 toast
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    // 自动移除
    toast.addEventListener('hidden.bs.toast', function() {
        this.remove();
    });
}

// 复制到剪贴板
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showToast('已复制到剪贴板', 'success');
        }).catch(() => {
            showToast('复制失败', 'error');
        });
    } else {
        // 降级处理
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            showToast('已复制到剪贴板', 'success');
        } catch (err) {
            showToast('复制失败', 'error');
        }
        document.body.removeChild(textArea);
    }
}

// 分享功能
function shareUrl(title, text, url) {
    if (navigator.share) {
        navigator.share({
            title: title,
            text: text,
            url: url || window.location.href
        }).catch(err => {
            console.log('分享失败:', err);
            copyToClipboard(url || window.location.href);
        });
    } else {
        copyToClipboard(url || window.location.href);
    }
}

// 收藏功能
function toggleFavorite(toolId) {
    let favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
    
    if (favorites.includes(toolId)) {
        favorites = favorites.filter(id => id !== toolId);
        showToast('已取消收藏', 'info');
    } else {
        favorites.push(toolId);
        showToast('已添加到收藏', 'success');
    }
    
    localStorage.setItem('favorites', JSON.stringify(favorites));
    updateFavoriteButtons();
}

// 更新收藏按钮状态
function updateFavoriteButtons() {
    const favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
    const favoriteButtons = document.querySelectorAll('[data-tool-id]');
    
    favoriteButtons.forEach(button => {
        const toolId = parseInt(button.dataset.toolId);
        const icon = button.querySelector('i');
        
        if (favorites.includes(toolId)) {
            icon.className = 'bi bi-heart-fill me-2';
            button.classList.add('btn-danger');
            button.classList.remove('btn-outline-secondary');
        } else {
            icon.className = 'bi bi-heart me-2';
            button.classList.add('btn-outline-secondary');
            button.classList.remove('btn-danger');
        }
    });
}

// 图片加载错误处理
function handleImageError(img) {
    img.src = 'https://via.placeholder.com/64?text=Logo';
    img.onerror = null; // 防止无限循环
}

// 平滑滚动
function smoothScrollTo(target) {
    const element = document.querySelector(target);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// 返回顶部
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// 显示返回顶部按钮
function initBackToTop() {
    const backToTopBtn = document.createElement('button');
    backToTopBtn.innerHTML = '<i class="bi bi-arrow-up"></i>';
    backToTopBtn.className = 'btn btn-primary position-fixed bottom-0 end-0 m-3 rounded-circle';
    backToTopBtn.style.display = 'none';
    backToTopBtn.style.zIndex = '1050';
    backToTopBtn.onclick = scrollToTop;
    
    document.body.appendChild(backToTopBtn);
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.style.display = 'block';
        } else {
            backToTopBtn.style.display = 'none';
        }
    });
}

// 键盘快捷键
function initKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K 打开搜索
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('input[name="q"]');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // ESC 关闭模态框
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal.show');
            if (openModal) {
                const modal = bootstrap.Modal.getInstance(openModal);
                if (modal) modal.hide();
            }
        }
    });
}

// 性能监控
function initPerformanceMonitoring() {
    // 页面加载时间
    window.addEventListener('load', function() {
        const loadTime = performance.now();
        console.log(`页面加载时间: ${loadTime.toFixed(2)}ms`);
    });
    
    // 监控长任务
    if ('PerformanceObserver' in window) {
        const observer = new PerformanceObserver((list) => {
            list.getEntries().forEach((entry) => {
                if (entry.duration > 50) {
                    console.warn(`长任务检测: ${entry.duration.toFixed(2)}ms`);
                }
            });
        });
        
        observer.observe({ entryTypes: ['longtask'] });
    }
}

// 错误处理
window.addEventListener('error', function(e) {
    console.error('JavaScript 错误:', e.error);
    // 可以发送错误报告到服务器
});

// 初始化所有功能
document.addEventListener('DOMContentLoaded', function() {
    initToolCards();
    enhanceFormValidation();
    updateFavoriteButtons();
    initBackToTop();
    initKeyboardShortcuts();
    initPerformanceMonitoring();
});

// 动态加载统计信息
function loadStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            // 更新统计数字（如果页面有统计元素）
            const statElements = document.querySelectorAll('.stat-item h3');
            if (statElements.length >= 4) {
                statElements[0].textContent = data.total_tools;
                statElements[1].textContent = data.total_categories;
                statElements[2].textContent = data.featured_tools;
                statElements[3].textContent = data.avg_rating;
            }
        })
        .catch(error => console.log('统计信息加载失败:', error));
}

// 加载随机推荐工具
function loadRandomTools() {
    fetch('/api/tools/random')
        .then(response => response.json())
        .then(tools => {
            console.log('随机推荐工具:', tools);
            // 这里可以添加显示随机工具的逻辑
        })
        .catch(error => console.log('随机工具加载失败:', error));
}

// 页面加载完成后加载统计信息
document.addEventListener('DOMContentLoaded', function() {
    // 如果是首页，加载统计信息
    if (document.querySelector('.stat-item')) {
        loadStats();
    }
});

// 导出全局函数
window.showToast = showToast;
window.copyToClipboard = copyToClipboard;
window.shareUrl = shareUrl;
window.toggleFavorite = toggleFavorite;
window.handleImageError = handleImageError;
window.smoothScrollTo = smoothScrollTo;
window.loadStats = loadStats;
window.loadRandomTools = loadRandomTools;