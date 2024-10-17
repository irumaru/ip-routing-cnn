import matplotlib.pyplot as plt

def generate(df, sn):
  x = df["Timestamp"]
  y = df["Length"]

  plt.scatter(x, y)
  plt.xlabel("Timestamp")
  plt.ylabel("Length")

  plt.savefig(f"flow-{sn}.png")
