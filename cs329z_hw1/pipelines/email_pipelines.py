import json
import logging
from cs329z_hw1.llm import LM
from cs329z_hw1.types import Email, LMCallable
lm = LM() # the model we grade with

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('main')

VALID_CATEGORIES = {"urgent", "normal", "ignore"}

def check_contract(reply): 
  default_return = {"category":"unknown", "reason":"incorrect lm reply"}  
  try:
      data = json.loads(reply)
      if not isinstance(data, dict):
        return default_return                      # JSON, but wrong shape
      cat = data.get("category")
      if cat not in VALID_CATEGORIES: 
        return default_return
      return data
  except json.JSONDecodeError:
      return  default_return                   # not JSON at all

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
    logger.info(json.dumps(test, indent=2))
    with open('cs329z_hw1/pipelines/email_priority_prompt.md') as fp:
        instruction = fp.read()
    reply = lm([{"role": "system", "content": instruction}, {"role": "user", "content": json.dumps(email)}])
    logger.info(reply)
    return check_contract(reply)

# urgent
test : Email = {"id": "em-04260", "thread_id": "th-03329", "reply_to": None, "to": ["suzanne.adams@enron.com"], "date": "2001-06-07T14:33:00Z", "subject": "David Marshall", "body": "Could you PLEASE PLEASE call David Marshall and get his email?  I'm on \nendless conference calls and need to contact him about a matter.\n\nThanks,\n\nKay\n\nPS, not a vacation day"}

# test
test : Email = {"id": "em-04324", "thread_id": "th-03352", "reply_to": "em-04298", "to": ["limor.nissan@enron.com"], "date": "2001-06-07T15:19:00Z", "subject": "Re: Enron Canada isda with Transalta", "body": "One note.  We are currently negotiating some credit amendments to this=20\nagreement.\n\n\n\n=09Limor Nissan/ENRON@enronXgate\n=0906/07/2001 03:02 PM\n=09=09=20\n=09=09 To: Tana Jones/HOU/ECT@ECT\n=09=09 cc:=20\n=09=09 Subject: Enron Canada isda with Transalta\n\nHi Tana,\n\nThe executed ISDA list says that we=01,ve got one b/t Enron Canada and=20\nTransalta.  Can you send me a copy of the docs faxed today??\n\nThanks a lot,\n\nLimor\n\nEnron Global Markets\n520 Madison Avenue\nNew York, NY 10022\nTel: 212.715.5283\nFax: 212.715.5608\nE-Mail: Limor.Nissan@Enron.com\n\n"}
test : Email = {"id": "em-04298", "thread_id": "th-03352", "reply_to": None, "from": "limor.nissan@enron.com", "to": ["tana.jones@enron.com"], "date": "2001-06-07T15:02:00Z", "subject": "Enron Canada isda with Transalta", "body": "Hi Tana,\n\nThe executed ISDA list says that we=01,ve got one b/t Enron Canada and=20\nTransalta.  Can I get a copy of the docs faxed to me asap??\n\nThanks a lot,\n\nLimor\n\nEnron Global Markets\n520 Madison Avenue\nNew York, NY 10022\nTel: 212.715.5283\nFax: 212.715.5608\nE-Mail: Limor.Nissan@Enron.com"}

run_priority(test, lm)



