from utils import Vec2
from math import sqrt


class Test_Vec2:
    def test_add(self):
        v00 = Vec2(0.0, 0.0)
        v11 = Vec2(1.0, 1.0)
        v5m3 = Vec2(5.0, -3.0)
        assert v00 + v11 == v11
        tmp = v00 + v5m3
        assert tmp == v5m3

    def test_iadd(self):
        v00 = Vec2(0.0, 0.0)
        v5m3 = Vec2(5.0, -3.0)
        v00 += v00
        assert v00 == Vec2(0.0, 0.0)
        tmp = Vec2(-100, 54)
        tmp += v5m3
        assert tmp == Vec2(-95, 51)

    def test_mul(self):
        v5m3 = Vec2(5.0, -3.0)
        assert v5m3 * 5 == Vec2(25, -15)

    def test_rmul(self):
        v5m3 = Vec2(5.0, -3.0)
        assert 5 * v5m3 == Vec2(25, -15)

    def test_imul(self):
        tmp = Vec2(5.0, -3.0)
        tmp *= 5
        assert tmp == Vec2(25, -15)

    def test_eq(self):
        v5m3 = Vec2(5.0, -3.0)
        v11 = Vec2(1, 1)
        assert v5m3 == v5m3
        assert v11 == v11
        assert v11 != v5m3
        assert v5m3 != v11

    def test_str(self):
        v5m3 = Vec2(5.0, -3.0)
        s = str(v5m3)
        assert "5." in s
        assert "-3." in s

    def test_repr(self):
        v5m3 = Vec2(5.0, -3.0)
        s = repr(v5m3)
        assert "5." in s
        assert "-3." in s

    def test_tuple(self):
        v5m3 = Vec2(5.0, -3.0)
        assert v5m3.tuple() == (5.0, -3.0)

    def test_distance(self):
        v5m3 = Vec2(5.0, -3.0)
        assert v5m3.distance(v5m3) == 0.0
        assert v5m3.distance(Vec2(4.0, -3.0)) == 1.0
        assert v5m3.distance(Vec2(5.0, 4)) == 7.0
        assert v5m3.distance(Vec2(4.0, -2.0)) == sqrt(2)

    def test_isClose(self):
        v5m3 = Vec2(5.0, -3.0)
        assert v5m3.isClose(v5m3, 1e-9)
        assert v5m3.isClose(v5m3, 1e9)
        assert v5m3.isClose(Vec2(4.0, -3.0), 1.1)
        assert not v5m3.isClose(Vec2(4.0, -3.0), 0.9)
        assert not v5m3.isClose(Vec2(5.0, 4), 6.9)
        assert v5m3.isClose(Vec2(5.0, 4), 7.0)
        assert v5m3.isClose(Vec2(5.0, 4), 7.1)
        assert not v5m3.isClose(Vec2(4.0, -2.0), 1)
        assert v5m3.isClose(Vec2(4.0, -2.0), 2)

    def test_rotated(self):
        v5m3 = Vec2(5.0, -3.0)
        assert v5m3.rotated(180).isClose(Vec2(-5.0, 3.0), 1e-9)
        assert v5m3.rotated(90).isClose(Vec2(3.0, 5.0), 1e-9)
        assert v5m3.rotated(-90).isClose(Vec2(-3.0, -5.0), 1e-9)
        assert v5m3.rotated(0).isClose(v5m3, 1e-9)
