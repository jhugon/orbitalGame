#!/bin/bash

shopt -s extglob

for i in spritesOrig/Sprite*.png; do
  basename=${i%.png}
  basename=${basename#"spritesOrig/"}
  for color in white blue green yellow red pink; do
    convert $i -channel RGB -fuzz 40% -fill $color -opaque black PNG32:sprites/$basename"_"$color.png
  done
done

for i in spritesOrig/!(Sprite*).png; do
  basename=${i%.png}
  basename=${basename#"spritesOrig/"}
  for color in white lightblue yellow red pink cyan magenta royalblue1 deepskyblue springgreen lime firebrick1; do
    convert $i -channel RGB -fuzz 40% -fill $color -opaque white PNG32:sprites/$basename"_"$color.png
  done
done


for i in spritesExt/nichol/*.png; do
  basename=${i%.png}
  basename=${basename#"spritesExt/nichol/"}
    convert $i -shave 40x40 PNG32:sprites/$basename.png
done
