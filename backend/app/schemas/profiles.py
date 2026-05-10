from typing import Literal

from pydantic import BaseModel, Field


class AudienceProfile(BaseModel):
    raw_text: str = Field(description="原始受众描述文本，尽量保留用户输入原意。")
    age_group_guess: str = Field(description="根据输入推断的主要年龄段，使用简短区间文本表达。")
    interest_tags: list[str] = Field(description="受众最关心的内容兴趣点，使用简短中文标签。")
    pain_points: list[str] = Field(description="受众当前最可能存在的理解、情绪或内容消费障碍。")
    content_preference: list[str] = Field(description="受众偏好的内容表达方式与节奏要求。")
    emotion_preference: list[str] = Field(description="受众更容易接受的情绪体验方式。")


class StyleProfile(BaseModel):
    style_label: str = Field(description="必须回填输入中的 style_tone 原值，不要改写。")
    emotion_label: str = Field(description="该风格希望传达给用户的核心情绪感受。")
    intensity_level: Literal["low", "medium", "high"] = Field(description="风格强度等级，只能是 low、medium、high。")
    custom_notes: str | None = Field(default=None, description="用户提供的额外风格备注，缺失时为 null。")
