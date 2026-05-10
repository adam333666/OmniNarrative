from fastapi import APIRouter, Header, HTTPException, Query

from app.core.config import settings
from app.schemas.creation_request import CONTENT_TYPES, STYLE_TONES, TARGET_PLATFORMS
from app.schemas.trend_template import TrendRefreshResponse, TrendTemplateListResponse
from app.services.trend_strategy.service import trend_strategy_service

router = APIRouter(tags=["config"])


CONTENT_TYPE_LABELS = {
    "science_popularization": "科普型",
    "story": "故事型",
    "mixed": "混合型",
    "auto": "自动判断",
}

PLATFORM_LABELS = {
    "douyin": "抖音",
    "kuaishou": "快手",
    "xiaohongshu": "小红书",
    "bilibili": "B站",
    "wechat_video": "视频号",
}

STYLE_TONE_LABELS = {
    "suspense": "悬疑",
    "healing": "治愈",
    "passionate": "热血",
    "serious": "严肃",
    "light": "轻松",
    "twist": "反转",
    "high_emotion": "高情绪",
    "calm": "冷静克制",
    "inspirational": "鼓舞",
    "mysterious": "神秘",
}


@router.get("/config/input-options")
def get_input_options() -> dict:
    return {
        "content_types": [
            {"value": value, "label": CONTENT_TYPE_LABELS[value]}
            for value in sorted(CONTENT_TYPES)
        ],
        "platforms": [
            {"value": value, "label": PLATFORM_LABELS[value]}
            for value in sorted(TARGET_PLATFORMS)
        ],
        "style_tones": [
            {"value": value, "label": STYLE_TONE_LABELS[value]}
            for value in sorted(STYLE_TONES)
        ],
        "example_prompts": [
            "我想做一个关于时间旅行悖论的内容",
            "我想做一个关于高三学生焦虑的内容",
            "我想做一个讲猫为什么会踩奶的内容",
        ],
    }


@router.get("/config/trend-templates", response_model=TrendTemplateListResponse)
def get_trend_templates(
    platform: str | None = Query(default=None),
    content_type: str | None = Query(default=None),
) -> TrendTemplateListResponse:
    return trend_strategy_service.list_template_summaries(platform=platform, content_type=content_type)


@router.post("/config/trend-refresh", response_model=TrendRefreshResponse)
def refresh_trend_templates(
    x_internal_api_key: str = Header(default="", alias="X-Internal-Api-Key"),
) -> TrendRefreshResponse:
    if not settings.internal_api_key:
        raise HTTPException(status_code=503, detail="Trend refresh is not enabled in the current environment")

    if x_internal_api_key != settings.internal_api_key:
        raise HTTPException(status_code=403, detail="Invalid internal API key")

    return trend_strategy_service.refresh_templates()
