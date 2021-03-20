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
        if cmd == "commands" or cmd == "!":
            self.send_reply(line, "Supported commands: !wait(only usable at the start of the game!),!engine, !eval, !queue, !time, ")
        elif cmd == "wait" and game.is_abortable():
            game.ping(30, 60)
            self.send_reply(line, "Waiting 30 seconds...")
        elif cmd == "engine":
            self.send_reply(line, "Stockfish dev running on heroku server")
        elif cmd == "eval":
            stats = self.engine.get_stats()
            self.send_reply(line, ", ".join(stats))
        elif cmd == "eval":
            self.send_reply(line, "That's the evaluation of the position according to my engine! ")
        elif cmd == "queue":
            if self.challengers:
                challengers = ", ".join(["@" + challenger.challenger_name for challenger in reversed(self.challengers)])
                self.send_reply(line, "Challenge queue: {}".format(challengers))
            else:
                self.send_reply(line, "No challenges as yet.")
         elif cmd == "time":
            self.send_reply(line, "est = timezone('EST')
                                   print("Time in EST:", datetime.now(est))")
          elif cmd == "fact":
            self.send_reply(line, "This game is also live at https://lichess.org/broadcast/live-games/7nPtJBfr!")
          elif cmd == "joke":
            self.send_reply(line, "
 1. print('What do you get when you cross a snowman with a vampire?')
 2. input()
 3. print('Frostbite!')
 4. print()
 5. print('What do dentists call an astronaut\'s cavity?')
 6. input()
 7. print('A black hole!')
 8. print()
 9. print('What do you call an alligator with a vest?')
 10. input()
 11. print("An investigator!")
 12. input()
 13. print('Why do bees have sticky hair?')
 14. input()
 15. print(' Because they have honey combs!')
                            
    def send_reply(self, line, reply):
        self.xhr.chat(self.game.id, line.room, reply)


class ChatLine():
    def __init__(self, json):
        self.room = json.get("room")
        self.username = json.get("username")
        self.text = json.get("text")
