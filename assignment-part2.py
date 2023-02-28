from datetime import datetime

import dtlpy as dl
if dl.token_expired():
    dl.login()

# Get the project
project = dl.projects.get(project_name='dinesh-dataloop-assignment')

#create dataset
# dataset = project.datasets.create(dataset_name='dogs')

# Get the dataset
dataset = project.datasets.get(dataset_name='dogs')

#create labels
labels = [{'tag': 'class1', 'color': (1, 1, 1)},
          {'tag': 'class2', 'color': (1, 1, 2)},
          {'tag': 'key', 'color': (1, 1, 3)}]
dataset.add_labels(label_list=labels)

# upload data
dataset.items.upload(local_path=r'C:\Users\Lenovo\Downloads\car-images-dataloop\dogs',
                     remote_path='/dog-folder')


# update the utm to items
filters = dl.Filters()
filters.add(field='name', values='*.jpg')
pages = dataset.items.list(filters=filters)
print('Number of filtered items in dataset: {}'.format(pages.items_count))
rsp = dataset.items.update(None, filters, {"collectedUTM":str(datetime.now())}, None, True)
# print(rsp)


# add annotations

for page in pages:
    for item in page:
        if item.metadata['system']['originalname'] == '1.jpg' or \
                item.metadata['system']['originalname'] == '2.jpg':
            builder = item.annotations.builder()
            builder.add(annotation_definition=dl.Box(top=10, left=10, bottom=100, right=100,
                                                 label='class1'))
            item.annotations.upload(builder)
        elif item.metadata['system']['originalname'] == '7.jpg' or \
                item.metadata['system']['originalname'] == '3.jpg':
            builder = item.annotations.builder()
            builder.add(annotation_definition=dl.Point(5, 4, label='key'))
            builder.add(annotation_definition=dl.Point(15, 20, label='key'))
            builder.add(annotation_definition=dl.Point(15, 30, label='key'))
            builder.add(annotation_definition=dl.Point(15, 40, label='key'))
            builder.add(annotation_definition=dl.Point(15, 50, label='key'))
            builder.add(annotation_definition=dl.Point(15, 60, label='key'))
            item.annotations.upload(builder)
        else:
            builder = item.annotations.builder()
            builder.add(annotation_definition=dl.Box(top=10, left=10, bottom=100, right=100,
                                                 label='class2'))
            item.annotations.upload(builder)

# filter for class1 label
filters = dl.Filters()
filters.add_join(field='label', values='class1')
# Get filtered item list in a page object
pages = dataset.items.list(filters=filters)
# Count the items
print('Number of filtered items in dataset: {}'.format(pages.items_count))
# Iterate through the items - go over all items and print the properties
for page in pages:
    for item in page:
        print(item.metadata['system']['originalname'])
        print(item.id)

# filter for point annotation
filters = dl.Filters(resource=dl.FiltersResource.ITEM)
# Get filtered item list in a page object
filters.add_join(field='label', values='key')
pages = dataset.items.list(filters)
# Count the items
print('Number of filtered items in dataset: {}'.format(pages.items_count))
# Iterate through the items - go over all items and print the properties
for page in pages:
    for item in page:
        print("item id: " + item.id)
        print("item name: " + item.name)
        annotations = annotations = item.annotations.list(filters=dl.Filters(
                             resource=dl.FiltersResource.ANNOTATION,
                             field='type',
                             values='point'),
          page_size=100,
          page_offset=0)
        for anObj in annotations:
            print("Annotation id:" + anObj.id)
            print("Annotation type:" + anObj.type)
            print("Annotation point " + anObj.to_json()['coordinates'])




