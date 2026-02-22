# @sulav_don
# @sulav_don2

from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# @MG24_GAMER
# @sulav_don2

YOUTUBE_API_KEY = "Sulav"

# @sulav_don2
# @sulav_don

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Sulav Gaming YouTube Info</title>
    <style>
        body {background: #0d0d0d; color: #fff; font-family: monospace; text-align: center;}
        h1 {font-size: 70px; color: #ff0055; text-shadow: 0 0 20px #ff00ff; margin-bottom: 5px;}
        h3 {font-size: 22px; color: #00ffff; margin-top: 0;}
        input {padding: 12px; width: 350px; border-radius: 6px; border: none; margin-right: 10px;}
        button {padding: 12px 25px; background: #ff0055; color: white; border: none; border-radius: 6px; cursor: pointer;}
        .credit {margin-top: 20px; color: gold; font-weight: bold; font-size: 18px;}
        .info-box {margin: 30px auto; padding: 20px; max-width: 600px; background: #1a1a1a; border-radius: 12px; box-shadow: 0 0 15px #ff00ff; text-align: left;}
        .info-box p {margin: 5px 0;}
    </style>
</head>
<body>

<h1>Sulav Gaming</h1>
<h3>YouTube Info API</h3>

<form action="/yt" method="get">
    <input type="text" name="channel" placeholder="Enter Channel ID or Handle (e.g @Sulavgaming.7)" required>
    <button type="submit">FETCH INFO</button>
</form>

<div class="credit">
    @sulav_don2 | @sulav_don
</div>

</body>
</html>
"""

# @sulav_don
# @sulav_don2

def fetch_youtube_info(channel_input):
    try:
        # Determine if it's a handle or channel_id
        if channel_input.startswith("UC"):
            channel_id = channel_input
        else:
            handle_clean = channel_input.lstrip("@")
            # search channel by handle
            search_url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                "part": "snippet",
                "q": handle_clean,
                "type": "channel",
                "maxResults": 1,
                "key": YOUTUBE_API_KEY
            }
            search_res = requests.get(search_url, params=params, timeout=10).json()
            if "items" not in search_res or len(search_res["items"]) == 0:
                return {"error": "Channel not found", "credit": "Sulav Gaming", "telegram_update": "@sulav_don2"}
            channel_id = search_res["items"][0]["snippet"]["channelId"]

        # fetch channel details
        url = "https://www.googleapis.com/youtube/v3/channels"
        params = {"part": "snippet,statistics", "id": channel_id, "key": YOUTUBE_API_KEY}
        res = requests.get(url, params=params, timeout=10).json()
        if "items" not in res or len(res["items"]) == 0:
            return {"error": "Channel not found", "credit": "Sulav Gaming", "telegram_update": "@sulav_don2"}

        item = res["items"][0]
        snippet = item.get("snippet", {})
        stats = item.get("statistics", {})

        # get handle reliably
        handle = None
        if snippet.get("customUrl"):
            handle = snippet.get("customUrl")
        else:
            handle = snippet.get("title", "").replace(" ", "").lower()

        return {
            "credit": "Sulav Gaming",
            "telegram_channel": "@sulav_don2",
            "channel_title": snippet.get("title"),
            "channel_id": item.get("id"),
            "handle": handle,
            "description": snippet.get("description"),
            "published_at": snippet.get("publishedAt"),
            "statistics": {
                "subscribers": stats.get("subscriberCount", "0"),
                "views": stats.get("viewCount", "0"),
                "videos": stats.get("videoCount", "0")
            }
        }
    except Exception as e:
        return {"error": str(e), "credit": "Sulav Gaming", "telegram_update": "@sulav_don2"}

# @sulav_don2
# @sulav_don

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/yt")
def yt():
    channel = request.args.get("channel")
    if not channel:
        return jsonify({"error": "channel parameter required", "credit": "Sulav Gaming", "telegram_update": "@sulav_don2"}), 400

    data = fetch_youtube_info(channel)
    return jsonify(data)

# @sulav_don
# @sulav_don2

if __name__ == "__main__":
    app.run(debug=True)