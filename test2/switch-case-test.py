class Main:

    def zero(arg):
        print("zero was called with arg=" + arg)

    def one(arg):
        print("one was called")

    options = {
        0: zero,
        1: one
    }

    def __init__():
        print("asdf")
        Main.options[1]("the arg")

Main.__init__()
