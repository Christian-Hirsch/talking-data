
# Talking Data -- Overview

[TalkingData](https://www.talkingdata.com/) is one of the largest mobile-service provider's in China. The [TalkingData Kaggle Competition](https://www.kaggle.com/c/talkingdata-mobile-user-demographics) is about predicting age and gender of the mobile user based on App-data. In this readme, I provide a rough high-level overview of my final submission.

## Result -- LB-Score 2.2475 -> Top 31%

My highest-scoring submission has an [LB-Score](https://www.kaggle.com/c/talkingdata-mobile-user-demographics/leaderboard) of 2.2475 which gives a top 31% position in the public LB. The top score on the public LB was 2.155.

## Method

My score was achieved by first partitioning the data into two patches: for about two-thirds of the devices no app usage information is available. Achieving good predictions on these devices is much harder. Therefore, our predictions are based on two steps. A single XGB classifier fitted on the dataset without events, and a single fitted on the dataset for which more detailed information are available.

## Scoring

The competition is a multi-class classification problem. For each device, we produce a 12-dimensional vector describing the probabilities of a data point being associated to one of the given age-gender classes. The performance is measured using cross-entropy loss.

## Feature Engineering

Since only about a third of the training and test data device ids that have associated events,  we split the dataset into two parts for which separate classifiers are trained. 

## Feature Engineering -- devices without events

For those device ids that do not have any events associated with them, we can only use the data from *phone_brand_device_model.csv*.

### Phone brand and device model

To create simple yet powerful features, we label-encode the phone brand and device model. Since the number of device models is large, a prefix is extracted from the name. This should help to aggregate isolated and rare devices.

In a further step, we use a crosstab-encoding for the device-model and phone-brand data. That is, for each device-model we compute the log-likelihoods of the histogram and save this 24-dimensional vector as a feature characterizing the device-model or phone-brand.

## Feature Engineering -- devices with events

For devices that do have some data associated with them, there are two more sources from which we can extract features, namely *events.csv* and *app_events.csv*

### Features from events

In the events data, we first count how many apps are installed at the device. As a second feature group, we compute the histogram of the app usage in time. 

### Features from apps associated with events

In the final round, we generate four types of features extracted from app usage. 

- The first is a simple counts on the number of installed and active apps. 
- Next, we create bags of features for the installed apps and their associated labels. 
- The third feature is derived  by taking predictions from neural network fitted on the bags. 
- Finally, we use a crosstab-encoding similar to what we have done for the device models. By this encoding, we can associate to each user a collection of 12-dimensional vectors. Now, we compute a GMM on that collection.
