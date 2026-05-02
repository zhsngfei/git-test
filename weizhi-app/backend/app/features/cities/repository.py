def list_supported_cities() -> list[dict[str, str | bool]]:
    return [
        {
            "slug": "kyoto",
            "nameZh": "京都",
            "countryRegion": "日本",
            "isSupported": True,
            "contentDepth": "core",
            "toneSummary": "安静、古典、适合旅行前慢慢进入的城市",
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
