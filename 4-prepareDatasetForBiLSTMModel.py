########################################################################################################
########################################################################################################
########################################################################################################
# Original Author: Mark Stowell                                                                        #
# Date Created: 6-13-22                                                                                #
# Date of Last Modification: 6-13-22                                                                   #
# Description:                                                                                         #
#   This code is to help prepare the dataset for the BiLSTM model                                      #
#                                                                                                      #
#   The model requires a specific directory structure (please refer to the                             # 
#   colab doc for structure details).                                                                  #
#                                                                                                      #
#   This code will tranform a csv file into the required directory structure.                          #
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
#         respectively (I think these are HTML encodings).                                             #
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
#   the model utilizing BERT with its accompanying tokenizer utilizes WordPiece and Split Punctuation to handle
#   word vectorization. In this case, we keep punctuation such as comma, period, apostrophe, etc. The model expects
#   these characters and can affect word embeddings (see more info on WordPiece and the vocab set for DistilBERT).

def remove_html_and_other(text):
    new_text = re.sub(r'<a href.*\/a>', ' ', text)
    new_text = re.sub('[.,?!$*/]+ *', ' ', new_text)
    new_text = (new_text.replace('<br /', ' ').
                replace('&#39;', "'").
                replace('<br >', ' ').
                replace('&amp;', '&').
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



filename = "./DataAbortionNLPAugBalanced.csv"
df = pd.read_csv(filename, usecols=['commentTextDisplay','label'], encoding='utf-8')
print(df)

df['commentTextDisplay'] = df['commentTextDisplay'].apply(cleanTxt)
print(df)

df['num_words'] = df.commentTextDisplay.apply(lambda x:len(x.split()))
print(df)
print("Max number of words: " + str(df.num_words.max()))

# To evaluate dataset for anomolies not removed by cleaning
df.to_excel("output.xlsx", sheet_name='Sheet_name_1') 

train_X, test_X, train_y, test_y = model_selection.train_test_split(df['commentTextDisplay'], df['label'], test_size=0.1, random_state = 1000)

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



print("Number of pos in train: ", pos_counter)
print("Number of neg in train: ", neg_counter)
print("Number of neu in train: ", neu_counter)


print("Number of pos in test: ", (pos_counter - train_pos_counter))
print("Number of neg in test: ", (neg_counter - train_neg_counter))
print("Number of neu in test: ", (neu_counter - train_neu_counter))


print("Total number positive comments: " + str(pos_counter))
print("Total number negative comments: " + str(neg_counter))
print("Total number neutral comments: " + str(neu_counter))
