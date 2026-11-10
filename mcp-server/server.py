"""MCP server written by hand, with no SDK: JSON-RPC over stdio.

Reads one JSON message per line on stdin and writes one JSON reply per line on stdout.
stdout is reserved for the protocol; every log goes to stderr.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent

# Read the data once, when the server starts, not on every call.
LECTURES = json.loads((HERE / "lectures.json").read_text(encoding="utf-8"))
CATEGORIES = json.loads((HERE / "categories.json").read_text(encoding="utf-8"))

# The tools this server offers. The description is what the model reads to choose.
TOOLS = [
    {
        "name": "find_lecture",
        "description": (
            "Return the title and topics of one course lecture by its number, 1 to 12. "
            "Use it when asked what a lecture covers. Returns one line of text."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "number": {"type": "integer", "description": "Lecture number, 1 to 12"}
            },
            "required": ["number"],
        },
    },
    {
        "name": "list_categories",
        "description": (
            "List the expense categories SplitMate accepts, each with a short description. "
            "Use it when asked which category an expense belongs to or which categories exist."
        ),
        "inputSchema": {"type": "object", "properties": {}},
    },
]


def log(text):
    """Write a log line to stderr. The client reads stdout as protocol."""
    print(text, file=sys.stderr, flush=True)


def send(reply):
    """Print one reply as one line of JSON on stdout, and flush it at once."""
    print(json.dumps(reply), flush=True)


def text_result(msg_id, text, is_error):
    """A tool result: one text part, and whether the tool failed."""
    return {
        "jsonrpc": "2.0",
        "id": msg_id,
        "result": {"content": [{"type": "text", "text": text}], "isError": is_error},
    }


def protocol_error(msg_id, code, message):
    """A JSON-RPC error: the message itself was wrong, not the tool."""
    return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": code, "message": message}}


def find_lecture(msg_id, args):
    number = args.get("number")
    lecture = next((l for l in LECTURES if l["number"] == number), None)
    if lecture is None:
        # The tool ran and failed: a normal result the model can read, marked isError.
        return text_result(
            msg_id, f"There is no lecture {number}. The course has lectures 1 to 12.", True
        )
    text = f"Lecture {lecture['number']}: {lecture['title']}. Topics: {lecture['topics']}"
    return text_result(msg_id, text, False)


def list_categories(msg_id, args):
    lines = [f"{c['name']}: {c['description']}" for c in CATEGORIES]
    return text_result(msg_id, "\n".join(lines), False)


# Tool name -> function that runs it.
HANDLERS = {"find_lecture": find_lecture, "list_categories": list_categories}


def handle(msg):
    """Decide what to answer. Return the reply, or None to answer nothing."""
    method = msg.get("method")
    msg_id = msg.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": msg["params"]["protocolVersion"],
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "lectures", "version": "0.1.0"},
            },
        }
    if method == "notifications/initialized":
        return None  # a notification: it has no id and gets no reply
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS}}
    if method == "tools/call":
        params = msg.get("params", {})
        name = params.get("name")
        handler = HANDLERS.get(name)
        if handler is None:
            # A tool we never offered: the message itself is wrong, so it is a protocol error.
            return protocol_error(msg_id, -32602, f"Unknown tool: {name}")
        return handler(msg_id, params.get("arguments") or {})
    if msg_id is not None:
        # Any other request we do not know.
        return protocol_error(msg_id, -32601, f"Unknown method: {method}")
    return None  # an unknown notification: ignore it


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        log("got: " + line)
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            # Not JSON at all: answer with a parse error instead of crashing.
            send(protocol_error(None, -32700, "Parse error"))
            continue
        reply = handle(msg)
        if reply is not None:
            send(reply)


if __name__ == "__main__":
    main()
