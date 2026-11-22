import json
from cs329z_hw1.llm import LM
from cs329z_hw1.types import Email, LMCallable
lm = LM() # the model we grade with


def run_priority(email: Email, lm: LMCallable) -> dict:
    """Problem (priority).

    Classify one email for its recipient, calling the model through ``lm``.
    Return {"category": "urgent" | "normal" | "ignore" | "unknown", "reason": str}.
    ``unknown`` means the reply stated no label.

    Rules the tests check:
    * Whatever the model replies, ``category`` is one of the four lower-case
      values and ``reason`` is a non-empty string.
    * A reply with no label word in it (empty, whitespace, text that names
      none of the three) gives "unknown", not a guess.
    * Live: the real model never gets "unknown".
    * The function does not raise and does not modify ``email``.
    * Live: at least 85% agreement with tests/fixtures/priority_gold.json.
    """
    
    with open('email_priority_prompt') as fp:
        instruction = fp.read()
    reply = lm([{"role": "system", "content": instruction}, {"role": "user", "content": json.dumps(email)}])
    print(reply)
    return json.loads(reply) 

test = {""}
test.
run_priority()
