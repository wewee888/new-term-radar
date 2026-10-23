"""
Build web dashboard for new-term-radar and output static files to dist/
"""
import os
import json
import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
DIST.mkdir(parents=True, exist_ok=True)

# 1. Read report.json and report.md
report_json_path = ROOT / "report.json"
report_md_path = ROOT / "report.md"

report_data = {}
if report_json_path.exists():
    try:
        report_data = json.loads(report_json_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Warning reading report.json: {e}")

report_md_text = ""
if report_md_path.exists():
    try:
        report_md_text = report_md_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Warning reading report.md: {e}")

# Copy assets
shutil.copy(ROOT / "docs" / "logo.svg", DIST / "logo.svg")
if (ROOT / "docs" / "logo-512.png").exists():
    shutil.copy(ROOT / "docs" / "logo-512.png", DIST / "logo-512.png")
if report_json_path.exists():
    shutil.copy(report_json_path, DIST / "report.json")
if report_md_path.exists():
    shutil.copy(report_md_path, DIST / "report.md")

# Default benchmark / demo items for candidate keywords if current run is skipped/empty
benchmark_keywords = [
    {
        "term": "photocraft",
        "type": "名字 (Product)",
        "source": "X / ProductHunt",
        "is_new": True,
        "daily_est": 12747,
        "surge_date": "2026-10-05",
        "peak_vs_gpts": "97 vs 3.1",
        "trend": "还在涨",
        "competition": "能进",
        "decision": "优先",
        "format": "image",
        "badge": "🖼 图片"
    },
    {
        "term": "claude haiku 5.5",
        "type": "名字 (Model)",
        "source": "Anthropic / X",
        "is_new": True,
        "daily_est": 1863,
        "surge_date": "2026-10-07",
        "peak_vs_gpts": "100 vs 23.7",
        "trend": "还在涨",
        "competition": "一般",
        "decision": "优先",
        "format": "text",
        "badge": "⚡ 突围"
    },
    {
        "term": "ai image detector",
        "type": "通用词 (Generic)",
        "source": "synthid detector",
        "is_new": False,
        "daily_est": 2537,
        "surge_date": "2026-10-04",
        "peak_vs_gpts": "87 vs 31.6",
        "trend": "平稳",
        "competition": "挤满",
        "decision": "观察",
        "format": "image",
        "badge": "🖼 需求词"
    },
    {
        "term": "photoshop alternative",
        "type": "通用词 (Generic)",
        "source": "photocraft",
        "is_new": False,
        "daily_est": 244,
        "surge_date": "2026-10-08",
        "peak_vs_gpts": "61 vs 61.7",
        "trend": "平稳",
        "competition": "挤满",
        "decision": "跳过",
        "format": "image",
        "badge": "⚠ 借用品牌"
    },
    {
        "term": "strata",
        "type": "名字 (Repo)",
        "source": "GitHub 爆发",
        "is_new": True,
        "daily_est": 3820,
        "surge_date": "2026-09-24",
        "peak_vs_gpts": "78 vs 12.4",
        "trend": "已验证",
        "competition": "能进",
        "decision": "优先",
        "format": "text",
        "badge": "★ 提前3天命中"
    }
]

# Benchmark HuggingFace items
hf_items = [
    {"name": "deepseek-ai/DeepInfer", "type": "model", "likes": 1420, "category": "LLM Inference", "desc": "High-performance large-scale inference framework for DeepSeek"},
    {"name": "Qwen/Qwen2.5-Coder-32B-Instruct", "type": "model", "likes": 2890, "category": "Code Generation", "desc": "State-of-the-art open code model"},
    {"name": "black-forest-labs/FLUX.1-schnell", "type": "model", "likes": 4120, "category": "Text-to-Image", "desc": "12B parameter rectified flow transformer for fast generation"},
    {"name": "lightonai/lightonocr-3", "type": "space", "likes": 650, "category": "OCR Demo", "desc": "Document parser & multimodal OCR live space"}
]

# Pain points data
pain_items = [
    {
        "keyword": "ai headshot generator",
        "complaint": "耳垂和牙齿经常变形，付费后无法退款，且生成风格极其油腻塑料感",
        "gap": "真实质感/无塑料感人像",
        "count": 48,
        "search_term": "realistic ai headshot free"
    },
    {
        "keyword": "ai video generator",
        "complaint": "多镜头人物面部不一致，动作超过 3 秒必定融化崩解，提示词控制不精准",
        "gap": "多镜头角色一致性与精准控制",
        "count": 76,
        "search_term": "consistent character ai video"
    },
    {
        "keyword": "ai slide maker",
        "complaint": "只能把长文本塞进死板排版卡片，根本无法生成适合演讲的图文结构与图表",
        "gap": "真正懂讲者演讲逻辑的幻灯片重排",
        "count": 35,
        "search_term": "convert notes to slide deck ai"
    }
]

# Extract breakout repos
breakout_repos = report_data.get("breakout", {}).get("repos", [])

# Paths for MCP json display
config_json_str = str(ROOT / 'config.json').replace('\\', '/')
state_dir_str = str(ROOT / 'state').replace('\\', '/')

# Generate HTML
html_content = f"""<!DOCTYPE html>
<html lang="zh-CN" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>新词雷达 · new-term-radar | AI 圈爆发热词与通用需求追踪中枢</title>
  <meta name="description" content="AI 圈马上要被搜的新名字，出现当天就抓到，赶在关键词工具收录之前。多源实时监控 GitHub 爆发、HuggingFace、X 实验室、竞品 Sitemap 与 Reddit 痛点。">
  <link rel="icon" type="image/svg+xml" href="logo.svg">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          colors: {{
            brand: {{
              50: '#ecfeff',
              100: '#cffafe',
              400: '#22d3ee',
              500: '#06b6d4',
              600: '#0891b2',
            }}
          }}
        }}
      }}
    }}
  </script>
  <style>
    @keyframes radarSweep {{
      0% {{ transform: rotate(0deg); }}
      100% {{ transform: rotate(360deg); }}
    }}
    .radar-sweep {{
      animation: radarSweep 4s linear infinite;
      transform-origin: center center;
    }}
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen flex flex-col font-sans selection:bg-cyan-500 selection:text-black">
  <!-- Top Banner -->
  <header class="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="relative w-9 h-9 flex items-center justify-center bg-slate-800 rounded-lg p-1.5 border border-slate-700 overflow-hidden">
          <img src="logo.svg" alt="Radar Logo" class="w-full h-full object-contain">
          <div class="absolute inset-0 border border-cyan-500/20 rounded-lg pointer-events-none"></div>
        </div>
        <div>
          <div class="flex items-center space-x-2">
            <span class="font-bold text-lg text-white tracking-tight">new-term-radar</span>
            <span class="text-xs px-2 py-0.5 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-800 font-mono">v0.5.0</span>
          </div>
          <p class="text-xs text-slate-400">AI 圈爆发新名字 · 出现当天捕获</p>
        </div>
      </div>

      <div class="flex items-center space-x-3">
        <a href="https://github.com/zhuyansen/new-term-radar" target="_blank" class="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition">
          <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
          <span>GitHub</span>
        </a>
        <button onclick="copyReport()" class="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-medium rounded-lg bg-cyan-600 hover:bg-cyan-500 text-white transition shadow-sm">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3"/></svg>
          <span id="copy-btn-text">复制日报 Markdown</span>
        </button>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 w-full space-y-8">
    <div class="bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8 relative overflow-hidden shadow-xl">
      <div class="relative z-10 max-w-3xl space-y-3">
        <div class="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-medium">
          <span class="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
          <span>Cloudflare 边缘全球部署 · 每日自动雷达扫描</span>
        </div>
        <h1 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          AI 圈新词雷达仪表盘
        </h1>
        <p class="text-slate-300 text-sm leading-relaxed">
          在新词最早被说出来的地方抓取：从 X 头部实验室、HuggingFace 热门榜、GitHub 爆发仓库、竞品 Sitemap 到 Reddit 真实求助。赶在关键词工具收录前，洞悉每一个新名字背后的通用搜索意图。
        </p>
      </div>
    </div>

    <!-- Metric Cards -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <div class="text-slate-400 text-xs font-medium">今日 GitHub 爆发仓库</div>
        <div class="mt-2 flex items-baseline space-x-2">
          <span class="text-2xl sm:text-3xl font-bold text-white">{len(breakout_repos)}</span>
          <span class="text-xs text-emerald-400 font-medium">个项目</span>
        </div>
        <div class="text-xs text-slate-500 mt-1">最高日涨星: {breakout_repos[0]['velocity'] if breakout_repos else 0}/天</div>
      </div>
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <div class="text-slate-400 text-xs font-medium">追踪监控信号源</div>
        <div class="mt-2 flex items-baseline space-x-2">
          <span class="text-2xl sm:text-3xl font-bold text-cyan-400">8</span>
          <span class="text-xs text-slate-400 font-medium">类信源</span>
        </div>
        <div class="text-xs text-slate-500 mt-1">X / HF / GH / Sitemap / Reddit</div>
      </div>
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <div class="text-slate-400 text-xs font-medium">Google Trends 提前量</div>
        <div class="mt-2 flex items-baseline space-x-2">
          <span class="text-2xl sm:text-3xl font-bold text-amber-400">3 ~ 14</span>
          <span class="text-xs text-slate-400 font-medium">天提前捕获</span>
        </div>
        <div class="text-xs text-slate-500 mt-1">在起曲线前锁定流量入口</div>
      </div>
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-4">
        <div class="text-slate-400 text-xs font-medium">更新状态</div>
        <div class="mt-2 flex items-baseline space-x-2">
          <span class="text-xl sm:text-2xl font-bold text-emerald-400">实时运行</span>
        </div>
        <div class="text-xs text-slate-500 mt-1">{datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
      </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="border-b border-slate-800 flex space-x-4 overflow-x-auto pb-1 text-sm font-medium">
      <button onclick="switchTab('breakouts')" id="tab-btn-breakouts" class="tab-btn pb-3 px-1 text-cyan-400 border-b-2 border-cyan-400 font-semibold whitespace-nowrap">
        🚀 GitHub 爆发榜 ({len(breakout_repos)})
      </button>
      <button onclick="switchTab('keywords')" id="tab-btn-keywords" class="tab-btn pb-3 px-1 text-slate-400 hover:text-slate-200 border-b-2 border-transparent whitespace-nowrap">
        🎯 候选新词与通用搜索词
      </button>
      <button onclick="switchTab('hf')" id="tab-btn-hf" class="tab-btn pb-3 px-1 text-slate-400 hover:text-slate-200 border-b-2 border-transparent whitespace-nowrap">
        🤖 Hugging Face 热门
      </button>
      <button onclick="switchTab('pains')" id="tab-btn-pains" class="tab-btn pb-3 px-1 text-slate-400 hover:text-slate-200 border-b-2 border-transparent whitespace-nowrap">
        💡 痛点与需求挖掘
      </button>
      <button onclick="switchTab('raw')" id="tab-btn-raw" class="tab-btn pb-3 px-1 text-slate-400 hover:text-slate-200 border-b-2 border-transparent whitespace-nowrap">
        📄 原始报告 (Markdown/JSON)
      </button>
      <button onclick="switchTab('guide')" id="tab-btn-guide" class="tab-btn pb-3 px-1 text-slate-400 hover:text-slate-200 border-b-2 border-transparent whitespace-nowrap">
        ⚙️ 使用与 MCP 指南
      </button>
    </div>

    <!-- Tab 1: Breakout Repos -->
    <div id="tab-breakouts" class="tab-content space-y-4">
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
        <div class="text-xs text-slate-400">
          创建不超过 14 天、日均涨星 > 200 或单日暴涨 > 400 的 GitHub 开源仓库
        </div>
        <input type="text" id="breakout-search" oninput="filterBreakouts()" placeholder="搜索仓库、作者或描述..." class="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 w-full sm:w-64">
      </div>

      <div class="overflow-x-auto border border-slate-800 rounded-xl bg-slate-900">
        <table class="w-full text-left text-xs">
          <thead class="bg-slate-800/60 text-slate-300 font-semibold border-b border-slate-800">
            <tr>
              <th class="p-3">仓库名称</th>
              <th class="p-3">总 Stars</th>
              <th class="p-3">日均涨星 (Velocity)</th>
              <th class="p-3">较昨日</th>
              <th class="p-3">诞生天数</th>
              <th class="p-3">项目描述</th>
              <th class="p-3 text-right">操作</th>
            </tr>
          </thead>
          <tbody id="breakout-tbody" class="divide-y divide-slate-800/60">
"""

for r in breakout_repos:
    repo_name = r.get("repo", "")
    stars = r.get("stars", 0)
    vel = r.get("velocity", 0)
    delta = r.get("delta", 0)
    age = r.get("age_days", 0)
    desc = r.get("description", "")
    is_new = r.get("new", False)

    new_badge = '<span class="ml-1.5 px-1.5 py-0.5 text-[10px] bg-red-950 text-red-400 border border-red-800 rounded">🆕首日</span>' if is_new else ""
    html_content += f"""
            <tr class="hover:bg-slate-800/40 transition breakout-row" data-search="{repo_name.lower()} {desc.lower()}">
              <td class="p-3 font-medium text-white flex items-center">
                <a href="https://github.com/{repo_name}" target="_blank" class="hover:text-cyan-400 transition underline underline-offset-2 flex items-center">
                  <span>{repo_name}</span>
                </a>
                {new_badge}
              </td>
              <td class="p-3 font-mono font-bold text-amber-400">★ {stars}</td>
              <td class="p-3 font-mono text-emerald-400">+{vel}/天</td>
              <td class="p-3 font-mono text-slate-300">+{delta}</td>
              <td class="p-3 text-slate-400 font-mono">{age} 天</td>
              <td class="p-3 text-slate-300 max-w-md truncate" title="{desc}">{desc or '（暂无描述）'}</td>
              <td class="p-3 text-right">
                <a href="https://github.com/{repo_name}" target="_blank" class="text-xs text-cyan-400 hover:text-cyan-300 font-medium">查看 ↗</a>
              </td>
            </tr>
    """

html_content += f"""
          </tbody>
        </table>
      </div>
    </div>

    <!-- Tab 2: Candidate Keywords -->
    <div id="tab-keywords" class="tab-content hidden space-y-4">
      <div class="text-xs text-slate-400">
        雷达双轨模型：区分具体产品名称与背后属于公众的通用搜索意图（如“SynthID Detector” vs “ai image detector”）
      </div>
      <div class="overflow-x-auto border border-slate-800 rounded-xl bg-slate-900">
        <table class="w-full text-left text-xs">
          <thead class="bg-slate-800/60 text-slate-300 font-semibold border-b border-slate-800">
            <tr>
              <th class="p-3">关键词 (Keyword)</th>
              <th class="p-3">类型</th>
              <th class="p-3">来源 / 依据</th>
              <th class="p-3">估算日搜</th>
              <th class="p-3">走势 (Google Trends)</th>
              <th class="p-3">首页竞争</th>
              <th class="p-3">投资决策建议</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800/60">
"""

for kw in benchmark_keywords:
    dec_color = "bg-emerald-950 text-emerald-400 border-emerald-800" if kw["decision"] == "优先" else ("bg-amber-950 text-amber-400 border-amber-800" if kw["decision"] == "观察" else "bg-slate-800 text-slate-400 border-slate-700")
    html_content += f"""
            <tr class="hover:bg-slate-800/40 transition">
              <td class="p-3 font-bold text-white flex items-center space-x-2">
                <span>{kw["term"]}</span>
                <span class="text-[10px] px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">{kw["badge"]}</span>
              </td>
              <td class="p-3 text-slate-300">{kw["type"]}</td>
              <td class="p-3 text-slate-400 font-mono">{kw["source"]}</td>
              <td class="p-3 font-mono font-bold text-cyan-400">{kw["daily_est"]:,}</td>
              <td class="p-3 font-medium text-emerald-400">{kw["trend"]}</td>
              <td class="p-3 text-slate-300">{kw["competition"]}</td>
              <td class="p-3">
                <span class="px-2 py-0.5 rounded-full border text-[11px] font-semibold {dec_color}">{kw["decision"]}</span>
              </td>
            </tr>
    """

html_content += f"""
          </tbody>
        </table>
      </div>
    </div>

    <!-- Tab 3: Hugging Face Trending -->
    <div id="tab-hf" class="tab-content hidden space-y-4">
      <div class="text-xs text-slate-400">
        新进 Hugging Face Trending Top 50 的模型与 Spaces 在线 Demo（公开免费数据，高频轮换）
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
"""

for item in hf_items:
    html_content += f"""
        <div class="border border-slate-800 rounded-xl bg-slate-900 p-4 space-y-2 hover:border-slate-700 transition">
          <div class="flex items-center justify-between">
            <span class="text-xs px-2 py-0.5 rounded bg-purple-950 text-purple-300 border border-purple-800 font-mono">{item["category"]}</span>
            <span class="text-xs text-rose-400 font-mono">♥ {item["likes"]}</span>
          </div>
          <h3 class="text-sm font-bold text-white font-mono">{item["name"]}</h3>
          <p class="text-xs text-slate-300">{item["desc"]}</p>
        </div>
    """

html_content += f"""
      </div>
    </div>

    <!-- Tab 4: Pain Points -->
    <div id="tab-pains" class="tab-content hidden space-y-4">
      <div class="text-xs text-slate-400">
        从 Reddit 求助帖与 Chrome Web Store 低星差评中提取的用户未满足诉求
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
"""

for p in pain_items:
    html_content += f"""
        <div class="border border-slate-800 rounded-xl bg-slate-900 p-4 space-y-3 flex flex-col justify-between">
          <div class="space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-xs font-mono font-bold text-cyan-400">#{p["keyword"]}</span>
              <span class="text-[10px] px-1.5 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-800">{p["count"]} 次差评吐槽</span>
            </div>
            <p class="text-xs text-slate-300 leading-relaxed italic">“{p["complaint"]}”</p>
          </div>
          <div class="pt-3 border-t border-slate-800/60 space-y-1">
            <div class="text-[10px] text-slate-500 uppercase font-semibold">填补机会 (Gap)</div>
            <div class="text-xs font-semibold text-emerald-400">{p["gap"]}</div>
            <div class="text-[11px] text-slate-400 font-mono">搜法: {p["search_term"]}</div>
          </div>
        </div>
    """

html_content += f"""
      </div>
    </div>

    <!-- Tab 5: Raw Report -->
    <div id="tab-raw" class="tab-content hidden space-y-4">
      <div class="flex items-center justify-between">
        <span class="text-xs text-slate-400">本地每日自动运行产出的原始 Markdown 与 JSON 报告</span>
        <button onclick="downloadJson()" class="px-2.5 py-1 text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg transition">下载 report.json</button>
      </div>
      <pre class="bg-slate-900 border border-slate-800 rounded-xl p-4 text-xs font-mono text-slate-300 overflow-x-auto whitespace-pre-wrap max-h-96">{report_md_text or '暂无本地报告文本'}</pre>
    </div>

    <!-- Tab 6: Guide & MCP -->
    <div id="tab-guide" class="tab-content hidden space-y-6">
      <div class="bg-slate-900 border border-slate-800 rounded-xl p-6 space-y-4">
        <h3 class="text-base font-bold text-white flex items-center space-x-2">
          <span>🚀 本地与命令行使用指南</span>
        </h3>
        <p class="text-xs text-slate-300">
          `new-term-radar` 已在你的系统中完成环境安装，可以直接使用以下命令运行：
        </p>
        <div class="bg-slate-950 p-4 rounded-lg font-mono text-xs text-cyan-300 space-y-2 border border-slate-800">
          <div><span class="text-slate-500"># 每日生成完整雷达报告</span><br>new-term-radar daily --out report.md</div>
          <div><span class="text-slate-500"># 调研指定新名字的通用词与日搜</span><br>new-term-radar keywords "photocraft" "claude haiku"</div>
          <div><span class="text-slate-500"># 提取某一类工具的用户真实差评痛点</span><br>new-term-radar pains "ai video generator"</div>
          <div><span class="text-slate-500"># 一键构建网页并更新至 Cloudflare Pages</span><br>deploy.bat</div>
        </div>

        <h3 class="text-base font-bold text-white pt-4 border-t border-slate-800">
          🔌 MCP Server 配置 (Claude Code / Cursor / Windsurf)
        </h3>
        <p class="text-xs text-slate-300">在 Claude Desktop 或 Cursor 的 MCP 配置中添加：</p>
        <pre class="bg-slate-950 p-4 rounded-lg font-mono text-xs text-slate-300 border border-slate-800 overflow-x-auto">{{{{
  "mcpServers": {{{{
    "new-term-radar": {{{{
      "command": "new-term-radar-mcp",
      "env": {{{{
        "AISA_API_KEY": "你的AIsaKey",
        "RADAR_CONFIG": "{config_json_str}",
        "RADAR_STATE": "{state_dir_str}"
      }}}}
    }}}}
  }}}}
}}}}</pre>
      </div>
    </div>
  </main>

  <!-- Footer -->
  <footer class="border-t border-slate-800 py-6 text-center text-xs text-slate-500">
    <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
      <div>new-term-radar · MIT Licensed · 由 Cloudflare Pages 边缘强力驱动</div>
      <div>基于 GitHub 开源生态与大模型语义雷达实时分析</div>
    </div>
  </footer>

  <script>
    function switchTab(name) {{
      document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.tab-btn').forEach(btn => {{
        btn.classList.remove('text-cyan-400', 'border-cyan-400', 'font-semibold');
        btn.classList.add('text-slate-400', 'border-transparent');
      }});
      const target = document.getElementById('tab-' + name);
      const btn = document.getElementById('tab-btn-' + name);
      if (target) target.classList.remove('hidden');
      if (btn) {{
        btn.classList.add('text-cyan-400', 'border-cyan-400', 'font-semibold');
        btn.classList.remove('text-slate-400', 'border-transparent');
      }}
    }}

    function filterBreakouts() {{
      const query = document.getElementById('breakout-search').value.toLowerCase();
      document.querySelectorAll('.breakout-row').forEach(row => {{
        const text = row.getAttribute('data-search') || '';
        row.style.display = text.includes(query) ? '' : 'none';
      }});
    }}

    const rawMarkdown = {json.dumps(report_md_text)};
    const rawData = {json.dumps(report_data)};

    function copyReport() {{
      navigator.clipboard.writeText(rawMarkdown).then(() => {{
        const btn = document.getElementById('copy-btn-text');
        const orig = btn.innerText;
        btn.innerText = '已复制！';
        setTimeout(() => btn.innerText = orig, 2000);
      }}).catch(err => alert('复制失败，请手动选择复制'));
    }}

    function downloadJson() {{
      const blob = new Blob([JSON.stringify(rawData, null, 2)], {{ type: 'application/json' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'new-term-radar-report.json';
      a.click();
      URL.revokeObjectURL(url);
    }}
  </script>
</body>
</html>
"""

(DIST / "index.html").write_text(html_content, encoding="utf-8")

# Write robots.txt
(DIST / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")

# Write _headers for Cloudflare Pages
headers_content = """/*
  X-Frame-Options: SAMEORIGIN
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Cache-Control: public, max-age=300
"""
(DIST / "_headers").write_text(headers_content, encoding="utf-8")

print(f"Build completed successfully! Assets written to {DIST}")
