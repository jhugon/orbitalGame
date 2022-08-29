# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## [v0.3.1](https://github.com/jhugon/orbitalGame/releases/tag/v0.3.1) - 2022-08-29

- [`91583f7`](https://github.com/jhugon/orbitalGame/commit/91583f7ddd368cb9a1c93cc9c3603fddd46fb475) Merge pull request #10 from jhugon/universe_refactoring
- [`e9671e9`](https://github.com/jhugon/orbitalGame/commit/e9671e9f94584da1db0ae2f143398db8042a78d1) refactor: moved some UniverseView into MainWindow in ui.py
- [`bc5fc63`](https://github.com/jhugon/orbitalGame/commit/bc5fc63d5e1fc02ee7c50777e88d9338182b446a) refactor(universe): input event handling broken out into methods
- [`04839f6`](https://github.com/jhugon/orbitalGame/commit/04839f6ada2ecb06a1d071f6ff25e695d5baac64) refactor: broke out part of UniverseModel.getFuture into copyUniverse
- [`656a5cd`](https://github.com/jhugon/orbitalGame/commit/656a5cdcc3764fdf19e846151eefbc977ef3e0f8) refactor(universe): add docstrings to methods
- [`880e0c7`](https://github.com/jhugon/orbitalGame/commit/880e0c7f33758e8ea3d3e829d2e11c553efdfcce) refactor: add typing to UniverseCtrl
- [`1d61a57`](https://github.com/jhugon/orbitalGame/commit/1d61a576683544b8634307f1327bab7dbee13b7c) refactor: added type checking to UniverseView
- [`4908542`](https://github.com/jhugon/orbitalGame/commit/490854247c6c9ebf3e610e1d6a8d254b26ea7578) refactor: get rid of path printing in universe
- [`08aab97`](https://github.com/jhugon/orbitalGame/commit/08aab97f99f75e71ae65de9fabc0bcfb294bfca7) fix: universe with Vec2 works now; kinematics returns copies of Vec2s
- [`ef216f7`](https://github.com/jhugon/orbitalGame/commit/ef216f75f5cdec4984150bf98deb76d400524784) refactor: try to use Vec2 in getFuture, but not working
- [`5d531f6`](https://github.com/jhugon/orbitalGame/commit/5d531f628f0f9d09795ede4fc043a8ee441dac85) refactor: Merge branch main into universe_refactoring
- [`fe845f8`](https://github.com/jhugon/orbitalGame/commit/fe845f8f1dba4ed56ad0cdba29c59a48be779adc) revert(universe): reverted code to use tuples instead of Vec2
- [`b95a2f6`](https://github.com/jhugon/orbitalGame/commit/b95a2f600d706128fd0ff419bb66a9a98fc03df1) refactor: adding type annotations to UniverseModel

## [v0.3.0](https://github.com/jhugon/orbitalGame/releases/tag/v0.3.0) - 2022-08-26

- [`fe62b46`](https://github.com/jhugon/orbitalGame/commit/fe62b46bb8ebeef3e69a5f1205a72cdf7690ad3e) feat: add montage images of all of the sprites
- [`22b1c55`](https://github.com/jhugon/orbitalGame/commit/22b1c55496224c136ac900945072383263f55351) refactor: add type refs to Universe* in spaceobject.py
- [`83795ad`](https://github.com/jhugon/orbitalGame/commit/83795ada5bc6bc90572a15e4022278a153f55293) Merge pull request #12 from jhugon/futurepaths_typechecking
- [`602323a`](https://github.com/jhugon/orbitalGame/commit/602323a1c7fe55e8340d7356fda359f191c2f70a) refactor: type checking now works in futurepaths.py
- [`b36b741`](https://github.com/jhugon/orbitalGame/commit/b36b741ca365255058fe2ff1c324b980c635bb98) refactor: added broken type-checking to futurepaths

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
