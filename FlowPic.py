import matplotlib.pyplot as plt

def Generate(df, path):
  x = df["Timestamp"].values.tolist()
  y = df["Length"].values.tolist()

  plt.clf()

  plt.figure(dpi=100, figsize=(15, 15))
  plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
  plt.style.use("grayscale")
  plt.ylim(0, 1500)
  plt.axis("off")

  plt.scatter(x, y)

  #plt.xlabel("Timestamp")
  #plt.ylabel("Length")

  plt.savefig(path)
  plt.clf()

  print(f"save: {path}")
