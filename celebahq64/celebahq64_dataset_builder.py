"""celebahq64 dataset."""

import tensorflow_datasets as tfds
import tensorflow as tf

class Builder(tfds.core.GeneratorBasedBuilder):
  """DatasetBuilder for celebahq64 dataset."""

  VERSION = tfds.core.Version('1.0.0')
  RELEASE_NOTES = {
      '1.0.0': 'Initial release.',
  }

  def _info(self) -> tfds.core.DatasetInfo:
    """Returns the dataset metadata."""
    # TODO(celebahqhq): Specifies the tfds.core.DatasetInfo object
    return self.dataset_info_from_configs(
        features=tfds.features.FeaturesDict({
            # These are the features of your dataset like images, labels ...
            'image': tfds.features.Image(shape=(64, 64, 3)),
            'label': tfds.features.ClassLabel(names=['female', 'male']),
        }),
    )

  def _split_generators(self, dl_manager: tfds.download.DownloadManager):
    """Returns SplitGenerators."""

    # TODO(celebahqhq): Returns the Dict[split names, Iterator[Key, Example]]
    return {
        'train': self._generate_examples(),
    }

  def _generate_examples(self):
    """Yields examples."""
    # TODO(celebahqhq): Yields (key, example) tuples from the dataset

    from datasets import load_dataset
    import numpy as np
    dataset = load_dataset("mattymchen/celeba-hq", split='train')
    dataset = dataset.to_tf_dataset()

    def deserialization_fn(data):
      image = data['image']
      image = tf.image.resize(image, (64, 64), method=tf.image.ResizeMethod.BICUBIC, antialias=True)
      return {'image': image, 'label': data['label']}

    dataset = dataset.map(deserialization_fn)
    dataset = tfds.as_numpy(dataset)
    for i, example in enumerate(dataset):
      yield i, {
          'image': example['image'].astype(np.uint8),
          'label': example['label'],
      }
