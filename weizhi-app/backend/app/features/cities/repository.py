def list_supported_cities() -> list[dict[str, str | bool]]:
    return [
        {
            "slug": "kyoto",
            "nameZh": "京都",
            "countryRegion": "日本",
            "isSupported": True,
            "contentDepth": "core",
            "toneSummary": "从作品、街区和地点关系开始认识这座城市",
        },
        {
            "slug": "tokyo",
            "nameZh": "东京",
            "countryRegion": "日本",
            "isSupported": True,
            "contentDepth": "core",
            "toneSummary": "孤独、夜晚、现代都市与日常缝隙",
        },
    ]
