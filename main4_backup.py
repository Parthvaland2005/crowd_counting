# Minimal Vercel WSGI entry — must expose `app`
# Ensure your main4.py defines `app = Flask(__name__)` (or exposes create_app()).
try:
    from main4 import app  # import your Flask app instance
except Exception as e:
    # Fallback minimal app so deployment at least succeeds
    from flask import Flask
    app = Flask(__name__)
    @app.route("/")
    def index():
        return "App import failed on build: " + str(e), 500        # Minimal Vercel WSGI entry — must expose `app`
        # Ensure your main4.py defines `app = Flask(__name__)` (or exposes create_app()).
        try:
            from main4 import app  # import your Flask app instance
        except Exception as e:
            # Fallback minimal app so deployment at least succeeds
            from flask import Flask
            app = Flask(__name__)
            @app.route("/")
            def index():
                return "App import failed on build: " + str(e), 500                # Minimal Vercel WSGI entry — must expose `app`
                # Ensure your main4.py defines `app = Flask(__name__)` (or exposes create_app()).
                try:
                    from main4 import app  # import your Flask app instance
                except Exception as e:
                    # Fallback minimal app so deployment at least succeeds
                    from flask import Flask
                    app = Flask(__name__)
                    @app.route("/")
                    def index():
                        return "App import failed on build: " + str(e), 500                        # Minimal Vercel WSGI entry — must expose `app`
                        # Ensure your main4.py defines `app = Flask(__name__)` (or exposes create_app()).
                        try:
                            from main4 import app  # import your Flask app instance
                        except Exception as e:
                            # Fallback minimal app so deployment at least succeeds
                            from flask import Flask
                            app = Flask(__name__)
                            @app.route("/")
                            def index():
                                return "App import failed on build: " + str(e), 500                                # Minimal Vercel WSGI entry — must expose `app`
                                # Ensure your main4.py defines `app = Flask(__name__)` (or exposes create_app()).
                                try:
                                    from main4 import app  # import your Flask app instance
                                except Exception as e:
                                    # Fallback minimal app so deployment at least succeeds
                                    from flask import Flask
                                    app = Flask(__name__)
                                    @app.route("/")
                                    def index():
                                        return "App import failed on build: " + str(e), 500                                        # Minimal Vercel WSGI entry — must expose `app`
                                        # Ensure your main4.py defines `app = Flask(__name__)` (or exposes create_app()).
                                        try:
                                            from main4 import app  # import your Flask app instance
                                        except Exception as e:
                                            # Fallback minimal app so deployment at least succeeds
                                            from flask import Flask
                                            app = Flask(__name__)
                                            @app.route("/")
                                            def index():
                                                return "App import failed on build: " + str(e), 500                                                # Minimal Vercel WSGI entry — must expose `app`
                                                # Ensure your main4.py defines `app = Flask(__name__)` (or exposes create_app()).
                                                try:
                                                    from main4 import app  # import your Flask app instance
                                                except Exception as e:
                                                    # Fallback minimal app so deployment at least succeeds
                                                    from flask import Flask
                                                    app = Flask(__name__)
                                                    @app.route("/")
                                                    def index():
                                                        return "App import failed on build: " + str(e), 500                                                        # Minimal Vercel WSGI entry — must expose `app`
                                                        # Ensure your main4.py defines `app = Flask(__name__)` (or exposes create_app()).
                                                        try:
                                                            from main4 import app  # import your Flask app instance
                                                        except Exception as e:
                                                            # Fallback minimal app so deployment at least succeeds
                                                            from flask import Flask
                                                            app = Flask(__name__)
                                                            @app.route("/")
                                                            def index():
                                                                return "App import failed on build: " + str(e), 500from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)