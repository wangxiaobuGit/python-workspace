#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Trending 爬虫模块
用于获取 GitHub 热门项目数据
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

        # 创建存储目录
        os.makedirs(data_dir, exist_ok=True)

    def _get_date_from_since(self, since: str) -> str:
        if since == "daily":
            return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        elif since == "weekly":
            return (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        else:
            return (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

    def get_trending_repos(self, language: str = "", since: str = "weekly", limit: int = 10) -> List[Dict]:
        """
        获取 GitHub 热门仓库（默认按一周热度）
        """
        try:
            date_from = self._get_date_from_since(since)
            query = f"created:>{date_from}"
            if language:
                query += f" language:{language}"

            params = {
                "q": query,
                "sort": "stars",
                "order": "desc",
                "per_page": limit
            }

            response = requests.get(f"{self.api_base}/search/repositories",
                                    headers=self.headers,
                                    params=params,
                                    timeout=10)

            if response.status_code == 200:
                items = response.json().get("items", [])
                return [{
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
                } for item in items]
            else:
                print(f"[Error] GitHub API 请求失败，状态码：{response.status_code}")
                return []
        except Exception as e:
            print(f"[Exception] 获取 GitHub 热门仓库失败：{e}")
            return []

    def get_trending_by_topics(self, topics: List[str], limit: int = 5) -> Dict[str, List[Dict]]:
        """
        根据主题获取热门仓库
        """
        results = {}
        date_from = self._get_date_from_since("weekly")

        for topic in topics:
            try:
                query = f"topic:{topic} created:>{date_from}"
                params = {
                    "q": query,
                    "sort": "stars",
                    "order": "desc",
                    "per_page": limit
                }

                response = requests.get(f"{self.api_base}/search/repositories",
                                        headers=self.headers,
                                        params=params,
                                        timeout=10)

                if response.status_code == 200:
                    items = response.json().get("items", [])
                    results[topic] = [{
                        "id": item["id"],
                        "name": item["name"],
                        "full_name": item["full_name"],
                        "description": item["description"] or "暂无描述",
                        "url": item["html_url"],
                        "stars": item["stargazers_count"],
                        "language": item["language"] or "Unknown",
                        "topics": item.get("topics", [])
                    } for item in items]
                else:
                    print(f"[Error] 请求主题 {topic} 热门项目失败，状态码: {response.status_code}")
                    results[topic] = []

                time.sleep(0.5)  # 防 API 限流

            except Exception as e:
                print(f"[Exception] 获取主题 {topic} 热门仓库失败：{e}")
                results[topic] = []

        return results

    def save_trending_data(self, data: Dict) -> bool:
        """保存热门数据到本地文件"""
        try:
            data["last_updated"] = datetime.now().isoformat()
            with open(self.trending_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"[Error] 保存热门数据失败：{e}")
            return False

    def load_trending_data(self) -> Dict:
        """从文件加载数据"""
        try:
            if os.path.exists(self.trending_file):
                with open(self.trending_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {"daily": [], "topics": {}, "last_updated": None}
        except Exception as e:
            print(f"[Error] 加载数据失败：{e}")
            return {"daily": [], "topics": {}, "last_updated": None}

    def is_data_fresh(self, max_age_hours: int = 6) -> bool:
        """检查缓存数据是否仍然新鲜"""
        data = self.load_trending_data()
        last_updated = data.get("last_updated")

        if not last_updated:
            return False

        try:
            last_time = datetime.fromisoformat(last_updated)
            return (datetime.now() - last_time).total_seconds() < max_age_hours * 3600
        except:
            return False

    def update_trending_data(self, force: bool = False) -> bool:
        """更新数据（如果未过期则跳过，除非 force=True）"""
        if not force and self.is_data_fresh():
            print("✅ 数据仍新鲜，跳过更新。")
            return True

        print("🔄 正在更新 GitHub 热门项目数据...")

        daily_repos = self.get_trending_repos(since="weekly", limit=10)

        topics = ["artificial-intelligence", "machine-learning", "deep-learning",
                  "python", "javascript", "react", "vue", "nodejs"]
        topic_data = self.get_trending_by_topics(topics, limit=3)

        trending_data = {
            "daily": daily_repos,
            "topics": topic_data,
            "last_updated": datetime.now().isoformat()
        }

        if self.save_trending_data(trending_data):
            print(f"✅ 成功更新 GitHub 热门数据，共获取 {len(daily_repos)} 个项目。")
            return True
        else:
            print("❌ 数据保存失败。")
            return False


def main():
    crawler = GitHubTrendingCrawler()
    crawler.update_trending_data(force=True)


if __name__ == "__main__":
    main()
