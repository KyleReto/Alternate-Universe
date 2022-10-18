from operator import is_
import gpt_2_simple as gpt2
import os
from dotenv import load_dotenv
load_dotenv()
MODEL_NAME = os.getenv('GPT_2_MODEL')

if not os.path.isdir(os.path.join("models", MODEL_NAME)):
	print(f"Downloading {MODEL_NAME} model...")
	gpt2.download_gpt2(model_name=MODEL_NAME)

file_name = "scrapes/completeScrape.txt"

sess = gpt2.start_tf_sess()

# If the model is a larger model, change the finetune() parameters to match
is_large_model = False
if MODEL_NAME == '774M' or MODEL_NAME == '1558M':
    is_large_model = True
    print("Model is a large size, the program will use appropriate parameters.")

# Note that this may occasionally crash due to mishandled unicode output when printing text.
# This can be fixed by setting sample_every to 1000 or so, but then you won't be able to see how the model is progressing.
gpt2.finetune(sess,
              file_name,
              model_name=MODEL_NAME,
              sample_every=1000,
              save_every=20,
              # Memory saving gradients are not available in this version of TF.
              only_train_transformer_layers=is_large_model,
              accumulate_gradients=1 if is_large_model else 5,
              restore_from='latest',
              overwrite=True,
              steps=1000)