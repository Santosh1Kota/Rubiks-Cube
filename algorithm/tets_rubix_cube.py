import numpy as np
from cubie import Cubie

def assert_dict_almost_equal(d1, d2):
    def normalize(d):
        return {tuple(int(x) for x in k): v for k, v in d.items()}
    
    d1_normalized = normalize(d1)
    d2_normalized = normalize(d2)
    
    for k, v in d1_normalized.items():
        assert k in d2_normalized, f"No match found for key {k} in second dict"
        assert v == d2_normalized[k], f"Value mismatch for key {k}: {v} != {d2_normalized[k]}"

def test_z90_clockwise():
    c = Cubie((1, 1, 1), {
        (1, 0, 0): 'red',
        (0, 1, 0): 'white',
        (0, 0, 1): 'blue'
    })
    c.z90("clockwise")
    assert np.allclose(c.position, [-1, 1, 1]), f"Position incorrect: {c.position}"
    expected_colors = {
    (0, 1, 0): 'red',
    (-1, 0, 0): 'white',
    (0, 0, 1): 'blue'
}
    assert_dict_almost_equal(c.face_colors, expected_colors)

def test_z90_counterclockwise():
    c = Cubie((1, 1, 1), {
        (1, 0, 0): 'red',
        (0, 1, 0): 'white',
        (0, 0, 1): 'blue'
    })
    c.z90("counterclockwise")
    assert np.allclose(c.position, [1, -1, 1]), f"Position incorrect: {c.position}"
    expected_colors = {
    (0, -1, 0): 'red',
    (1, 0, 0): 'white',
    (0, 0, 1): 'blue'
}
    assert_dict_almost_equal(c.face_colors, expected_colors)

def test_x90_clockwise():
    c = Cubie((1, 1, 1), {
        (0, 1, 0): 'white',
        (0, 0, 1): 'blue',
        (1, 0, 0): 'red'
    })
    c.x90("clockwise")
    assert np.allclose(c.position, [1, -1, 1]), f"Position incorrect: {c.position}"
    expected_colors = {
        (0, 0, -1): 'white',  # y+ → z−
        (0, 1, 0): 'blue',    # z+ → y+
        (1, 0, 0): 'red'      # x+ unchanged
    }
    assert_dict_almost_equal(c.face_colors, expected_colors)

def test_y90_clockwise():
    c = Cubie((1, 1, 1), {
        (1, 0, 0): 'red',
        (0, 0, 1): 'blue',
        (0, 1, 0): 'white'
    })
    c.y90("clockwise")
    assert np.allclose(c.position, [1, 1, -1]), f"Position incorrect: {c.position}"
    expected_colors = {
        (0, 0, -1): 'red',
        (1, 0, 0): 'blue',
        (0, 1, 0): 'white'
    }
    assert_dict_almost_equal(c.face_colors, expected_colors)

def run_all_tests():
    test_z90_clockwise()
    test_z90_counterclockwise()
    test_x90_clockwise()
    test_y90_clockwise()
    print("✅ All Cubie rotation tests passed.")

if __name__ == "__main__":
    run_all_tests()