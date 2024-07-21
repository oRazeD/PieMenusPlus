<img align="right" width="400" src="https://user-images.githubusercontent.com/31065180/220215046-8ba7e52a-1d0c-4f71-9025-088706699176.png" />

##### Table of Contents
- [Introduction](#introduction)
- [Functionality](#functionality)
  - [Available Pie Menus](#available-pie-menus)
  - [Made for industry artists](#made-for-industry-artists)
  - [Built-in add-on integration](#built-in-add-on-integration)
  - [Non-intrusive default keymaps](#non-intrusive-default-keymaps)
  - [Stability](#stability)
  - [Extras](#extras)
    - [Extended origin and cursor manipulation](#extended-origin-and-cursor-manipulation)
    - [Improved Separate](#improved-separate)
- [Installation Guide](#installation-guide)

&nbsp;
&nbsp;

# Introduction
Welcome to the Git version of Pie Menus Plus! This page will host "volatile" releases of the add-on, although it is a very stable tool all around in its inherent simplicity.

If you are looking for stable full releases of the add-on, check out the Releases tab or head on over to the Gumroad product page linked below.

[Product Page](https://gumroad.com/l/piesplus)

[Discord Support Server](https://discord.gg/fttAx9g9WQ)

# Functionality

## Available pie menus
- Select Modes (UV compatible)
- Origin / Cursor
- Transforms & Relations
- Mesh / Curve Delete
- Shading & Overlays
- Selection
- Animation Playback
- Keyframing
- Select Active Tool
- Select Sculpt Tool
- Snapping (UV compatible)
- Proportional Editing
- LoopTools Integration
- BoolTool Integration
- Mesh Align
- Save

## Made for industry artists
Pie menus are by far the most efficient way to interact within the Blender viewport. The built-in pie menu add-on is good, but it doesn't consider certain aspects of modern modeling workflows. There is a ton of extremely useful operators that deserve to exist within pies that are simply left out in the default and built-in add-on pies, forcing you to sift through dropdowns or use the operator search.

## Built-in add-on integration
Some functionality is locked behind optional add-ons you can enable within Blender. This add-on attempts to fill some of the gaps where this extra functionality lacks pie support, while staying true a "vanilla" experience.

## Non-intrusive default keymaps
Pie Menus Plus overlays keymaps over the standard Blender keymap configuration, meaning uninstalling will maintain the original keymaps. This add-on does not accommodate industry standard keymaps but you can use it at the minor risk of other keymaps becoming "conflicted".

## Stability
Pie Menus Plus is fundamentally stable due to its inherent simplicity. It often does no more than convert existing operators into a digestible menu of contextually relevant functionality. The only functionality potentially considerable as unstable is the [Extra Tools](#extra-functionality) I tend to integrate into the add-on for larger QOL workflow improvements.

## Extras
Pie Menus Plus is sort of my do-it-all add-on and as such has some extra goodies I've made that don't really have a home anywhere else, so I threw them in! Here are the important ones:

### Extended origin and cursor manipulation
Most operators contained within the Origin / Cursor pie have access to the `Copy Active Rotation` tick within the Redo Panel of the operators.

<img src="https://imgur.com/lev0EZX.gif" width="834" height="667"/>
<img src="https://user-images.githubusercontent.com/31065180/220211533-85ee2a20-f0e5-4aeb-986b-738ba15b45ff.gif" width="830" height="706"/>

### Improved Separate
Added `Remove Modifiers` tick to the Redo Panel of the operator for situations where modifiers make separated objects completely unselectable in the 3D View.

<img src="https://imgur.com/N6yp7tj.gif" width="827" height="579"/>

# Installation guide
1. Click the **Code** button in the top right of the repo & click **Download ZIP** in the dropdown (Do not unpack the ZIP file)
2. Follow this video for the rest of the simple instructions

https://user-images.githubusercontent.com/31065180/137642217-d51470d3-a243-438f-8c49-1e367a8972ab.mp4
