import requests
import pandas as pd
from PIL import Image

def main():
    r = requests.get('https://isic-archive.com/api/v1/image?limit=300')
    s = r.json()
    data = []
    for i, doc in enumerate(s):
        # fetch each image separately
        r = requests.get('https://isic-archive.com/api/v1/image/%s' % doc['_id'])
        r2 = requests.get('https://isic-archive.com/api/v1/image/%s/download' % doc['_id'])
        image_metadata = r.json()
        # We only want the metadata from each image
        metadata = image_metadata['meta']
        clinical_metadata = metadata['clinical']
        unstructured_metadata = metadata['unstructured']
        
        # do something with this metadata
        complete_metadata = {**clinical_metadata, **unstructured_metadata}
        complete_metadata['num'] = i
        data.append(complete_metadata)

        # read in the image
        image = r2.content
        with open('img/image%03d.jpg' % i, 'wb') as f:
            f.write(image)

        # resize the images to 400x700
        img = Image.open('img/image%03d.jpg' % i)
        img = img.resize((700, 400), Image.ANTIALIAS)
        img.save('img/image%03d.jpg' % i)
    
    data_df = pd.DataFrame(data)
    data_df.to_csv('complete_data.csv')
            
main()
