import cProfile
import pstats
import time
from io import StringIO

import caspailleur
import polars as pl
import numpy as np
import fcatng
import multiprocessing
from multiprocessing import Manager
import pandas as pd


class ConceptParallel:
    def __init__(self, extent=[], intent=[]):
        self._extent = np.array(extent)
        self._intent = np.array(intent)
        self._num_extent = np.arange(1, len(extent))
        self._num_intent = np.arange(1, len(intent))

    def get_extent(self):
        return self._extent

    def get_intent(self):
        return self._intent


class ContextParallel:
    def __init__(self, dataframe=pl.DataFrame()):
        self._dataframe = dataframe
        self._num_objs = np.arange(1, len(dataframe["objects"]))
        self._num_attrs = np.arange(1, len(dataframe.columns[1:]))
        self._rows = self.compute_rows_attrs()
        self._table = dataframe[:, 1:].to_numpy()
        self._amount_attrs = dataframe.columns[1:]

    def get_dataframe(self):
        return self._dataframe

    def get_num_objs(self):
        return self._num_objs

    def get_num_attrs(self):
        return self._num_attrs

    def get_rows(self):
        return self._rows

    def get_table(self):
        return self._table

    def get_amount_attrs(self):
        return self._amount_attrs

    def compute_rows_attrs(self):
        dataframe = self.get_dataframe()

        object_mapping = {name: idx for idx, name in enumerate(dataframe["objects"].to_list())}
        attribute_mapping = {col: idx for idx, col in enumerate(dataframe.columns[1:], 1)}

        result = {}

        for attr_name in dataframe.columns[1:]:
            attr_index = attribute_mapping[attr_name]

            filtered = dataframe.filter(pl.col(attr_name) == 1)

            object_indices_with_1 = [object_mapping[obj] for obj in filtered["objects"].to_list()]

            result[attr_index] = np.array(object_indices_with_1) + 1

        return result


def compute_closure(i_concept, i_y, i_context):
    new_intent = np.zeros(shape=len(i_context.get_dataframe()["objects"]), dtype=int)
    new_extent = np.ones(shape=len(i_context.get_dataframe().columns[1:]), dtype=int)

    matching_objects = []

    for i in range(0, len(i_context.get_num_objs())+1):
        if i_concept.get_extent()[i] == 1:
            matching_objects.append(i+1)

    extent = np.array(matching_objects)

    for i in np.intersect1d(extent, i_context.get_rows()[i_y+1]):
        new_extent[i-1] = 1
        for j in range(0, len(i_context.get_num_attrs())+1):
            if i_context.get_table()[i-1, j-1] == 0:
                new_intent[j-1] = 0

    return ConceptParallel(new_extent, new_intent.tolist())


def generate_from(i_concept, i_y, i_context, i_mgr_list):
    r_concept = ConceptParallel()
    skip = True

    i_mgr_list.append(i_concept)

    if np.array_equal(i_concept.get_intent(), i_context.get_num_attrs()) or i_y > len(i_context.get_amount_attrs()):
        return

    for j in range(i_y, len(i_context.get_amount_attrs())):
        if i_concept.get_intent()[j] == 0:

            r_concept = compute_closure(i_concept, j, i_context)
            skip = False

            for k in range(0, j-1):
                if r_concept.get_intent()[k] != i_concept.get_intent()[k]:
                    skip = True
                    break

            if not skip:
                generate_from(r_concept, j+1, i_context, i_mgr_list)

    return


def process_queue_item(queue, i_context, i_mgr_list):
    while not queue.empty():
        try:
            item = queue.get()
            formal_concept = item['formal_concept']
            attribute = item['attribute']
            generate_from(formal_concept, attribute, i_context, i_mgr_list)
        except Exception as e:
            print(f"Fehler in Prozess : {e}")


def parallel_generate_from(i_concept, i_y, i_l, i_context, i_mgr_list, i_manager, i_mgr_queue):
    """
    """
    L = 2 # len(i_context.get_dataframe().columns[1:]) # Recursion Level
    P = 4 # multiprocessing.cpu_count()  # Anzahl der Kerne
    temp_conc = None
    skip = False
    r = None
    processes = []

    if i_l == L:
        r = 0
        q_size = 0
        for queue in i_mgr_queue:
            q_size += queue.qsize()
        r = q_size % P
        i_mgr_queue[r].put({'formal_concept': i_concept, 'attribute': i_y})
        return

    i_mgr_list.append(i_concept)

    if not np.array_equal(i_concept.get_intent(), i_context.get_num_attrs()) or not i_y > len(i_context.get_dataframe().columns[1:]):
        for j in range(i_y, len(i_context.get_dataframe().columns[1:])):
            if i_concept.get_intent()[j] == 0:
                temp_conc = compute_closure(i_concept, j, i_context)
                skip = False

                for k in range(0, j-1):
                    if temp_conc.get_intent()[k] != i_concept.get_intent()[k]:
                        skip = True
                        break

                if not skip:
                    parallel_generate_from(temp_conc, j+1, i_l+1, i_context, i_mgr_list, i_manager, i_mgr_queue)

    if i_l == 0:
        pool_act = multiprocessing.Pool(P-1)
        for r in range(1, P):
            pool_act.apply_async(process_queue_item, args=(i_mgr_queue[r], i_context, i_mgr_list))

        time.sleep(2)

        pool_2 = multiprocessing.Pool(1)
        pool_2.apply_async(process_queue_item, args=(i_mgr_queue[0], i_context, i_mgr_list))

        pool_act.close()
        pool_act.join()

        pool_2.close()
        pool_2.join()

    return


def generate_concepts(i_context, i_cores=multiprocessing.cpu_count()/2):
    if __name__ == '__main__':
        with multiprocessing.Manager() as manager:
            mgr_list = manager.list()
            mgr_queue = [manager.Queue() for _ in range(i_cores)]

            initial_ext = [1 for _ in range(i_context.get_dataframe().height)]
            initial_int = [0 for _ in range(i_context.get_amount_attrs())]
            initial_concept = ConceptParallel(initial_ext, initial_int)

            parallel_generate_from(initial_concept, 0, 0, i_context, mgr_list, manager, mgr_queue)

    return list(mgr_list)