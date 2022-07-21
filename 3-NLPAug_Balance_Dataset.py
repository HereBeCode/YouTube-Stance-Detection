# Additional dependencies:
#   transformers    (pip install transformers)
#   torch           (pip install torch)

import nlpaug
import pandas as pd
import nlpaug.augmenter.word.context_word_embs as aug
import re
import numpy as np

filename = "./DataAbortion.csv"
df = pd.read_csv(filename, usecols=['commentTextDisplay','label'], encoding='utf-8')
print(df)

df = df[(df.label == 0) | (df.label == 1) | (df.label == 2)]
df = df.astype({'label': int})
print(df)

def remove_html_and_other(text):
    new_text = re.sub(r'<a href.*\/a>', ' ', text)
    new_text = (new_text.replace('<br /', ' ').
                replace('<b>', ' ').
                replace('</b>', ' ').
                replace('&#39;', "\u0027").
                replace('<br >', ' ').
                replace('&amp;', '&').
                replace('<br>', ' ').
                replace('\u2026', ' ').
                replace('&quot;', '\u0022').
                replace('1st', 'first ').
                replace('2nd', 'second ').
                replace('3rd', 'third ').
                replace('100%', 'one hundred percent ')
    )
    return new_text

def cleanTxt(text):
    TEXT = text.lower()
    TEXT = remove_html_and_other(TEXT)
    return TEXT

df['commentTextDisplay'] = df['commentTextDisplay'].apply(cleanTxt)
print(df)

print(df['label'].value_counts())

augmenter = aug.ContextualWordEmbsAug(model_path='bert-base-uncased', action='insert', device='cuda')

from tqdm.auto import tqdm
import numpy as np
from sklearn.utils import shuffle

def augmentMyData(df, augmenter, stance, repetitions=1, samples=1000):
    augmented_texts = []
    # select only the minority class samples
    truncated_df = df[df['label'] == stance].reset_index(drop=True) # removes unecessary index column
    for i in tqdm(np.random.randint(0, len(truncated_df), samples)):
        # generating 'n_samples' augmented texts
        for _ in range(repetitions):
            augmented_text = augmenter.augment(truncated_df['commentTextDisplay'].iloc[i])
            augmented_texts.append(augmented_text)
    
    data = {
        'label': stance,
        'commentTextDisplay': augmented_texts
    }
    aug_df = pd.DataFrame(data)
    df = shuffle(df.append(aug_df).reset_index(drop=True))
    return df

num_positive = 0
num_negative = 0
num_neutral = 0
for x in range(len(df)):
  if (df['label'].iloc[x] == 0):
    num_neutral += 1
  elif (df['label'].iloc[x] == 1):
    num_positive += 1
  elif (df['label'].iloc[x] == 2):
    num_negative += 1
  else:
    None
print("Positive: " + str(num_positive))
print("Negative: " + str(num_negative))
print("Neutral: " + str(num_neutral))

# Must pass stance into augmentMyData method
# stance is one of [0, 1, 2] where 0 = neutral, 1 = positive, 2 = negative
if (max(num_positive, num_negative, num_neutral) is num_positive):
  diff_neg = num_positive - num_negative
  diff_neu = num_positive - num_neutral
  aug_df = augmentMyData(df, augmenter, stance=2, samples=diff_neg)
  aug_df = augmentMyData(aug_df, augmenter, stance=0, samples=diff_neu)
elif (max(num_positive, num_negative, num_neutral) is num_negative):
  diff_pos = num_negative - num_positive
  diff_neu = num_negative - num_neutral
  aug_df = augmentMyData(df, augmenter, stance=1, samples=diff_pos)
  aug_df = augmentMyData(aug_df, augmenter, stance=0, samples=diff_neu)
elif (max(num_positive, num_negative, num_neutral) is num_neutral):
  diff_pos = num_neutral - num_positive
  diff_neg = num_neutral - num_negative
  aug_df = augmentMyData(df, augmenter, stance=1, samples=diff_pos)
  aug_df = augmentMyData(aug_df, augmenter, stance=2, samples=diff_neg)
else:
  None

print(aug_df['label'].value_counts())

print(aug_df)

aug_df.to_excel('balanced_dataset.xlsx')