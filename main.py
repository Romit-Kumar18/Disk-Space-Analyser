import os
import matplotlib.pyplot as plt
import squarify
import seaborn as sns
from collections import defaultdict
from matplotlib.patches import Patch

def get_file_sizes(directory):
    file_sizes = defaultdict(list)

    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(foldername, filename)
            relative_path = os.path.relpath(filepath, directory)
            size = os.path.getsize(filepath)
            file_sizes[relative_path].append((filename, size))

    return file_sizes

def convert_size(size_in_bytes):
    # Convert sizes to kilobytes, megabytes, etc.
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0

def print_file_info(file_sizes):
    folders_printed = set()  # To keep track of printed folders
    for relative_path, files in file_sizes.items():
        folder, _ = os.path.split(relative_path.replace('\\', '/'))  # Replace backslashes with forward slashes
        if folder not in folders_printed:
            print(f"\nFolder: {folder}")
            folders_printed.add(folder)

        for file, size in files:
            formatted_size = convert_size(size)
            print(f"\t{file}: {formatted_size}")

def assign_colors_to_subdirectories(file_sizes):
    subdirectory_colors = {}
    color_index = 0

    for relative_path in file_sizes.keys():
        subdirectory, _ = os.path.split(relative_path.replace('\\', '/'))  # Replace backslashes with forward slashes
        if subdirectory not in subdirectory_colors:
            subdirectory_colors[subdirectory] = sns.color_palette("Set1", n_colors=len(subdirectory_colors) + 1)[color_index]
            color_index += 1

    return subdirectory_colors

def create_legend(ax, subdirectory_colors, file_sizes):
    legend_patches = []
    count=0
    # Add files to legend, including their relative paths
    for relative_path, files in file_sizes.items():
        for file, size in files:
            subdirectory, _ = os.path.split(relative_path.replace('\\', '/'))  # Replace backslashes with forward slashes
            legend_patches.append(Patch(color=subdirectory_colors[subdirectory], label=f"{relative_path} - {file} ({convert_size(size)})"))
            count+=1
        # if count>40:
            # print("Legend truncated due to size limit.")
            # break
    ax.legend(handles=legend_patches, loc='upper left', bbox_to_anchor=(1, 1), title="Legend", fontsize='small')

def plot_treemap(file_sizes):
    labels = []
    sizes = []
    colors = []

    subdirectory_colors = assign_colors_to_subdirectories(file_sizes)

    for idx, (relative_path, files) in enumerate(file_sizes.items()):
        labels.append(relative_path)
        sizes.append(sum(size for _, size in files))
        subdirectory, _ = os.path.split(relative_path.replace('\\', '/'))  # Replace backslashes with forward slashes
        colors.append(subdirectory_colors[subdirectory])

    total_size = sum(sizes)

    if total_size > 0:
        norm_sizes = [(size / total_size) * 100 for size in sizes]

        # Create treemap
        fig, ax = plt.subplots(figsize=(12, 10))
        squarify.plot(sizes=norm_sizes, label=None, color=colors, alpha=0.7, ax=ax)

        # Add border to each rectangle
        for rect, color in zip(ax.patches, colors):
            rect.set_linewidth(1)
            rect.set_edgecolor('black')

        # Create a legend for files including their relative paths
        create_legend(ax, subdirectory_colors, file_sizes)

        # Adjust layout
        plt.axis('off')
        plt.tight_layout()

        plt.show()
    else:
        print("Total size is zero. Cannot create treemap.")

def main():
    directory = input("Enter the path of the directory: ")
    file_sizes = get_file_sizes(directory)

    # Print file information in the terminal
    print_file_info(file_sizes)

    # Plot treemap
    plot_treemap(file_sizes)

if __name__ == "__main__":
    main()
