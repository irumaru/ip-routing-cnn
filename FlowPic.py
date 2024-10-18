import matplotlib.pyplot as plt

def generate(df, sn):
  x = df["Timestamp"].values.tolist()
  y = df["Length"].values.tolist()

  plt.clf()
  plt.scatter(x, y)
  plt.xlabel("Timestamp")
  plt.ylabel("Length")

  plt.savefig(f"output/flow-{sn}.png")
  plt.clf()
