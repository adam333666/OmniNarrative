from copy import deepcopy
from datetime import UTC, datetime

from app.schemas.trend_template import PlatformTrendTemplate


DEFAULT_TEMPLATE_DEFINITIONS: list[dict] = [
    {
        "platform": "douyin",
        "content_type": "auto",
        "summary": "强钩子、强节奏、快速抛出冲突或反差。",
        "hook_patterns": ["先给反常识判断", "先给情绪冲击点"],
        "rhythm_patterns": ["3秒抓住注意力", "段落切换快"],
        "title_cover_style": ["问题式标题", "情绪强对比封面文案"],
        "audience_preference_summary": "更偏好即时理解与情绪反应。",
        "avoid_patterns": ["铺垫过长", "抽象论述过多"],
        "hot_topics_summary": ["情绪议题", "反常识知识点"],
        "interaction_patterns": ["评论区接龙补充反差案例", "转发时强调一句强结论"],
        "emotional_entry_points": ["情绪冲击", "反差爽点"],
        "creator_angle_summary": "更适合用短句强结论和高冲突开场快速建立注意力。",
    },
    {
        "platform": "kuaishou",
        "content_type": "auto",
        "summary": "真实直给、接地气，优先人和情境。",
        "hook_patterns": ["先抛真实生活问题", "先给人物状态"],
        "rhythm_patterns": ["叙事直线推进", "口语化表达"],
        "title_cover_style": ["口语化标题", "人物状态型封面"],
        "audience_preference_summary": "更重视真实感和情绪直达。",
        "avoid_patterns": ["过度包装", "概念过虚"],
        "hot_topics_summary": ["日常生活", "真实困境"],
        "interaction_patterns": ["评论区补真实经历", "围绕人物处境展开共鸣"],
        "emotional_entry_points": ["生活压力", "人物关系共鸣"],
        "creator_angle_summary": "更适合从人物处境和生活现场切入，不宜过度概念化。",
    },
    {
        "platform": "xiaohongshu",
        "content_type": "auto",
        "summary": "强调可分享、可共鸣、可转述的观点表达。",
        "hook_patterns": ["先给可共鸣场景", "先给结论再解释"],
        "rhythm_patterns": ["信息分层清楚", "视觉感受要统一"],
        "title_cover_style": ["笔记式标题", "关键词清晰的封面文案"],
        "audience_preference_summary": "更偏好可转发、可收藏的表达。",
        "avoid_patterns": ["信息过密无重点", "语气过硬"],
        "hot_topics_summary": ["生活方式", "经验总结"],
        "interaction_patterns": ["收藏导向的清单评论", "围绕个人经验补充案例"],
        "emotional_entry_points": ["自我提升焦虑", "被理解感"],
        "creator_angle_summary": "更适合以经验总结、可保存观点和场景化表达组织内容。",
    },
    {
        "platform": "bilibili",
        "content_type": "auto",
        "summary": "允许更完整的逻辑链条与世界观展开。",
        "hook_patterns": ["先抛核心设问", "先给世界观矛盾"],
        "rhythm_patterns": ["可以有完整铺垫", "中段信息密度可以提升"],
        "title_cover_style": ["命题式标题", "设问型封面文案"],
        "audience_preference_summary": "更接受解释、推理和结构化展开。",
        "avoid_patterns": ["只给结论不给推理", "节奏过于碎片化"],
        "hot_topics_summary": ["设定讨论", "知识拆解", "长逻辑叙事"],
        "interaction_patterns": ["评论区补反例", "围绕设定漏洞继续推理"],
        "emotional_entry_points": ["认知冲突", "世界观好奇"],
        "creator_angle_summary": "更适合从核心设问、世界观矛盾和完整解释链组织表达。",
    },
    {
        "platform": "wechat_video",
        "content_type": "auto",
        "summary": "表达平衡、可信、适合较广泛人群转发。",
        "hook_patterns": ["先给普适问题", "先给切身感受"],
        "rhythm_patterns": ["叙事平稳", "观点明确"],
        "title_cover_style": ["可信赖标题", "清晰陈述式封面"],
        "audience_preference_summary": "偏好稳妥、信息清晰的内容。",
        "avoid_patterns": ["过度刺激化表达", "过强网络黑话"],
        "hot_topics_summary": ["普适情绪", "大众认知问题"],
        "interaction_patterns": ["转发给家人朋友的实用补充", "围绕普适问题留言举例"],
        "emotional_entry_points": ["切身感受", "可信赖安心感"],
        "creator_angle_summary": "更适合用可信、平衡、适合广泛转发的口吻建立表达。",
    },
]

PLATFORM_VARIANT_TARGETS: tuple[str, ...] = ("douyin", "kuaishou", "xiaohongshu", "bilibili")

