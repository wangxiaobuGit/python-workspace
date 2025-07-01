#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Trending 爬虫模块
用于获取GitHub热门项目数据
"""

import requests
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time

class GitHubTrendingCrawler:
    """GitHub Trending 爬虫类"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.trending_file = os.path.join(data_dir, "github_trending.json")
        self.api_base = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "AI-Tools-Navigator/1.0"
        }
        
        # 确保数据目录存在
        os.makedirs(data_dir, exist_ok=True)
    
    def get_trending_repos(self, language: str = "", since: str = "daily", limit: int = 10) -> List[Dict]:
        """
        获取GitHub热门仓库
        
        Args:
            language: 编程语言过滤 (可选)
            since: 时间范围 (daily, weekly, monthly)
            limit: 返回数量限制
            
        Returns:
            热门仓库列表
        """
        try:
            # 计算查询日期
            if since == "daily":
                date_from = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            elif since == "weekly":
                date_from = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            else:  # monthly
                date_from = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
            
            # 构建查询参数
            query = f"created:>{date_from}"
            if language:
                query += f" language:{language}"
            
            # API请求参数
            params = {
                "q": query,
                "sort": "stars",
                "order": "desc",
                "per_page": limit
            }
            
            # 发送请求
            response = requests.get(
                f"{self.api_base}/search/repositories",
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                repos = []
                
                for item in data.get("items", []):
                    repo = {
                        "id": item["id"],
                        "name": item["name"],
                        "full_name": item["full_name"],
                        "description": item["description"] or "暂无描述",
                        "url": item["html_url"],
                        "stars": item["stargazers_count"],
                        "forks": item["forks_count"],
                        "language": item["language"] or "Unknown",
                        "created_at": item["created_at"],
                        "updated_at": item["updated_at"],
                        "owner": {
                            "login": item["owner"]["login"],
                            "avatar_url": item["owner"]["avatar_url"]
                        },
                        "topics": item.get("topics", [])
                    }
                    repos.append(repo)
                
                return repos
            else:
                print(f"GitHub API请求失败: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"获取GitHub热门仓库失败: {str(e)}")
            return []
    
    def get_trending_by_topics(self, topics: List[str], limit: int = 5) -> List[Dict]:
        """
        根据主题获取热门仓库
        
        Args:
            topics: 主题列表
            limit: 每个主题的返回数量
            
        Returns:
            按主题分类的热门仓库
        """
        results = {}
        
        for topic in topics:
            try:
                # 构建查询
                date_from = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
                query = f"topic:{topic} created:>{date_from}"
                
                params = {
                    "q": query,
                    "sort": "stars",
                    "order": "desc",
                    "per_page": limit
                }
                
                response = requests.get(
                    f"{self.api_base}/search/repositories",
                    headers=self.headers,
                    params=params,
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    repos = []
                    
                    for item in data.get("items", []):
                        repo = {
                            "id": item["id"],
                            "name": item["name"],
                            "full_name": item["full_name"],
                            "description": item["description"] or "暂无描述",
                            "url": item["html_url"],
                            "stars": item["stargazers_count"],
                            "language": item["language"] or "Unknown",
                            "topics": item.get("topics", [])
                        }
                        repos.append(repo)
                    
                    results[topic] = repos
                
                # 避免API限制
                time.sleep(0.5)
                
            except Exception as e:
                print(f"获取主题 {topic} 的热门仓库失败: {str(e)}")
                results[topic] = []
        
        return results
    
    def save_trending_data(self, data: Dict) -> bool:
        """
        保存热门数据到文件
        
        Args:
            data: 要保存的数据
            
        Returns:
            是否保存成功
        """
        try:
            # 添加时间戳
            data["last_updated"] = datetime.now().isoformat()
            
            with open(self.trending_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"保存热门数据失败: {str(e)}")
            return False
    
    def load_trending_data(self) -> Dict:
        """
        从文件加载热门数据
        
        Returns:
            热门数据字典
        """
        try:
            if os.path.exists(self.trending_file):
                with open(self.trending_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {"daily": [], "topics": {}, "last_updated": None}
        except Exception as e:
            print(f"加载热门数据失败: {str(e)}")
            return {"daily": [], "topics": {}, "last_updated": None}
    
    def is_data_fresh(self, max_age_hours: int = 6) -> bool:
        """
        检查数据是否新鲜
        
        Args:
            max_age_hours: 最大数据年龄（小时）
            
        Returns:
            数据是否新鲜
        """
        data = self.load_trending_data()
        last_updated = data.get("last_updated")
        
        if not last_updated:
            return False
        
        try:
            last_update_time = datetime.fromisoformat(last_updated)
            age = datetime.now() - last_update_time
            return age.total_seconds() < max_age_hours * 3600
        except:
            return False
    
    def update_trending_data(self, force: bool = False) -> bool:
        """
        更新热门数据
        
        Args:
            force: 是否强制更新
            
        Returns:
            是否更新成功
        """
        # 检查是否需要更新
        if not force and self.is_data_fresh():
            print("数据仍然新鲜，跳过更新")
            return True
        
        print("开始更新GitHub热门数据...")
        
        # 获取每日热门
        daily_repos = self.get_trending_repos(since="daily", limit=10)
        
        # 获取特定主题的热门项目
        ai_topics = ["artificial-intelligence", "machine-learning", "deep-learning", 
                    "python", "javascript", "react", "vue", "nodejs"]
        topic_repos = self.get_trending_by_topics(ai_topics, limit=3)
        
        # 构建数据结构
        trending_data = {
            "daily": daily_repos,
            "topics": topic_repos,
            "last_updated": datetime.now().isoformat()
        }
        
        # 保存数据
        success = self.save_trending_data(trending_data)
        
        if success:
            print(f"成功更新GitHub热门数据，共获取 {len(daily_repos)} 个每日热门项目")
        else:
            print("更新GitHub热门数据失败")
        
        return success

def main():
    """主函数，用于测试"""
    crawler = GitHubTrendingCrawler()
    crawler.update_trending_data(force=True)

if __name__ == "__main__":
    main()