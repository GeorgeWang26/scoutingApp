from db import *

print(json.dumps(json.loads(User.objects().to_json()), sort_keys=True, indent=4))
