import os
import torch
import pandas as pd
import PIL.Image

# Dataset implementation by Nick Kipshidze

class NYUDepthDataset(torch.utils.data.Dataset):
    def __init__(self, root_dir, csv_index, transform=None):
        self.root_dir = root_dir
        self.csv_index = os.path.join(root_dir, csv_index)
        self.transform = transform

        self.index_df = self.load_csv_index(self.csv_index)
    
    def parse_csv(self, raw_csv):
        lines = raw_csv.split("\n")
        lines.remove("")
        data = [row.split(",") for row in lines]
        return data
    
    def change_index_path(self, path):
        # Before: data/nyu2_train/living_room_0038_out/69.jpg
        # After: nyu_depth_data/nyu2_train/living_room_0038_out/69.jpg
        return os.path.join(self.root_dir, path.strip("data/"))

    def load_csv_index(self, path):
        data = self.parse_csv(open(path, "r").read())

        for row in range(len(data)):
            for col in range(len(data[row])):
                data[row][col] = self.change_index_path(data[row][col])

        index_df = pd.DataFrame(
            columns=["image", "mask"],
            data=data
        )

        return index_df

    def __len__(self):
        return len(self.index_df)

    def __getitem__(self, index):
        image_path, mask_path = list(self.index_df.iloc[index])
        image, mask = PIL.Image.open(image_path), PIL.Image.open(mask_path)

        if self.transform != None:
            image, mask = self.transform(image), self.transform(mask)

        return image, mask