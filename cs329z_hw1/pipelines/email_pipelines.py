import json
import logging
from cs329z_hw1.llm import LM
from cs329z_hw1.types import Email, LMCallable
lm = LM() # the model we grade with

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('main')

VALID_CATEGORIES = {"urgent", "normal", "ignore"}

with open('cs329z_hw1/pipelines/prompt_template_email_urgent_summary.md') as fp:
  prompt_summary_urgent = fp.read()
with open('cs329z_hw1/pipelines/prompt_template_email_normal_summary.md') as fp:
  prompt_summary_normal = fp.read()
with open('cs329z_hw1/pipelines/prompt_template_email_priority_prompt.md') as fp:
  prompt_email_priority = fp.read()

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
    reply = lm([{"role": "system", "content": prompt_email_priority}, {"role": "user", "content": json.dumps(email)}])
    return check_contract(reply)

def run_priority_list(emails: list[Email], lm: LMCallable) -> dict:

    replies = [lm([{"role": "system", "content": prompt_email_priority}, {"role": "user", "content": json.dumps(email)}]) for email in emails]
    replies_checked_contract = [check_contract(reply) for reply in replies]
    ids = [email["id"] for email in emails]
    by_id = dict(zip(ids, replies_checked_contract))
    return by_id

def _lm_simple(system_prompt, user_message, lm):
  return lm([{"role": "system", "content": system_prompt}, {"role": "user", "content": user_message}])
    

def run_daily_digest(emails: list[Email], lm: LMCallable) -> str:
    """Problem (daily_digest).

    ``emails`` is a list of emails from one calendar day (UTC date); it may
    be empty. Return the morning summary as a string.

    Rules the tests check:
    * Returns a string for every model reply, and for an empty day.
    * The function does not modify ``emails``.
    * Live (tests/fixtures/digest_days.json): the digest is not empty and
      at most 300 words (``len(digest.split())``) as the model wrote it; for
      each gold urgent email it contains the name of the company, project or
      site that email is about; it contains no term listed for the gold
      ignore emails.
    """
    email_ids = [email["id"] for email in emails]
    emails_dict = dict(zip(email_ids, emails))
    logger.info(emails_dict )
    
    # step 1. break emails into priority queues as per label. 
    responses = run_priority_list(emails, lm) # id -> {label: urgent, reason: ...}
    with open('cs329z_hw1/pipelines/summary_template.txt') as fp:
      template = fp.read()
    urgent_indices = [indices for indices, rep in responses.items() if rep["category"] == "urgent"]
    emails_urgent = [emails_dict[urgent_index] for urgent_index in urgent_indices]
    
    # step 2. prepare the answer template.
    template = str.replace(template, "<total_email>", str(len(emails)))
    
    # step 3. Append the urgent email summary (incl company name, project or site)
    emails_urgent_summary = _lm_simple(prompt_summary_urgent, json.dumps(emails_urgent), lm)
    logger.info(f"Summary of urgent: {emails_urgent_summary}")
    template = str.replace(template, "<urgent_emails_summary>", emails_urgent_summary)
    
    # step 4. Append the normal, unknown part. 
    normal_indices = [indices for indices, rep in responses.items() if rep["category"] != "urgent" and rep["category"] != "ignore"]
    emails_normal = [emails_dict[normal_index] for normal_index in normal_indices]
    word_count_left = 300 - len(template.split())
    prompt_summary_normal_new = str.replace(prompt_summary_normal, "%word_count%", str(word_count_left))
    emails_normal_summary = _lm_simple(prompt_summary_normal_new, json.dumps(emails_normal), lm)
    template = str.replace(template, "<normal_emails_summary>", emails_normal_summary)
    
    print(template)
    return template