import qmpy_rester as qr
import json
import time
import os

PAGE_LIMIT = 107

if not os.path.exists('query_files_C'):
    os.mkdir('query_files_C')


def download_by_batch(batch_num):
    t1 = time.time()
    with qr.QMPYRester() as q:
        kwargs = {
                  'limit': PAGE_LIMIT,
                  'offset': batch_num * PAGE_LIMIT,
                  'element_set': 'C',
                  "ntypes": "1",
                  # 'icsd': 'T',
                  'fields': 'entry_id,icsd_id,unit_cell,sites',
                  "natom": "<13",
                  }
        data = q.get_oqmd_phases(verbose=False, **kwargs)
        # get_optimade_structures
        print(data)
        keys = data.keys()
        print('keys = ', keys)

        links = data.get('links')
        print("links=", links)

        resource = data.get('resource')
        print("resource=", resource)

        # subdata = data.get('data')
        # print("subdata=", subdata)
        meta = data.get('meta')
        response_message = data.get('response_message')
        print("response_message=", response_message)
        print("meta=", meta)
        # print(data['next'])

    t2 = time.time()

    if batch_num == 0:
        print('Size of query dataset is %d.' % data['meta']['data_available'])

    with open('query_files_C/query_' + str(batch_num) + '.json', 'w') as json_file:
        json.dump(data['data'], json_file, indent=2)

    print('Loading Batch %d time %.3f seconds' % (batch_num, t2 - t1))

    if data['links']['next']:
        return True
    else:
        return False


if __name__ == "__main__":
    batch_num = 0
    while download_by_batch(batch_num):
        batch_num = batch_num + 1

