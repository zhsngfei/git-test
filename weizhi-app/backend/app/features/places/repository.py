def get_place_detail(place_slug: str) -> dict[str, object] | None:
    place_details: dict[str, dict[str, object]] = {
        "gion": {
            "place": {
                "id": "gion",
                "slug": "gion",
                "nameZh": "祇园",
                "summary": "京都代表性的传统街区之一，与作品中的旧日生活秩序紧密相关。",
            },
            "city": {
                "slug": "kyoto",
                "nameZh": "京都",
                "countryRegion": "日本",
            },
            "meaning": "祇园帮助用户理解《古都》中传统街区、旧日生活秩序和城市记忆之间的关系。",
            "relatedWorks": [
                {
                    "id": "old-capital",
                    "slug": "old-capital",
                    "titleZh": "古都",
                    "contentType": "book",
                    "creator": "川端康成",
                    "summary": "从街巷、季节和传统生活进入京都。",
                }
            ],
        },
        "kamo-river": {
            "place": {
                "id": "kamo-river",
                "slug": "kamo-river",
                "nameZh": "鸭川",
                "summary": "贯穿京都日常生活的河流，也是理解作品中城市关系的地点触点。",
            },
            "city": {
                "slug": "kyoto",
                "nameZh": "京都",
                "countryRegion": "日本",
            },
            "meaning": "鸭川把作品里的城市季节感、散步经验和日常生活连接起来。",
            "relatedWorks": [
                {
                    "id": "old-capital",
                    "slug": "old-capital",
                    "titleZh": "古都",
                    "contentType": "book",
                    "creator": "川端康成",
                    "summary": "从街巷、季节和传统生活进入京都。",
                }
            ],
        },
        "shinjuku": {
            "place": {
                "id": "shinjuku",
                "slug": "shinjuku",
                "nameZh": "新宿",
                "summary": "霓虹、人潮和夜间城市经验交汇的地点。",
            },
            "city": {
                "slug": "tokyo",
                "nameZh": "东京",
                "countryRegion": "日本",
            },
            "meaning": "新宿帮助用户理解《迷失东京》中陌生城市的明亮、喧嚣与短暂连接。",
            "relatedWorks": [
                {
                    "id": "lost-in-translation",
                    "slug": "lost-in-translation",
                    "titleZh": "迷失东京",
                    "contentType": "film",
                    "creator": "Sofia Coppola",
                    "summary": "在陌生的城市里，寻找连接的可能。",
                }
            ],
        },
    }

    return place_details.get(place_slug)
