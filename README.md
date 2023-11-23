# Mining Social Media Data for Revealing Public Attitudes toward Mobile Cabin Hospitals
 
## !!! As the paper is under review, all contents in this repository currently are not allowed to be re-used by anyone until this announcement is deleted.

# 1. Summary of supplemental materials
This table below shows all supplemental materials. All sheets in Tables S1, S2, and S3 are arranged in the order shown in this table.

![image]( https://github.com/0AnonymousSite0/Mining-Social-Media-Data-for-Revealing-Public-Attitudes-toward-Mobile-Cabin-Hospitals/blob/main/Screenshots%20for%20model%20developments/Inventory%20of%20supplemental%20materials.png)

# 2. General Introduction

2.1 This repository aims at providing the codes and data regarding the paper entitled “……” for the public, and it is developed by University of XXX in UK,  The University of XXX in Hong Kong SAR, and XXX University in China.

2.2 We greatly appreciate the selfless spirits of these voluntary contributors of a series of open python libraries, including Bert (https://github.com/google-research/bert), Tensorflow (https://github.com/tensorflow/models), pytorch (https://github.com/pytorch/pytorch), Keras (https://github.com/keras-team/keras), Numpy (https://numpy.org/), labelImg (https://github.com/tzutalin/labelImg), pyExcelerator (https://github.com/WoLpH/pyExcelerator), some base works (https://github.com/yongzhuo/Keras-TextClassification, https://github.com/zjunlp/DeepKE/tree/master), and so on. Our work stands on the shoulders of these giants.

2.3 As for anything regarding the copyright, please refer to the MIT License or contact the authors.

# 3 Repository reuse 
## 3.1 Set environment 
All codes are developed on Python 3.7, and the IDE adopted is PyCharm (Professional version). The codes also support the GPU computing for higher speed; the Navida CUDA we adopted is V10.0.130. The GIS platform is Arcgis Pro 2.3, and its license is necessary. 

•	gensim==3.7.1

•	jieba==0.39

•	numpy==1.16.2

•	pandas==0.23.4

•	scikit-learn==0.19.1

•	tflearn==0.3.2

•	tqdm==4.31.1

•	passlib==1.7.1

•	keras==2.2.4

•	keras-bert==0.41.0

•	keras-xlnet==0.16.0

•	keras-adaptive-softmax==0.6.0


Before submitting these codes to Github, all of them have been tested to be well-performed (as shown in the screwshots). Even so, we are not able to guarantee their operation in other computing environments due to the differences in the python version, computer operating system, and adopted hardware.

## 3.2 Download the embedding models 
![image]( https://github.com/0AnonymousSite0/Mining-Social-Media-Data-for-Revealing-Public-Attitudes-toward-Mobile-Cabin-Hospitals/blob/main/Screenshots%20for%20model%20developments/embeddings.png)
Embeddings are available through this link (https://drive.google.com/drive/folders/1oG5OD3u6-igaUfYAw9ekMQYJzJZisR8A?usp=sharing)
## 3.3 Reuse or Retrain the models 
### 3.3.1 Models directly for reuses
![image]( https://github.com/0AnonymousSite0/Mining-Social-Media-Data-for-Revealing-Public-Attitudes-toward-Mobile-Cabin-Hospitals/blob/main/Screenshots%20for%20model%20developments/Developed%20sentiment%20analysis%20models.png)

Developed models for sentiment analysis models (https://drive.google.com/drive/folders/1oG5OD3u6-igaUfYAw9ekMQYJzJZisR8A?usp=sharing)

![image]( https://github.com/0AnonymousSite0/Mining-Social-Media-Data-for-Revealing-Public-Attitudes-toward-Mobile-Cabin-Hospitals/blob/main/Screenshots%20for%20model%20developments/Developed%20topic%20classification%20models.png)

Developed models for topic classification models (https://drive.google.com/drive/folders/1oG5OD3u6-igaUfYAw9ekMQYJzJZisR8A?usp=sharing)
### 3.3.2 Codes for retraining the models

![image](https://github.com/0AnonymousSite0/Mining-Social-Media-Data-for-Revealing-Public-Attitudes-toward-Mobile-Cabin-Hospitals/blob/main/Screenshots%20for%20model%20developments/codes%20for%20developing%20sentiment%20analysis%20models.png)
Codes for retraining the sentiment analysis models

![image]( https://github.com/0AnonymousSite0/Mining-Social-Media-Data-for-Revealing-Public-Attitudes-toward-Mobile-Cabin-Hospitals/blob/main/Screenshots%20for%20model%20developments/codes%20for%20developing%20topic%20classification%20models.png)
Codes for retraining the topic classification models

