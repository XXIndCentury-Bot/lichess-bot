from time import time

class Conversation():
    def __init__(self, game, engine, xhr, version, challenge_queue):
        self.game = game
        self.engine = engine
        self.xhr = xhr
        self.version = version
        self.challengers = challenge_queue

    command_prefix = "!"

    def react(self, line, game):
        print("*** {} [{}] {}: {}".format(self.game.url(), line.room, line.username, line.text.encode("utf-8")))
        if (line.text[0] == self.command_prefix):
            self.command(line, game, line.text[1:].lower())
        pass

    def command(self, line, game, cmd):
        elif cmd == "!":
            self.send_reply(line, "Supported commands: !wait(only usable at the start of the game!),!engine, !eval, !fact, !time(if someone can help me out with this, I would be grateful; currently not working.")
        elif cmd == "wait" and game.is_abortable():
            game.ping(30, 60)
            self.send_reply(line, "Waiting 30 seconds...")
        elif cmd == "engine":
            self.send_reply(line, "Stockfish dev running on heroku server")
        elif cmd == "eval":
            stats = self.engine.get_stats()
            self.send_reply(line, ", ".join(stats))
        elif cmd == "eval":
            self.send_reply(line, "That's the evaluation of the position according to my engine!")
        elif cmd == "fact":
            self.send_reply(line, "This game is also live at https://lichess.org/broadcast/live-games/7nPtJBfr!")

    def send_reply(self, line, reply):
        self.xhr.chat(self.game.id, line.room, reply)


class ChatLine:
    def __init__(self, json):
        self.room = json.get("room")
        self.username = json.get("username")
        self.text = json.get("text")
