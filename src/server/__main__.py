import os
from server import create_app

os.environ["TODOS_FS_MODE"] = "development"
app = create_app()
app.run()
