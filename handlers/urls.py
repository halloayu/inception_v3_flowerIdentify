from handlers.fi_handlers import *

handlers = [
    (r'^/flower', FlowerIdentify),
    (r'^/imgPost', IdentifyHandler),
]