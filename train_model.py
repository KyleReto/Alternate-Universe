import gpt_2_simple as gpt2
import os

model_name = "124M"
if not os.path.isdir(os.path.join("models", model_name)):
	print(f"Downloading {model_name} model...")
	gpt2.download_gpt2(model_name=model_name)

file_name = "scrapes/completeScrape.txt"

sess = gpt2.start_tf_sess()
gpt2.finetune(sess,
              file_name,
              model_name=model_name,
              sample_every=20,
              save_every=100,
              restore_from='latest',
              overwrite=True,
              steps=1000)   # steps is max number of training steps

#try .generate_to_file()
gpt2.generate(sess,
              length=500,
              temperature=0.7,
              prefix="",
              nsamples=5,
              batch_size=5
              )