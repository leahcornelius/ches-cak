from chatterbot import ChatBot


def new_ches_cak():
    return ChatBot(
        'Ches Cak',
        storage_adapter="chatterbot.storage.SQLStorageAdapter",
        database_uri='sqlite:///ches cak-database.db',
       preprocessors=[
           'chatterbot.preprocessors.clean_whitespace',
           'chatterbot.preprocessors.unescape_html',
       ],
        logic_adapters=[
            'chatterbot.logic.BestMatch',
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'default_response': ' ',
                "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
            } 
      ]
    )
