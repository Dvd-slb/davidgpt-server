#!/"<path/to/your/virtual/env>"

def choose_joke():
    voice_dir = "<path/to/jokes/folder>"
    jokes = os.listdir(voice_dir)
    joke = random.choice(jokes)
    joke = f"{voice_dir}/{joke}"
    return joke


agi = AGI()
jk = choose_joke()
time.sleep(1)
agi.stream_file(jk[:-4], "#")
time.sleep(1)
