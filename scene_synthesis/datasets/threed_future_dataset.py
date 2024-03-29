# 
# Copyright (C) 2021 NVIDIA Corporation.  All rights reserved.
# Licensed under the NVIDIA Source Code License.
# See LICENSE at https://github.com/nv-tlabs/ATISS.
# Authors: Despoina Paschalidou, Amlan Kar, Maria Shugrina, Karsten Kreis,
#          Andreas Geiger, Sanja Fidler
# 

import numpy as np
import pickle

from .utils import parse_threed_future_models


class ThreedFutureDataset(object):
    def __init__(self, objects):
        assert len(objects) > 0
        self.objects = objects

    def __len__(self):
        return len(self.objects)

    def __str__(self):
        return "Dataset contains {} objects with {} discrete types".format(
            len(self)
        )

    def __getitem__(self, idx):
        return self.objects[idx]

    def _filter_objects_by_label(self, label):
        return [oi for oi in self.objects if oi.label == label]

    def get_closest_furniture_to_box(self, query_label, query_size):
        print(query_label)
        objects = self._filter_objects_by_label(query_label)
        print("2")
        mses = {}
        for i, oi in enumerate(objects):
            temp2 = oi.size 
            temp3 = query_size
            temp1 = (temp2 - temp3)**2
            tmp = np.sum(temp1, axis=-1)
            mses[oi] = tmp
        print("4")
        sorted_mses = [k for k, v in sorted(mses.items(), key=lambda x:x[1])]
        #print(objects)
        #print(sorted_mses)
        return sorted_mses[0]
        '''
        if len(sorted_mses) > 0:
            return sorted_mses[0]
        else: 
            return None
        '''

    def get_closest_furniture_to_2dbox(self, query_label, query_size):
        objects = self._filter_objects_by_label(query_label)

        mses = {}
        for i, oi in enumerate(objects):
            mses[oi] = (
                (oi.size[0] - query_size[0])**2 +
                (oi.size[2] - query_size[1])**2
            )
        sorted_mses = [k for k, v in sorted(mses.items(), key=lambda x: x[1])]
        return sorted_mses[0]

    @classmethod
    def from_dataset_directory(
        cls, dataset_directory, path_to_model_info, path_to_models
    ):
        objects = parse_threed_future_models(
            dataset_directory, path_to_models, path_to_model_info
        )
        return cls(objects)

    @classmethod
    def from_pickled_dataset(cls, path_to_pickled_dataset):
        with open(path_to_pickled_dataset, "rb") as f:
            dataset = pickle.load(f)
        return dataset
