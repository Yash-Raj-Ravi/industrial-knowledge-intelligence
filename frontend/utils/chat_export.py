from datetime import datetime


def generate_chat_markdown(messages):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content = f"# Industrial Knowledge Intelligence Chat\n\n"
    content += f"**Exported:** {timestamp}\n\n"
    content += "---\n\n"

    for message in messages:
        role = "User" if message["role"] == "user" else "Assistant"

        content += f"## {role}\n\n"
        content += message["content"]
        content += "\n\n"

    return content