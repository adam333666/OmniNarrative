from pydantic import BaseModel, Field


CONTENT_TYPES = {
    "science_popularization",
    "story",
    "mixed",
    "auto",
}

TARGET_PLATFORMS = {
    "douyin",
    "kuaishou",
    "xiaohongshu",
    "bilibili",
    "wechat_video",
}

STYLE_TONES = {
    "suspense",
    "healing",
    "passionate",
    "serious",
    "light",
    "twist",
    "high_emotion",
    "calm",
    "inspirational",
    "mysterious",
}


class CreationRequest(BaseModel):
    theme_text: str = Field(min_length=1, max_length=500)
    content_type: str = Field(min_length=1, max_length=64)
    target_platform: str = Field(min_length=1, max_length=64)
    target_audience_text: str = Field(min_length=1, max_length=500)
    style_tone: str = Field(min_length=1, max_length=64)
    custom_style_text: str | None = Field(default=None, max_length=300)

    def normalized(self) -> "CreationRequest":
        return CreationRequest(
            theme_text=self.theme_text.strip(),
            content_type=self.content_type.strip(),
            target_platform=self.target_platform.strip(),
            target_audience_text=self.target_audience_text.strip(),
            style_tone=self.style_tone.strip(),
            custom_style_text=self.custom_style_text.strip() if self.custom_style_text else None,
        )

    def validate_enums(self) -> None:
        if self.content_type not in CONTENT_TYPES:
            raise ValueError("Unsupported content_type")
        if self.target_platform not in TARGET_PLATFORMS:
            raise ValueError("Unsupported target_platform")
        if self.style_tone not in STYLE_TONES:
            raise ValueError("Unsupported style_tone")
