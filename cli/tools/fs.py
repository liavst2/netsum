

class FsUtil:

  @staticmethod
  def extract_int(file):
    try:
      with open(file, 'r') as f:
        return int(f.readline())
    except IOError:
      print("Failed to open file ", file)
      raise

