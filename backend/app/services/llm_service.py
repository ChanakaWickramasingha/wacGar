def generate_explanation(garbage_class):
    explanations = {
        "plastic": {
            "description": "Plastic waste takes hundreds of years to decompose.",
            "tips": [
                "Rinse before recycling",
                "Avoid burning plastic",
                "Reuse when possible"
            ]
        },
        "battery": {
            "description": "Batteries contain harmful chemicals.",
            "tips": [
                "Do not throw in normal trash",
                "Take to e-waste collection points"
            ]
        }
    }

    return explanations.get(
        garbage_class,
        {
            "description": "This type of waste should be disposed responsibly.",
            "tips": ["Check local recycling guidelines"]
        }
    )
