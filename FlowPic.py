import matplotlib.pyplot as plt

def Generate(df, path):
  x = df["Timestamp"].values.tolist()
  y = df["Length"].values.tolist()

  plt.clf()
  plt.scatter(x, y)

  plt.ylim(0, 1500)

  #plt.xlabel("Timestamp")
  #plt.ylabel("Length")

  plt.axis("off")

  plt.style.use("grayscale")

  plt.savefig(path)
  plt.clf()

  print(f"save: {path}")
