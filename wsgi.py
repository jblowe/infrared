"""WSGI entry point. The active core comes from ``INFRARED_CORE``."""
from infrared import create_app

app = create_app()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the Infrared dev server.")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=3002)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, debug=args.debug)
