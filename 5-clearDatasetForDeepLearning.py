########################################################################################################
########################################################################################################
########################################################################################################
# Original Author: Mark Stowell                                                                        #
# Date Created: 6-13-22                                                                                #
# Date of Last Modification: 6-13-22                                                                   #
# Description:                                                                                         #
#   This program is used in conjunction with 3-prepareDatasetForBiLSTMModel.                           #
#                                                                                                      #
#   This huge :) program will recursively remove all files/subdirectories within your main directory.  #
#   It will also remove your main directory. Note, 3-prepareDatasetForDeepLearningFromCSV recreates    #
#   the main directory and subdirectories necessary for our deep learning model.                       #
#                                                                                                      #
#   The combination of program 3 and 4 allows for efficient changes to the splitting of the dataset    #
#   and any other desired alterations.                                                                 #
########################################################################################################
########################################################################################################
########################################################################################################

import shutil

# Change directory name as necessary
shutil.rmtree('./AbortionData')
