import logging

from cs329z_hw1.llm import LM
from cs329z_hw1.pipelines.email_pipelines import run_priority, run_daily_digest
from cs329z_hw1.types import Email


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('main')
lm = LM() # the model we grade with


if __name__ == '__main__':
    # urgent
    urgent_email = {"id": "em-04298", "thread_id": "th-03352", "reply_to": None, "to": ["tana.jones@enron.com"], "date": "2001-06-07T15:02:00Z", "subject": "Enron Canada isda with Transalta", "body": "Hi Tana,\n\nThe executed ISDA list says that we=01,ve got one b/t Enron Canada and=20\nTransalta.  Can I get a copy of the docs faxed to me today??\n\nThanks a lot,\n\nLimor\n\nEnron Global Markets\n520 Madison Avenue\nNew York, NY 10022\nTel: 212.715.5283\nFax: 212.715.5608\nE-Mail: Limor.Nissan@Enron.com"}
    normal_email = {"id": "em-00001", "thread_id": "th-00001", "reply_to": None, "from": "s..ward@enron.com", "to": ["jmhpower@aol.com"], "date": "2001-06-01T00:03:01Z", "subject": "RFP Response", "body": "Jim,\n\nAttached is Enron's response to your Request for Natural Gas Supply Proposals.    If you have any questions or comments, please contact me at 713-853-0685.\n\nThank you for your consideration.\n\nSincerely,\n\nKim Ward\nManager, West Gas Origination\n\n "}
    run_daily_digest([normal_email, urgent_email], lm)
    
    

    