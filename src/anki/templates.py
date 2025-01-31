import genanki


MODEL_ID = 1234567890


def get_model():
    fields = [
        {"name": "Word"},
        {"name": "Video"},
    ]

    templates = [
        {
            "name": "Word-to-Video",
            "qfmt": """
                <div class="card word">
                    <div class="word-title">{{Word}}</div>
                </div>
            """,
            "afmt": """
                {{FrontSide}}
                <hr>
                <div class="card media">
                    {{Video}}
                </div>
            """,
        }
    ]

    css = """
        /* Card Container */
        .card {
            font-family: Arial, sans-serif;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.8); /* Stronger shadow for dark mode */
            max-width: 400px;
            margin: auto;
            padding: 16px;
            background-color: #1e1e1e; /* Dark background */
            color: #f5f5f5; /* Light text */
        }

        /* Word Card */
        .card.word .word-title {
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            color: #ffcc00; /* Highlighted title for contrast */
            padding: 16px 0;
        }

        /* Video Card */
        .card.media video {  /* Fixed Selector */
            display: block;
            margin: 0 auto;
            width: 300px;
            max-width: 100%;
            border-radius: 8px;
            background-color: #333; /* Dark background for videos */
        }

        /* Horizontal Rule */
        hr {
            border: none;
            border-top: 1px solid #555; /* Subtle divider for dark mode */
            margin: 16px 0;
        }
    """

    return genanki.Model(
        model_id=MODEL_ID,
        name="Lesco Model",
        fields=fields,
        templates=templates,
        css=css,
    )
