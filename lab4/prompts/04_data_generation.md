Implement the dataset generation step for the project.

Create:

src/dataset_generator.py

The purpose of this script is to automatically generate the image-pair dataset used by the Wavelet Hash practical assignment.

The source images are already stored in:

original_images/

The generated dataset must use this structure:

data/
├── similar/
│   ├── pair_01/
│   │   ├── image1.jpg
│   │   └── image2.jpg
│   ├── pair_02/
│   │   ├── image1.jpg
│   │   └── image2.jpg
│   └── ...
│
└── dissimilar/
    ├── pair_01/
    │   ├── image1.jpg
    │   └── image2.jpg
    ├── pair_02/
    │   ├── image1.jpg
    │   └── image2.jpg
    └── ...

## Dataset split

Loop through the images in original_images/.

Generate approximately:

- 50% similar pairs
- 50% dissimilar pairs

The total number of generated pairs should be based on the number of available source images.

Make the number of pairs configurable rather than hard-coding it.

If the number of source images makes an exact 50/50 split impossible, use the closest possible split.

## Similar pairs

For a similar pair:

- image1 must be based on an original source image.
- image2 must be based on the SAME source image.
- image2 may either remain unchanged or receive exactly ONE randomly selected transformation.

The transformation choice must be random.

Include a configurable probability for leaving the image unchanged.

For example, support a configuration such as:

unchanged_probability = 0.2

The exact probability should be configurable and should not be hard-coded into the transformation logic.

Possible transformations should remain simple and relevant to the practical assignment, such as:

- small rotation
- brightness adjustment
- small amount of noise
- horizontal flip
- small resize/crop operation

Do NOT combine multiple transformations in one pair.

For each similar pair, randomly choose either:

1. no transformation
or
2. exactly one transformation

Keep transformation parameters within reasonable ranges so that the second image remains visually similar to the original.

## Dissimilar pairs

For a dissimilar pair:

- image1 and image2 must come from DIFFERENT source images.
- Do not pair an image with itself.
- Randomly select the second source image.
- Prefer avoiding duplicate unordered pairs if possible.

For example:

image01 + image05

and later:

image05 + image01

should be considered the same pair and should not both be generated.

The dissimilar pair should not apply transformations unless there is a clear reason to do so.

Keep the original image contents unchanged for dissimilar pairs.

## File handling

Use Pillow for image loading and transformations.

Support common image formats such as:

- .jpg
- .jpeg
- .png
- .webp

Preserve the generated pair structure described above.

Save generated images as JPG or PNG consistently.

Do not modify the files inside original_images/.

## Reproducibility

Use a configurable random seed.

For example:

seed = 42

This should allow the same dataset to be regenerated when the same seed and source images are used.

## Naming

Use simple predictable filenames:

image1.jpg
image2.jpg

inside each pair directory.

Do not encode complicated metadata into filenames.

## Safety and validation

The script should:

- check that original_images/ exists
- check that enough source images exist
- ignore unsupported file extensions
- create data/similar/ and data/dissimilar/ automatically
- avoid overwriting original_images/
- clearly report how many pairs were generated
- report the final similar/dissimilar ratio

If the output directories already contain a previous generated dataset, provide a simple option to clear/recreate the generated dataset rather than mixing old and new pairs.

## Keep the implementation simple

This is a university Computer Vision practical assignment.

Do NOT add:

- machine learning
- deep learning
- databases
- configuration frameworks
- web interfaces
- unnecessary classes
- unnecessary abstractions
- complex dataset libraries

A small Python script using Pillow, pathlib, and the standard random module is sufficient.

## Integration

The generated dataset must be compatible with the existing:

src/wavelet_hash.py
src/matching.py
src/evaluation.py

Do not modify those files unless absolutely necessary.

The dataset generator is only responsible for creating the image pairs.

It does NOT perform:

- Wavelet Hashing
- Hamming distance
- matching
- Accuracy calculation
- Sensitivity calculation
- Specificity calculation
- ROC calculation

## Documentation

Create:

prompts/02_dataset_generation.md

and put this complete prompt inside it.

Also update README.md only with a short section explaining:

- original_images/ contains source images
- dataset_generator.py generates similar and dissimilar pairs
- the generated dataset is stored under data/

Do not rewrite the entire README.

After implementation, show:

1. The resulting file tree.
2. The number of source images detected.
3. How many similar pairs and dissimilar pairs the generator will create.
4. The transformations currently supported.
5. How to run the generator.

Do not proceed to modifying main.ipynb yet.