class EventHandler:
    cls_subs = []

    def __init__(self) -> None:
        self.inst_subs = []

    @staticmethod
    def subscribe(name: str):
        def decorator(func):
            setattr(EventHandler, name, func)
            return func
        return decorator

    on_event1 = None
    def event1(self):
        EventHandler.on_event1({"k1": "v1"})

    def trigger(self):
        for func in self.inst_subs:
            func({"k2": "v2"}) #call every function in the list

# app = EventHandler()

class Subject:
    def __init__(self) -> None:
        self.event_handler = EventHandler()
        self.event_handler.inst_subs.append(self.update2)

    @EventHandler.subscribe("on_event1")
    def update1(self, data: dict):
        print("from update1", data)

    def update2(self, data: dict):
        print("from update2", data)

s = Subject()
s.event_handler.trigger()

# s.event_handler.trigger()

# @app.subscriber
# def eventHandler1():
#     print("Event handler 1 called!")
    
# @app.subscriber
# def eventHandler2():
#     print("Event handler 2 called!")

# eventHandler1()

# app.trigger()

# klass = Other()
# # klass.log()
# klass.event.trigger()