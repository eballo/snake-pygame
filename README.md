# Snake Game

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Python 3.7][python-shield]][python-url]
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

Snake Game crated using Pygame Library

In this game there are tow characters: the snake (the player) and its food. Whenever the snake eats food, its lenght should be increased.
- whenever the snake eats the food, we have to generate new food in a new position.
- whenever the snake eats the food, we have to incrrease the speed of the snake to make the game more difficult. We should also track collisions beteen the snake's head and its body.



![ScreenShot][product-screenshot-1]
![ScreenShot][product-screenshot-2]


## Getting Started

To get a local copy up and running follow these simple example steps.

### Installation

Install the project dependencies

```sh
pip install -r requirements.txt
```

## Usage

Use the Keys to manage the snake and eat the food.

### Run the game
```sh 
python game.py
```


## Release History

* 1.0
    * Pygame working version

* 1.1
    * Add Score

* 1.x
    * Refactor to use Sprites
    * Add Victory, Game Over Screen
    * Add Sound Effects + Music
    * Add PS4 controller support
    * Full screen support
    * Add Level support
  

#### TODO:
- History
- Multiplayer
- configuration
    - on / off music
    - on / off sound effects
    - Translations
- Credits
- Add levels
  - Increase speed
  - Add walls
  - add objects/booms
- Add food different value, different time
  - apple
- Hall of Fame
- Boss Monster
- Snake AI


## Acknowledgements
* [PyGame](https://www.pygame.org/news)
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Img Shields](https://shields.io)
* [Google Fonts](https://fonts.google.com/)

### Multiplayer Resources
* [Youtbe Tutorial multiplayer](https://www.youtube.com/watch?v=McoDjOCb2Zo)
* [udppong - code inspiration multiplayer](https://github.com/marvin939/udpong)

### Music Resources
* [Creatation of values](https://opengameart.org/content/creation-of-values)
* [Insert coin](https://opengameart.org/content/insert-coin)
* [Victory](https://opengameart.org/content/victory-1)
* [Menu and Jingles](https://opengameart.org/content/ui-and-item-sound-effect-jingles-sample-2)
* [Death sound effect](https://opengameart.org/content/hurt-death-sound-effect-for-character)
* [The Tunnel](https://opengameart.org/content/the-tunnel-2)

### PS4 Controller
* [PS4](https://www.youtube.com/watch?v=hqBgJQOa_1E)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[python-shield]: https://img.shields.io/badge/python-3.7-blue.svg
[python-url]: https://www.python.org/downloads/release/python-370/
[contributors-shield]: https://img.shields.io/github/contributors/eballo/snake-pygame.svg?style=flat-square
[contributors-url]: https://github.com/eballo/snake-pygame/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/eballo/snake-pygame.svg?style=flat-square
[forks-url]: https://github.com/eballo/snake-pygame/network/members
[stars-shield]: https://img.shields.io/github/stars/eballo/snake-pygame.svg?style=flat-square
[stars-url]: https://github.com/eballo/snake-pygame/stargazers
[issues-shield]: https://img.shields.io/github/issues/eballo/snake-pygame.svg?style=flat-square
[issues-url]: https://github.com/eballo/snake-pygame/issues
[product-screenshot-1]: screenshots/screenshot02.png
[product-screenshot-2]: screenshots/screenshot03.png