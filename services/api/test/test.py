import sys
from datasets import load_dataset
sst_dataset = load_dataset('glue', 'sst2')
count = 0
for blah in sst_dataset['train']:
    if count > 300:
        sys.exit
    print(blah)