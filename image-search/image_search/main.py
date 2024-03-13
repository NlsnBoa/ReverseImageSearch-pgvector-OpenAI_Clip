from PIL import Image
from sentence_transformers import SentenceTransformer
import vecs
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
import os

# Assuming you have set these environment variables
# DB_CONNECTION = os.getenv("SUPABASE_DB_CONNECTION")
DB_CONNECTION = "postgresql://postgres:postgres@localhost:54322/postgres"

def seed():
    
  # create vector store client
  vx = vecs.create_client(DB_CONNECTION)

  # create a collection of vectors with 3 dimensions
  images = vx.get_or_create_collection(name="image_vectors", dimension=512)

  # Load CLIP model
  model = SentenceTransformer('clip-ViT-B-32')

  # Encode an image:
  img_emb1 = model.encode(Image.open('./images/Bengals.jpg'))
  img_emb2 = model.encode(Image.open('./images/Canyon.jpg'))
  img_emb3 = model.encode(Image.open('./images/Horse.jpg'))
  img_emb4 = model.encode(Image.open('./images/RedCar.jpg'))
  img_emb5 = model.encode(Image.open('./images/Dogs.jpg'))
  img_emb6 = model.encode(Image.open('./images/UnitedStatesFlag.jpg'))
  img_emb7 = model.encode(Image.open('./images/BugsBunny.jpg'))

  # add records to the *images* collection
  images.upsert(
      records=[
          (
              "Bengals.jpg",        # the vector's identifier
              img_emb1,          # the vector. list or np.array
              {"type": "jpg"}   # associated  metadata
          ), (
              "Canyon.jpg",
              img_emb2,
              {"type": "jpg"}
          ), (
              "Horse.jpg",
              img_emb3,
              {"type": "jpg"}
          ), (
              "RedCar.jpg",
              img_emb4,
              {"type": "jpg"}
          ), (
              "Dogs.jpg",
              img_emb5,
              {"type": "jpg"}
          ), (
              "UnitedStatesFlag.jpg",
              img_emb6,
              {"type": "jpg"}
          ), (
              "BugsBunny.jpg",
              img_emb7,
              {"type": "jpg"}
          )
          
      ]
  )
  print("Inserted images")

  # index the collection for fast search performance
  images.create_index()
  print("Created index")
  
  
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


def imagesearch():
  # create vector store client
  vx = vecs.create_client(DB_CONNECTION)
  images = vx.get_or_create_collection(name="image_vectors", dimension=512)

  # Load CLIP model
  model = SentenceTransformer('clip-ViT-B-32')
  
  # Encode an image as the query instead of text
  query_image_path = './images/Bengals.jpg'  # Path to the query image
  query_img_emb = model.encode(Image.open(query_image_path))

  # query the collection using the image embedding
  results = images.query(
      data=query_img_emb,                   # Use image embedding for the query
      limit=1,                              # Number of records to return
      filters={"type": {"$eq": "jpg"}},     # Metadata filters (adjust as needed)
  )
  
  if results:
      result = results[0]
      print(result)
      
      # Assuming `result` contains the filename of the matching image
      result_image_path = './images/' + result if not result.startswith('./') else result
      
      # Load and display the result image
      plt.title("Query Result: " + result)
      image = mpimg.imread(result_image_path)
      plt.imshow(image)
      plt.show()
  else:
      print("No matching images found.")
