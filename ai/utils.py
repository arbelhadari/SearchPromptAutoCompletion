CONFIG_PATH = "AI\config.json"

END_PROMPT = "#"

END_PROGRAM = "quit"

ROLE_PROMPT = """for the following prompts, suggest auto complete as if you are the google auto complete feature. suggest 5 options.
consider the previous prompts (excluding the first one) as context for the next prompt's suggestions to an extent.
your output should be the suggestions only, numbered, and with no punctuations beside dot."""