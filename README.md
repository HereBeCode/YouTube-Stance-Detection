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
<p> This section will briefly discuss the utility of each of the nunbered python scripts. They include: </p>
<blockquote> <p> 1-gatherYoutubeData.py </p>
             <p> 2-findWhoSubscribedTo.py </p>
             <p> 3-NLPAug_Balance_Dataset.py </p>
             <p> 4-prepareDatasetForBiLSTMModel.py </p>
             <p> 5-clearDatasetForDeepLearning.py </p>
</blockquote>
