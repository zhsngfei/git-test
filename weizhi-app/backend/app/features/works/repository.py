def get_work_detail(work_slug: str) -> dict[str, object] | None:
    work_details: dict[str, dict[str, object]] = {
        "old-capital": {
            "work": {
                "id": "old-capital",
                "slug": "old-capital",
                "titleZh": "古都",
                "titleOriginal": "古都",
                "contentType": "book",
                "creator": "川端康成",
                "year": "1962",
                "summary": "一部通过京都街巷、季节和传统生活气息进入城市记忆的小说。",
            },
            "city": {
                "slug": "kyoto",
                "nameZh": "京都",
                "countryRegion": "日本",
            },
            "recommendationReason": "它不急着解释京都，而是让用户先习惯这座城市的留白、秩序和季节感。",
            "cityConnection": "作品中的京都不是背景板，而是人物生活方式、家族记忆和城市秩序的一部分。",
            "relatedPlaces": [
                {
                    "id": "gion",
                    "slug": "gion",
                    "nameZh": "祇园",
                    "summary": "理解传统街区和旧日生活秩序的入口。",
                },
                {
                    "id": "kamo-river",
                    "slug": "kamo-river",
                    "nameZh": "鸭川",
                    "summary": "连接京都日常和作品中的城市经验。",
                },
            ],
        },
        "lost-in-translation": {
            "work": {
                "id": "lost-in-translation",
                "slug": "lost-in-translation",
                "titleZh": "迷失东京",
                "titleOriginal": "Lost in Translation",
                "contentType": "film",
                "creator": "Sofia Coppola",
                "year": "2003",
                "summary": "一部以东京酒店、街道和夜晚经验为主要城市线索的电影。",
            },
            "city": {
                "slug": "tokyo",
                "nameZh": "东京",
                "countryRegion": "日本",
            },
            "recommendationReason": "它用克制的镜头语言捕捉都市中的异乡感、疏离与短暂连接。",
            "cityConnection": "片中的酒店、酒吧、街道与霓虹构成了东京的夜间层次。",
            "relatedPlaces": [
                {
                    "id": "shinjuku",
                    "slug": "shinjuku",
                    "nameZh": "新宿",
                    "summary": "霓虹、人潮和夜间城市经验交汇的地点。",
                }
            ],
        },
    }

    return work_details.get(work_slug)
