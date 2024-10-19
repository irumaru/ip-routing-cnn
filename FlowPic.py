import matplotlib.pyplot as plt

def Generate(df, path):
  x = df["Timestamp"].values.tolist()
  y = df["Length"].values.tolist()

  plt.clf()

  plt.style.use("grayscale")
  plt.ylim(0, 1500)
  plt.axis("off")

  plt.scatter(x, y)

  #plt.xlabel("Timestamp")
  #plt.ylabel("Length")

  plt.savefig(path)
  plt.clf()

  print(f"save: {path}")
