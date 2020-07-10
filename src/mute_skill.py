from chatterbot.logic import LogicAdapter


class MuteLogicAdaptor(LogicAdapter):

    def __init__(self, chatbot, **kwargs):
     super().__init__(chatbot, **kwargs)

    def can_process(self, statement):
        return True

    def process(self, input_statement, additional_response_selection_parameters):
        confidence = 0
        if input_statement.text.lower() in ['shut up ches cak', 'be quiet ches cak', 'ches cak mute', 'mute ches cak', 'ches cak shutup']:
            confidence = 1
            print('mute active')

        selected_statement = input_statement
        selected_statement.text = ''
        selected_statement.confidence = confidence
        return selected_statement
