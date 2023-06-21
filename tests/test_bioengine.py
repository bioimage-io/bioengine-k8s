import pytest
import asyncio
import subprocess
import micropip

@pytest.fixture
async def install_dependencies():
    try:
        # For pyodide in the browser
        await micropip.install(['pyotritonclient', 'kaibu-utils'])
    except ImportError:
        # For native python with pip
        subprocess.call(['pip', 'install', 'pyotritonclient', 'kaibu-utils'])

@pytest.mark.asyncio
async def test_image_processing1(install_dependencies):
    import io
    from PIL import Image
    import matplotlib.pyplot as plt
    import numpy as np
    from pyotritonclient import execute
    from kaibu_utils import fetch_image

    image = await fetch_image('https://static.imjoy.io/img/img02.png')
    image = image.astype('float32')
    assert image.shape, "Invalid image shape"

    param = {'diameter': 30, 'model_type': 'cyto'}
    # run inference
    results = await execute([image.transpose(2, 0, 1), param],
                                  server_url='https://hypha.imjoy.io/triton',
                                  model_name='cellpose-python',
                                  decode_bytes=True)
    mask = results['mask']
    assert mask.shape, "Invalid mask shape"

@pytest.mark.asyncio
async def test_image_processing2(install_dependencies):
    import io
    from PIL import Image
    import matplotlib.pyplot as plt
    import numpy as np
    from pyotritonclient import execute
    from kaibu_utils import fetch_image

    # obtain the model config
    image = await fetch_image('https://raw.githubusercontent.com/stardist/stardist/3451a4f9e7b6dcef91b09635cc8fa78939fb0d29/stardist/data/images/img2d.tif', grayscale=True)
    image = image.astype('uint16')
    param = {'diameter': 30}

    # run inference
    results = await execute([image, param],
                                  server_url='https://ai.imjoy.io/triton',
                                  model_name='stardist',
                                  decode_bytes=True)
    mask = results['mask']
    assert mask.shape, "Invalid mask shape"

@pytest.mark.asyncio
async def test_image_processing3(install_dependencies):
    LABELS = {
      0: 'Nucleoplasm',
      1: 'Nuclear membrane',
      2: 'Nucleoli',
      3: 'Nucleoli fibrillar center',
      4: 'Nuclear speckles',
      5: 'Nuclear bodies',
      6: 'Endoplasmic reticulum',
      7: 'Golgi apparatus',
      8: 'Intermediate filaments',
      9: 'Actin filaments',
      10: 'Microtubules',
      11: 'Mitotic spindle',
      12: 'Centrosome',
      13: 'Plasma membrane',
      14: 'Mitochondria',
      15: 'Aggresome',
      16: 'Cytosol',
      17: 'Vesicles and punctate cytosolic patterns',
      18: 'Negative',
    }

    COLORS =  ["red", "green", "blue", "yellow"]

    async def fetch_hpa_image(image_id, size=None):
        crops = []
        for color in COLORS:
            image = await fetch_image(f'https://images.proteinatlas.org/{image_id}_{color}.jpg', grayscale=True, size=size)
            crops.append(image)
        image = np.stack(crops, axis=0)
        # assert image.shape == (4, 128, 128)
        return image

    image = await fetch_hpa_image('115/672_E2_1', size=(340, 340))
    # crop the image to a single cell
    image = image[:, 60:188, 120:248]

    # make sure the image size is 128x128
    assert image.shape == (4, 128, 128), "Invalid image shape"

@pytest.mark.asyncio
async def test_image_processing4(install_dependencies):
    import matplotlib.pyplot as plt
    import numpy as np
    from pyotritonclient import execute
    from kaibu_utils import fetch_image

    image = await fetch_hpa_image('115/672_E2_1', size=(340, 340))
    # crop the image to a single cell
    image = image[:, 60:188, 120:248]

    results = await execute([image.astype('float32')/255],
                            server_url='https://ai.imjoy.io/triton',
                            model_name='bestfitting-inceptionv3-single-cell')
    classes = results['classes']
    pred = [(LABELS[i], prob) for i, prob in enumerate(classes.tolist()) if prob > 0.5]

    assert pred, "Prediction not found"
