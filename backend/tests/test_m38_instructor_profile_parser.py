from __future__ import annotations

from app.schemas.creation_request import CreationRequest
from app.schemas.profiles import AudienceProfile, StyleProfile
from app.services.profile_parser.service import ProfileParserService
from app.services.structured_output_gateway.service import StructuredOutputGatewayService


def build_request() -> CreationRequest:
    return CreationRequest(
        theme_text="时间旅行悖论",
        content_type="science_popularization",
        target_platform="bilibili",
        target_audience_text="18到28岁，喜欢科幻设定和逻辑推理的观众",
        style_tone="suspense",
        custom_style_text="保持一点烧脑感",
    )


class FakeInstructorClient:
    def __init__(self, responses: list[AudienceProfile | StyleProfile]) -> None:
        self._responses = responses
        self.calls: list[dict] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return self._responses.pop(0)


def test_profile_parser_prefers_instructor_client() -> None:
    client = FakeInstructorClient(
        responses=[
            AudienceProfile(
                raw_text="18到28岁，喜欢科幻设定和逻辑推理的观众",
                age_group_guess="18-28",
                interest_tags=["科幻设定", "逻辑推理"],
                pain_points=["需要快速进入主题"],
                content_preference=["信息密度高", "开头要快"],
                emotion_preference=["紧张好奇"],
            ),
            StyleProfile(
                style_label="suspense",
                emotion_label="紧张好奇",
                intensity_level="medium",
                custom_notes="保持一点烧脑感",
            ),
        ]
    )
    service = ProfileParserService(
        structured_output_gateway=StructuredOutputGatewayService(
            instructor_client_factory=lambda: client,
            provider_name="litellm",
            model_name="openai/gpt-4o-mini",
            max_retries=2,
            temperature=0.2,
        ),
    )

    audience_profile = service.parse_audience_profile(build_request())
    style_profile = service.parse_style_profile(build_request())

    assert audience_profile.interest_tags == ["科幻设定", "逻辑推理"]
    assert style_profile.emotion_label == "紧张好奇"
    assert len(client.calls) == 2
    assert client.calls[0]["response_model"] is AudienceProfile
    assert client.calls[1]["response_model"] is StyleProfile
    assert client.calls[0]["model"] == "openai/gpt-4o-mini"
    assert client.calls[1]["max_retries"] == 2


def test_profile_parser_falls_back_when_instructor_unavailable() -> None:
    service = ProfileParserService(
        structured_output_gateway=StructuredOutputGatewayService(
            instructor_client_factory=lambda: (_ for _ in ()).throw(RuntimeError("instructor missing")),
            provider_name="litellm",
            model_name="openai/gpt-4o-mini",
        ),
    )

    audience_profile = service.parse_audience_profile(build_request())
    style_profile = service.parse_style_profile(build_request())

    assert audience_profile.age_group_guess == "18-24"
    assert audience_profile.interest_tags == ["脑洞设定"]
    assert style_profile.style_label == "suspense"
    assert style_profile.emotion_label == "紧张好奇"
    assert style_profile.intensity_level == "medium"


def test_profile_parser_normalizes_sparse_instructor_payload() -> None:
    client = FakeInstructorClient(
        responses=[
            AudienceProfile(
                raw_text="",
                age_group_guess="",
                interest_tags=[],
                pain_points=[],
                content_preference=[],
                emotion_preference=[],
            ),
            StyleProfile(
                style_label="",
                emotion_label="",
                intensity_level="medium",
                custom_notes="   ",
            ),
        ]
    )
    service = ProfileParserService(
        structured_output_gateway=StructuredOutputGatewayService(
            instructor_client_factory=lambda: client,
            provider_name="litellm",
            model_name="openai/gpt-4o-mini",
        ),
    )

    audience_profile = service.parse_audience_profile(build_request())
    style_profile = service.parse_style_profile(build_request())

    assert audience_profile.raw_text == build_request().target_audience_text
    assert audience_profile.age_group_guess == "18-24"
    assert audience_profile.interest_tags == ["脑洞设定"]
    assert audience_profile.pain_points == ["需要更快进入内容主题"]
    assert audience_profile.content_preference == ["开头要快", "结构要清楚"]
    assert audience_profile.emotion_preference == ["希望被带入但不被说教"]
    assert style_profile.style_label == "suspense"
    assert style_profile.emotion_label == "紧张好奇"
    assert style_profile.custom_notes == "保持一点烧脑感"
