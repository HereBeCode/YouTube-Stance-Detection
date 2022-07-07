########################################################################################################
########################################################################################################
########################################################################################################
# Original Author: Mark Stowell                                                                        #
# Date Created: 6-13-22                                                                                #
# Date of Last Modification: 6-13-22                                                                   #
# Description:                                                                                         #
#   This code is to help prepare the dataset for the deep learning model found at:                     #
#   https://colab.research.google.com/drive/1FwZ4xVIgCz4Go_e0gfO-NIl2Rf28eZG5#scrollTo=VLEbD0Zja8e7    #
#                                                                                                      #
#   The model requires a specific directory structure (please refer to the                             # 
#   colab doc for structure details).                                                                  #
#                                                                                                      #
#   This code will tranform a csv file into the required directory structure. Note: the default        #
#   split for train and test will be set to 50:50 and will work for large dataset. If you have a       # 
#   smaller dataset, consider using an 80:20, train:test split instead.                                #
#   Note: It would likely be better to manually split your dataset, especially in the case of          #
#         multi-class classification, as train_test_split is not perfect. However, this will save      #
#         you the time of manually splitting, converting to text files, etc.                           #
#                                                                                                      #
#   Note: This code will also clean your dataset of encoding anomolies. From what I can tell from      #
#         limited resources, there exists an issue on the backend with the YouTube API and it's        #
#         encoding of special characters. In general, it appears UTF-8 is the default encoding scheme. #                                                           
#         It would appear most special characters are correctly encoded and returned in readable       #
#         form following an API request. However, there are some special characters such as the        #
#         single quote (') and double quote (") which are incorrectly returned as &#39; and &quot,     #
#         respectively.                                                                                #
########################################################################################################
########################################################################################################
########################################################################################################
import os
import re
import pandas as pd
from sklearn import model_selection


# Important note on cleaning dataset:
#   Some pretrained models such as BERT, DistilBERT, etc. are paired with trained tokenizers.
#   Such tokenizers may or may not handle and/or expect punctuation. Refer to your model's documentation
#   to determine whether or not to clean the text of punctuation (all or some) before doing so. For example,
#   the model utilizing DistilBERT with its accompanying tokenizer utilizes WordPiece and Split Punctuation to handle
#   word vectorization. In this case, we keep punctuation such as comma, period, apostrophe, etc. The model expects
#   these characters and can affect how words are vectorized (see more info on WordPiece and the vocab set for DistilBERT).

def remove_html_and_other(text):
    new_text = re.sub(r'<a href.*\/a>', ' ', text)
    new_text = re.sub('[.,?!$*/]+ *', ' ', new_text)
    new_text = (new_text.replace('<br /', ' ').
                replace('&#39;', "'").
                replace('<br >', ' ').
                replace('<br>', ' ').
                replace('\u2026', ' ').
                replace('&quot;', '"').
                replace('1st', 'first ').
                replace('2nd', 'second ').
                replace('3rd', 'third ').
                replace('100%', 'one hundred percent ')
    )
    return new_text

def remove_non_alphabets(text):
    new_text = ""
    for x in range(len(text)):
        if(re.match('[a-zA-z\ ]+', text[x])):
            new_text += text[x]
    return new_text


def cleanTxt(text):
    TEXT = text.lower()
    TEXT = remove_html_and_other(TEXT)
    TEXT = remove_non_alphabets(TEXT)
    return TEXT



filename = "./DataAbortion.csv"
df = pd.read_csv(filename, usecols=['commentTextDisplay','Standing'], encoding='utf-8')
print(df)

df['commentTextDisplay'] = df['commentTextDisplay'].apply(cleanTxt)
print(df)

df['num_words'] = df.commentTextDisplay.apply(lambda x:len(x.split()))
print(df)
print("Max number of words: " + str(df.num_words.max()))

# To evaluate dataset for anomolies not removed by cleaning
df.to_excel("output.xlsx", sheet_name='Sheet_name_1') 

train_X, test_X, train_y, test_y = model_selection.train_test_split(df['commentTextDisplay'], df['Standing'], test_size=0.2, random_state = 1000)

# Change the value held by this variable accordingly
main_directory = './AbortionData'

if not os.path.exists('%s' %(main_directory)):
    os.makedirs('%s/train/pos' %(main_directory))
    os.makedirs('%s/train/neg' %(main_directory))
    os.makedirs('%s/train/neu' %(main_directory))
    os.makedirs('%s/test/pos' %(main_directory))
    os.makedirs('%s/test/neg' %(main_directory))
    os.makedirs('%s/test/neu' %(main_directory))
    

train_directory = ('%s/train' %(main_directory))
test_directory = ('%s/test' %(main_directory))

pos_counter = 0
neg_counter = 0
neu_counter = 0

for x in range (len(train_X)):
    if(train_y.iloc[x] == 1):                                                                               # i.e. if review positive...
        f = open('%s/pos/1_%s.txt' %(train_directory, str(pos_counter)), 'w', encoding='utf-8')
        f.write(train_X.iloc[x])
        f.close()
        pos_counter += 1
    elif(train_y.iloc[x] == 2):                                                                             # i.e. review is negative...
        f = open('%s/neg/2_%s.txt' %(train_directory, str(neg_counter)), 'w', encoding='utf-8')
        f.write(train_X.iloc[x])
        f.close()
        neg_counter += 1
    elif(train_y.iloc[x] == 0):                                                                             # i.e. review is neutral...
        f = open('%s/neu/0_%s.txt' %(train_directory, str(neu_counter)), 'w', encoding='utf-8')
        f.write(train_X.iloc[x])
        f.close()
        neu_counter += 1 
    else:
        None

print("Number of pos in train: ", pos_counter)
print("Number of neg in train: ", neg_counter)
print("Number of neu in train: ", neu_counter)
train_pos_counter = pos_counter
train_neg_counter = neg_counter
train_neu_counter = neu_counter

for x in range (len(test_X)):
    if(test_y.iloc[x] == 1):                                                                                # i.e. if review positive...
        f = open('%s/pos/1_%s.txt' %(test_directory, str(pos_counter)), 'w', encoding='utf-8')
        f.write(test_X.iloc[x])
        f.close()
        pos_counter += 1
    elif(test_y.iloc[x] == 2):                                                                              # i.e. review is negative...
        f = open('%s/neg/1_%s.txt' %(test_directory, str(neg_counter)), 'w', encoding='utf-8')
        f.write(test_X.iloc[x])
        f.close()
        neg_counter += 1
    elif(test_y.iloc[x] == 0):                                                                             # i.e. review is neutral...
        f = open('%s/neu/0_%s.txt' %(test_directory, str(neu_counter)), 'w', encoding='utf-8')
        f.write(test_X.iloc[x])
        f.close()
        neu_counter += 1 
    else:
        None
print("Number of pos in test: ", (pos_counter - train_pos_counter))
print("Number of neg in test: ", (neg_counter - train_neg_counter))
print("Number of neu in test: ", (neu_counter - train_neu_counter))
