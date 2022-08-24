# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## [v0.2.2](https://github.com/jhugon/orbitalGame/releases/tag/v0.2.2) - 2022-08-24

- [`2bf59eb`](https://github.com/jhugon/orbitalGame/commit/2bf59ebb4d878538c9d594527c6c742b785a2857) Merge pull request #9 from jhugon/spaceobjectviewrefactor
- [`e5979e7`](https://github.com/jhugon/orbitalGame/commit/e5979e7c2e4b4e6eb16bfe6051a1279774b223e2) chore: update CHANGELOG with comments about #9
- [`5f5d9c9`](https://github.com/jhugon/orbitalGame/commit/5f5d9c941a35c5598b2f6284aa223e0acf4a71d7) refactor(spaceobject): finish adding annotations and comments to file
- [`60f06bf`](https://github.com/jhugon/orbitalGame/commit/60f06bf35c277ca2c567f328f33bea2ebe2ee88d) refactor: thrustDirection -> drawFlame and clearer
- [`d7303ef`](https://github.com/jhugon/orbitalGame/commit/d7303ef5a061e1e83f3a99c73a2b3c2e07f73abd) fix: errors in latest version of mypy
- [`f761e15`](https://github.com/jhugon/orbitalGame/commit/f761e157894b62865d30374b4b2256e388c4f2b0) ci: now only runs on pull_reqs and pushes to main
- [`c3e0ee0`](https://github.com/jhugon/orbitalGame/commit/c3e0ee06ef2bfc0d068aba420262aa14dd82b462) fix: SpaceObjectView.update type didnt match Sprite
- [`9466a34`](https://github.com/jhugon/orbitalGame/commit/9466a34ccc99aba1288e5b185d5b87dedefb0f09) refactor: SpaceObjectView prepare image/rect in seperate method

Finished refactoring classes in spaceobject, the SpaceObjectView constructor is
much more comprehensible, in particular.

## [v0.2.1](https://github.com/jhugon/orbitalGame/releases/tag/v0.2.1) - 2022-08-24

- [`fe31762`](https://github.com/jhugon/orbitalGame/commit/fe31762b859d85b69404ce97783d469de38d2086) Merge pull request #6 from jhugon/KinematicsModel
- [`7319782`](https://github.com/jhugon/orbitalGame/commit/7319782355913ed326a324719b961c9c97a00624) fix: now future paths work again, kinematic == fixed
- [`a457b02`](https://github.com/jhugon/orbitalGame/commit/a457b023579de31167fcc370664b5ee840a3d111) refactor: SpaceObjectModel uses kinematic class now
- [`5854e96`](https://github.com/jhugon/orbitalGame/commit/5854e969ebe72ef343c2623768ab99bdc3b99190) refactor: added tests for kinematics.py
- [`92c79b2`](https://github.com/jhugon/orbitalGame/commit/92c79b23a195b296f6e43d32260909e077d1d329) refactor: add kinematics.py

## [v0.2.0](https://github.com/jhugon/orbitalGame/releases/tag/v0.2.0) - 2022-08-23

- [`7bb7e88`](https://github.com/jhugon/orbitalGame/commit/7bb7e88f2ef4ea6d590cde6f718ebbf4daaced46) ci: added pytest to github ci action
- [`4100fa9`](https://github.com/jhugon/orbitalGame/commit/4100fa99a1a7cabe07371f0baff5f2bee16afb88) feat: Vec2 added distance isclose __eq__ and unit tests
- [`ea16889`](https://github.com/jhugon/orbitalGame/commit/ea168892ea90c107e70f590d508756a5106eb8f3) refactor: modify and type annotate Vec2

## [v0.1.2](https://github.com/jhugon/orbitalGame/releases/tag/v0.1.2) - 2022-08-23

- [`a2ee02f`](https://github.com/jhugon/orbitalGame/commit/a2ee02f289e6e1fba8e7173ba7bf3b4b998dbb36) Merge pull request #4 from jhugon/multi-files
- [`822bec0`](https://github.com/jhugon/orbitalGame/commit/822bec0f4091bc5aa7541e71cab32f70f7923467) fix: fix imports now that multiple files
- [`2e11162`](https://github.com/jhugon/orbitalGame/commit/2e1116298f0a60cb39ade7aeb9b59c86f4c9c2ad) ci: add mypy pre-commit hook
- [`2370df2`](https://github.com/jhugon/orbitalGame/commit/2370df28a4e00f8565971dd3c1fac0452bbfb275) refactor: working on splitting into multi files

## [v0.1.1](https://github.com/jhugon/orbitalGame/releases/tag/v0.1.1) - 2022-08-23

- [`cfb3974`](https://github.com/jhugon/orbitalGame/commit/cfb39746622c620a92d7622f597173593800b7ce) fix(CI): fix mypy GitHub action

## [v0.1.0](https://github.com/jhugon/orbitalGame/releases/tag/v0.1.0) - 2022-08-23

- [`3b61df3`](https://github.com/jhugon/orbitalGame/commit/3b61df370e4186ad88e910b6d26416a262ad7b6f) feat: Added mypy CI and made code pass
- [`22ac09a`](https://github.com/jhugon/orbitalGame/commit/22ac09aa3aaf44ccad39cf3742c84bd9bf53a94f) ci: added uplift and black Github actions
- [`7f495cc`](https://github.com/jhugon/orbitalGame/commit/7f495ccf58238aec5cf955dbed685b0abf01b89c) refactor: ran black on engine.py
- [`44b1c4f`](https://github.com/jhugon/orbitalGame/commit/44b1c4fb1d3d8cb7a9ac760c1a38a324f382e5b4) added engine.py, sprites, and makeSprites.sh
- [`125feb4`](https://github.com/jhugon/orbitalGame/commit/125feb4788e07743c728892d2527526d32176624) Initial commit
