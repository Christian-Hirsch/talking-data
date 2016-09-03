
# coding: utf-8

## TalkingData -- Feature Engineering

# Before we can tap the potential that is buried in the app data, we need to join the apps to the device ids.

# In[1]:

import numpy as np
import pandas as pd
import pickle

#path to data
DATA_PATH = "../../../input/"


# Next, we load the data.

# In[2]:

train = pd.read_csv("{0}gender_age_train.csv".format(DATA_PATH))
test = pd.read_csv("{0}gender_age_test.csv".format(DATA_PATH))
events = pd.read_csv("{0}events.csv".format(DATA_PATH))
apps = pd.read_csv("{0}app_events.csv".format(DATA_PATH))
apps['app_id'] = apps['app_id'].astype(str)


# We merge first with the events data...

# In[ ]:

train_test = pd.concat([train['device_id'], test['device_id']])
train_test_event = pd.merge(train_test.to_frame(), events.loc[:, ['device_id', 'event_id']], 
                       'inner', on = 'device_id').drop_duplicates()


# ... and afterwards with the apps data.

# In[ ]:

train_test_app_raw = pd.merge(train_test_event, apps,'left', on = 'event_id').drop('event_id', axis = 1).drop_duplicates()


# Finally, we pickle the merged dataframe.

# In[ ]:

pickle.dump(train_test_app, open('{0}device_apps_inner'.format(DATA_PATH), 'wb'))

