

class FsUtil:

  @staticmethod
  def extract_int(file):
    try:
      with open(file, 'r') as f:
        gig = int(f.readline())
        return gig
    except IOError:
      print("Failed to open file ", file)
      raise

