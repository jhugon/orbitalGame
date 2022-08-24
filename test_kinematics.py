from kinematics import ObjectKinematics
from utils import Vec2
from math import sqrt, pi


class Test_ObjectKinematics:
    def test_getters(self):
        k = ObjectKinematics(Vec2(0.0, 0.0), Vec2(0.0, 0.0), Vec2(0.0, 0.0))
        assert k.getPosition() == Vec2(0.0, 0.0)
        assert k.getVelocity() == Vec2(0.0, 0.0)
        assert k.getAcceleration() == Vec2(0.0, 0.0)
        k = ObjectKinematics(Vec2(1.0, 2.0), Vec2(0.0, 1000.0), Vec2(5.0, 3.0))
        assert k.getPosition() == Vec2(1.0, 2.0)
        assert k.getVelocity() == Vec2(0.0, 1000.0)
        assert k.getDirection() == -pi / 2.0
        assert k.getDirectionDeg() == -90.0
        assert k.getAcceleration() == Vec2(5.0, 3.0)
        k.updateAcceleration(Vec2(3.0, 10.0))
        assert k.getAcceleration() == Vec2(3.0, 10.0)

    def test_updatePosVel(self):
        k = ObjectKinematics(Vec2(0.0, 0.0), Vec2(0.0, 0.0), Vec2(1.0, 0.0))
        assert k.getVelocity() == Vec2(0.0, 0.0)
        assert k.getPosition() == Vec2(0.0, 0.0)
        assert k.getAcceleration() == Vec2(1.0, 0.0)
        k.updatePosVel(1.0)
        assert k.getVelocity() == Vec2(1.0, 0.0)
        assert k.getPosition() == Vec2(1.0, 0.0)
        assert k.getAcceleration() == Vec2(1.0, 0.0)
        k.updatePosVel(2.0)
        assert k.getVelocity() == Vec2(3.0, 0.0)
        assert k.getPosition() == Vec2(7.0, 0.0)
        assert k.getAcceleration() == Vec2(1.0, 0.0)

        k = ObjectKinematics(Vec2(1000.0, 0.0), Vec2(0.0, 0.0), Vec2(-5.0, -10.0))
        assert k.getVelocity() == Vec2(0.0, 0.0)
        assert k.getPosition() == Vec2(1000.0, 0.0)
        assert k.getAcceleration() == Vec2(-5.0, -10.0)
        k.updatePosVel(100.0)
        assert k.getVelocity() == Vec2(-500.0, -1000.0)
        assert k.getPosition() == Vec2(1000.0 - 50000, -100000)
        assert k.getAcceleration() == Vec2(-5.0, -10.0)
