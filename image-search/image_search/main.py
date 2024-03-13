from PIL import Image
from sentence_transformers import SentenceTransformer
import vecs
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
import argparse
import os

# Assuming you have set these environment variables
# DB_CONNECTION = os.getenv("SUPABASE_DB_CONNECTION")
DB_CONNECTION = "postgresql://postgres:postgres@localhost:54322/postgres"

# def seed():
    
#   # create vector store client
#   vx = vecs.create_client(DB_CONNECTION)

#   # create a collection of vectors with 3 dimensions
#   images = vx.get_or_create_collection(name="image_vectors", dimension=512)

#   # Load CLIP model
#   model = SentenceTransformer('clip-ViT-B-32')
  
#   folder_path = './official_images'
#   records = []

#   # Encode an image:
#   img_emb1 = model.encode(Image.open('./official_images/Bengals.jpg'))
  
#   # add records to the *images* collection
#   images.upsert(
#       records=[
#           (
#               "Bengals.jpg",        # the vector's identifier
#               img_emb1,          # the vector. list or np.array
#               {"type": "jpg"}   # associated  metadata
#           ), (
#               "Canyon.jpg",
#               img_emb2,
#               {"type": "jpg"}
#           ), (
#               "Horse.jpg",
#               img_emb3,
#               {"type": "jpg"}
#           ), (
#               "RedCar.jpg",
#               img_emb4,
#               {"type": "jpg"}
#           ), (
#               "Dogs.jpg",
#               img_emb5,
#               {"type": "jpg"}
#           ), (
#               "UnitedStatesFlag.jpg",
#               img_emb6,
#               {"type": "jpg"}
#           ), (
#               "BugsBunny.jpg",
#               img_emb7,
#               {"type": "jpg"}
#           )
          
#       ]
#   )
#   print("Inserted images")

#   # index the collection for fast search performance
#   images.create_index()
#   print("Created index")
  
def seed():
    # Assuming DB_CONNECTION and vecs are defined and imported elsewhere
    vx = vecs.create_client(DB_CONNECTION)
    images = vx.get_or_create_collection(name="image_vectors", dimension=512)

    # Load CLIP model
    model = SentenceTransformer('clip-ViT-B-32')

    folder_path = './official_images'
    records = []

    # Traverse the official_images folder and process each image
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.jpg')):
            file_path = os.path.join(folder_path, filename)
            print("Processing:", file_path)
            # Encode the image
            img_emb = model.encode(Image.open(file_path))

            # Prepare the record for upsertion
            records.append(
                (
                    filename,       # the vector's identifier
                    img_emb,        # the vector
                    {"type": "jpg"} # associated metadata
                )
            )
    # print(records)
    # add records to the *images* collection if any images were found
    if records:
        images.upsert(records=records)
        print("Inserted images")

        # index the collection for fast search performance
        images.create_index()
        print("Created index")
    else:
        print("No images found to insert.")
    
      
def textsearch():
  # create vector store client
  vx = vecs.create_client(DB_CONNECTION)
  images = vx.get_or_create_collection(name="image_vectors", dimension=512)

  # Load CLIP model
  model = SentenceTransformer('clip-ViT-B-32')
  # Encode text query
  query_string = "nfl"
  
  text_emb = model.encode(query_string)
  

  # query the collection filtering metadata for "type" = "jpg"
  results = images.query(
      data=text_emb,                      # required
      limit=1,                            # number of records to return
      filters={"type": {"$eq": "jpg"}},   # metadata filters
  )
  result = results[0]
  print(result)
  plt.title(result)
  image = mpimg.imread('./images/' + result)
  plt.imshow(image)
  plt.show()


def imagesearch(query_image_path):
  print("Searching for similar images...")
  print("Query Image:", query_image_path)
  # create vector store client
  vx = vecs.create_client(DB_CONNECTION)
  images = vx.get_or_create_collection(name="image_vectors", dimension=512)

  # Load CLIP model
  model = SentenceTransformer('clip-ViT-B-32')
  
  # Encode an image as the query instead of text
  # query_image_path = './images/Bengals.jpg'  # Path to the query image
  query_img_emb = model.encode(Image.open(query_image_path))

  # query the collection using the image embedding
  results = images.query(
    data=query_img_emb,                   # Use image embedding for the query
    limit=3,                              # Number of records to return
    filters={"type": {"$eq": "jpg"}},     # Metadata filters (adjust as needed)
  )
  
  if results:
    for result in results:
      result
      print(result)
      
      # Assuming `result` contains the filename of the matching image
      result_image_path = './official_images/' + result if not result.startswith('./') else result
      
      # Load and display the result image
      plt.title("Query Result: " + result)
      image = mpimg.imread(result_image_path)
      plt.imshow(image)
      plt.show()
  else:
    print("No matching images found.")


def rename_to_jpg():
  print("Renaming images to .jpg format...")
  # Specify the directory containing the images
  directory = './official_images'

  # Loop through all files in the directory
  for filename in os.listdir(directory):
    # Check if the file has a .jpeg extension
    if filename.endswith('.jpeg'):
      # Construct the full file path
      old_file = os.path.join(directory, filename)
      # Replace the .jpeg extension with .jpg
      new_file = os.path.join(directory, filename[:-5] + '.jpg')
      # Rename the file
      os.rename(old_file, new_file)
      print(f'Renamed: {old_file} to {new_file}')

  print("Renaming complete.")
    
    
    

def cli_imagesearch():
  parser = argparse.ArgumentParser()
  parser.add_argument("filepath", help="give the .jpg file path")

  args = parser.parse_args()
  imagesearch(args.filepath)

    
def cli_textsearch():
  parser = argparse.ArgumentParser()
  parser.add_argument("query", help="give the query string")

  args = parser.parse_args()
  imagesearch(args.filepath)