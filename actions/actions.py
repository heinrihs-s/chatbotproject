import os
from typing import Text
from rasa_sdk import Action
from actions.clients.mailchimp_client import MailChimpClient


class ActionAboutMe(Action):
    def name(self):
        return "action_about_me"

    def run(self, dispatcher, tracker, domain):
        message = {
            "type":"template",
            "payload":{
                "template_type":"generic",
                "elements":[
                    {
                        "title":"Visit our website",
                        "buttons":[
                            {
                                "title":"Project GitLab",
                                "url": "https://gitlab.com/langnerd/chatbot-engine"
                            }
                        ]
                    }
                ]
            }
        }
        dispatcher.utter_message(attachment=message)
        return []


class ActionCheerUp(Action):
    def name(self):
        return "action_cheer_up"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_cheer_up", tracker)
        dispatcher.utter_template("utter_did_that_help", tracker)
        return []


class ActionContribute(Action):
    def name(self):
        return "action_contribute"

    def run(self, dispatcher, tracker, domain):
        message = {
            "type":"template",
            "payload":{
                "template_type":"generic",
                "elements":[
                    {
                        "title":"See how you can make a difference!",
                        "buttons":[
                            {
                                "title":"Become a contributor",
                                "url": "https://gitlab.com/langnerd/chatbot-engine"
                            }
                        ]
                    }
                ]
            }
        }
        dispatcher.utter_message(attachment=message)
        return []


class ActionDefaultFallback(Action):
    def name(self):
        return "action_default_fallback"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_template("utter_default_fallback", tracker)
        return []


class ActionSubscribe(Action):
    """Asks for the user's email, calls the newsletter API and signs the user up"""
    def name(self) -> Text:
        return "action_subscribe"

    def run(self, dispatcher, tracker, domain):
        email = next(tracker.get_latest_entity_values("email"), None)

        if email:
            client = MailChimpClient(os.getenv('MAILCHIMP_API_KEY'), os.getenv('MAILCHIMP_USER'))
            # if the email is already subscribed, this returns False
            added_to_list = client.subscribe(os.getenv('MAILCHIMP_LIST_ID'), email)

            # utter submit template
            if added_to_list:
                dispatcher.utter_message(template="utter_confirmation_email")
            else:
                dispatcher.utter_message(template="utter_already_subscribed")
        else:
            # no entity was picked up, we want to ask again
            dispatcher.utter_message(template="utter_no_email")

        return []

