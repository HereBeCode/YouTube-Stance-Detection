# Stance Detection in YouTube Comments
<h2> Table of Contents </h2>
<ol>
  <li> Overview </li>
  <li> Python Scripts (1-5) </li>
  <li> Models in Colab
      <ul>
      <li> SVM </li>
      <li> RNN (BiLSTM) </li>
      <li> Transformer Models </li>
      </ul>
</ol>

<h3>1. Overview </h3>
<p> The general purpose of this work is to provide foundational code and workbooks to build machine learning model(s) to predict user stance from a YouTube comment on controversial topics (multiclass text classification: neutral, positive, or negative). While the focus for my work was abortion stance detection, the code provided here can easily be altered to build and train similar models for different controversial topics.
</p>    
<p> This repo includes scripts to handle scraping the YouTube API for comment data for a particular YouTube video, gathering user subscriber info (if desired
    and accessible), the datasets used for training and testing abortion detection models, links to the google colab notebooks used to build, train, and test the models, and
    the models themselves.
</p>

<h3>2. Python Scripts (1-5) </h3>
<p> This section will briefly discuss the utility of each of the nunbered python scripts.</p>
<blockquote> <p> <strong>1-gatherYoutubeData.py</strong> </p>
                <p> This script scrapes the YouTube API for commentThread data from a particular YouTube videoId. A new excel spreadsheet will be generated with all
                attributes including, but not limited to, commentTextDisplay (the actual comment), and userId. You will need to visit the Google Developer Console and sign 
                up for a developer account (you can just use your gmail account). This will allow you to become authorized to use the YouTube API. Most importantly, you 
                will need a YouTube API Key. Please follow the instructions on the Google Developer Console site. Once you have been authorized, follow the comments in this 
                code to utilize the .env file to store and access your API key (helps mask your API key if uploading code to GitHub, etc.). Identifying the videoID: 
                Consider https://www.youtube.com/watch?v=dQw4w9WgXcQ, the videoId for this video is dQw4w9WgXcQ. Review the comments within the code for the variable which 
                holds this videoId and change accordingly. Finally, you are ready to run the script.
                </p>
             <p> <strong> 2-findWhoSubscribedTo.py </strong> </p>
                <p> This script will acquire the subscriber info for a particular user through his/her userId, if the user is subscribed and if the user authorizes such
                requests through the API. The original intent for this code was to acquire an additional feature to use in the SVM model. After running this code, it became 
                clear subscriber info was not an appropriate feature for the model. Unfortunately, many users have restricted the scraping of this info through the API. You
                will be lucky to get 1/3 of all users subscriber info. I would not recommend incorporating subscriber info into your model as an additional feature, but if
                you choose to do so here is the code.
                </p>
             <p> <strong> 3-NLPAug_Balance_Dataset.py </strong> </p>
                <p> Note: this script is available as a notebook on google colab (see 
                </p>
             <p> <strong> 4-prepareDatasetForBiLSTMModel.py </strong> </p>
             <p> <strong> 5-clearDatasetForDeepLearning.py </strong> </p>
</blockquote>
