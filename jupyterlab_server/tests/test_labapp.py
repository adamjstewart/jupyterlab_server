"""Basic tests for the lab handlers.
"""

import pytest

@pytest.fixture
def notebooks(create_notebook, make_lab_extension_app):
    make_lab_extension_app()
    nbpaths = (
        'notebook1.ipynb',
        'jlab_test_notebooks/notebook2.ipynb',
        'jlab_test_notebooks/level2/notebook3.ipynb'
    )
    for nb in nbpaths:
        create_notebook(nb)
    return nbpaths


async def test_lab_handler(notebooks, fetch, http_port, labserverapp):
    r = await fetch('lab', 'jlab_test_notebooks')
    assert r.code == 200
    # Check that the lab template is loaded
    html = r.body.decode()
    assert "Files" in html
    assert "JupyterLab Test App" in html

async def test_notebook_handler(notebooks, fetch, labserverapp):
    for nbpath in notebooks:
        r = await fetch('lab', nbpath)
        assert r.code == 200
        # Check that the notebook template is loaded
        html = r.body.decode()
        assert "JupyterLab Test App" in html
