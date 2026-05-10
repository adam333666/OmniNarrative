from enum import StrEnum


class GenerationStatus(StrEnum):
    input_collecting = "INPUT_COLLECTING"
    theme_parsing = "THEME_PARSING"
    profile_parsing = "PROFILE_PARSING"
    narrative_generating = "NARRATIVE_GENERATING"
    trend_adapting = "TREND_ADAPTING"
    package_assembling = "PACKAGE_ASSEMBLING"
    done = "DONE"
    failed = "FAILED"
    timeout = "TIMEOUT"