CONTENT_TYPE_VARIANT_OVERRIDES: dict[str, dict[str, str | list[str]]] = {
    "science_popularization": {
        "summary_suffix": "更适合从问题拆解、知识解释和结论复述来组织内容。",
        "hook_patterns": ["先抛核心问题", "先给反常识结论"],
        "rhythm_patterns": ["前段快提问", "中段补解释链"],
        "title_cover_style": ["问题拆解式标题", "结论先行封面文案"],
        "audience_preference_summary": "更偏好清楚、具体、能带走一个判断的知识表达。",
        "avoid_patterns": ["术语堆叠过多", "解释链断裂"],
        "hot_topics_summary": ["知识拆解", "反常识问题"],
        "interaction_patterns": ["评论区追问原理", "补充反例和案例"],
        "emotional_entry_points": ["认知冲突", "求知欲"],
        "creator_angle_summary": "更适合从问题切入，再给出完整但不冗长的解释。",
    },
    "story": {
        "summary_suffix": "更适合从人物处境、情绪推进和可代入场景来组织内容。",
        "hook_patterns": ["先给人物状态", "先给情绪瞬间"],
        "rhythm_patterns": ["前段立处境", "中段推冲突"],
        "title_cover_style": ["情绪共鸣式标题", "人物状态型封面文案"],
        "audience_preference_summary": "更偏好能代入、能共鸣、能快速看懂关系和情绪的表达。",
        "avoid_patterns": ["情绪空转", "人物动机不清"],
        "hot_topics_summary": ["人物关系", "情绪共鸣"],
        "interaction_patterns": ["评论区补经历", "围绕关系展开讨论"],
        "emotional_entry_points": ["委屈感", "被理解感"],
        "creator_angle_summary": "更适合先建立人物处境，再推进情绪和关系变化。",
    },
}


def _iter_default_template_definitions() -> list[dict]:
    definitions = [deepcopy(item) for item in DEFAULT_TEMPLATE_DEFINITIONS]

    auto_by_platform = {item["platform"]: item for item in DEFAULT_TEMPLATE_DEFINITIONS}
    for platform in PLATFORM_VARIANT_TARGETS:
        base = auto_by_platform[platform]
        for content_type, override in CONTENT_TYPE_VARIANT_OVERRIDES.items():
            variant = deepcopy(base)
            variant["content_type"] = content_type
            variant["summary"] = f"{base['summary']} {override['summary_suffix']}"
            variant["hook_patterns"] = list(override["hook_patterns"])
            variant["rhythm_patterns"] = list(override["rhythm_patterns"])
            variant["title_cover_style"] = list(override["title_cover_style"])
            variant["audience_preference_summary"] = str(override["audience_preference_summary"])
            variant["avoid_patterns"] = list(override["avoid_patterns"])
            variant["hot_topics_summary"] = list(override["hot_topics_summary"])
            variant["interaction_patterns"] = list(override["interaction_patterns"])
            variant["emotional_entry_points"] = list(override["emotional_entry_points"])
            variant["creator_angle_summary"] = str(override["creator_angle_summary"])
            definitions.append(variant)

    return definitions

REFRESH_APPENDIX: dict[str, str] = {
    "douyin": "近期更强调开场冲突、短句节奏和情绪显性表达。",
    "kuaishou": "近期更强调人物关系、生活场景和真实表达。",
    "xiaohongshu": "近期更强调可保存、可复述和场景化经验。",
    "bilibili": "近期更强调设问推进、知识密度和完整解释链条。",
    "wechat_video": "近期更强调可信表达、家庭场景和广泛转发友好度。",
}


def build_seed_templates(updated_at: datetime | None = None, source_type: str = "seed") -> list[PlatformTrendTemplate]:
    timestamp = updated_at or datetime.now(UTC)
    return [
        PlatformTrendTemplate(**item, source_type=source_type, updated_at=timestamp)
        for item in _iter_default_template_definitions()
    ]


def build_refreshed_templates(updated_at: datetime | None = None) -> list[PlatformTrendTemplate]:
    timestamp = updated_at or datetime.now(UTC)
    refreshed_templates: list[PlatformTrendTemplate] = []

    for item in _iter_default_template_definitions():
        appendix = REFRESH_APPENDIX[item["platform"]]
        hot_topics = list(item["hot_topics_summary"])
        refresh_topic = f"{timestamp.year}平台观察"
        if refresh_topic not in hot_topics:
            hot_topics.append(refresh_topic)

        refreshed_item = {
            **item,
            "summary": f"{item['summary']} {appendix}",
            "hot_topics_summary": hot_topics,
            "source_type": "manual_refresh",
            "updated_at": timestamp,
        }
        refreshed_templates.append(PlatformTrendTemplate(**refreshed_item))

    return refreshed_templates
