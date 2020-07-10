from create_chatbot_instance import new_ches_cak
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

# Create a new chat bot named ches cak
chatbot = new_ches_cak()
export = False;

trainer = ChatterBotCorpusTrainer(chatbot)
print("Training custom datasets")
trainer.train(
    "datasets/",
)
print("trained from custom  datasets")

print("finished training")
if (export):
    trainer.export_for_training('./exported_train_data.json')
